from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  

    @property
    def get_db_credentials(self):
        """Retorna las credenciales de base de datos"""
        return {
            "user": self.DB_USER,
            "password": self.DB_PASSWORD,
            "host": self.DB_HOST,
            "port": self.DB_PORT,
            "name": self.DB_NAME
        }

settings = Settings()