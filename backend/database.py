from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings
from urllib.parse import quote_plus
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('database')

# Obtener las credenciales de la base de datos
db_credentials = settings.get_db_credentials

# Log de conexión
logger.info(f"Conectando a la base de datos en: {db_credentials['host']}:{db_credentials['port']}/{db_credentials['name']}")

try:
    # Codifica la contraseña para manejar caracteres especiales
    encoded_password = quote_plus(db_credentials["password"])

    # URL de conexión a PostgreSQL
    SQLALCHEMY_DATABASE_URL = f"postgresql://{db_credentials['user']}:{encoded_password}@{db_credentials['host']}:{db_credentials['port']}/{db_credentials['name']}"

    # Motor de la base de datos
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

    # Sesión de la base de datos
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Base para los modelos
    Base = declarative_base()
except Exception as e:
    logger.error(f"Error al configurar la conexión a la base de datos: {str(e)}")
    raise

# Importa todos los modelos para que Alembic los detecte correctamente
from models.docente_model import Docente
from models.curso_model import Curso
from models.horario_model import Horario
from models.bloque_model import Bloque
from models.materia_model import Materia
from models.salon_model import Salon


# Dependencia para inyectar la sesión de la base de datos en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error de base de datos: {str(e)}")
        raise
    finally:
        db.close()
        
# Asegurar que todas las tablas sean creadas si no existen
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.error(f"Error al crear las tablas: {str(e)}")