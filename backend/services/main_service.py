from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Tuple
import random

#materia
from repositories.materia_repository import MateriaRepository
from schemas.requests.materia_request import MateriaRequest
from schemas.responses.materia_response import MateriaResponse

#docente
from repositories.docente_repository import DocenteRepository
from schemas.requests.docente_request import DocenteRequest
from schemas.responses.docente_response import DocenteResponse

#salon
from repositories.salon_repository import SalonRepository
from schemas.requests.salon_request import SalonRequest
from schemas.responses.salon_response import SalonResponse

#curso
from repositories.curso_repository import CursoRepository
from schemas.requests.curso_request import CursoRequest
from schemas.responses.curso_response import CursoResponse

#bloque
from repositories.bloque_repository import BloqueRepository
from schemas.requests.bloque_request import BloqueRequest
from schemas.responses.bloque_response import BloqueResponse

#horario
from repositories.horario_repository import HorarioRepository
from schemas.requests.horario_request import HorarioRequest
from schemas.responses.horario_response import HorarioResponse


class MainService:
    def __init__(self, db: Session):
        self.db = db
        self.materia_repository = MateriaRepository(db)
        self.docente_repository = DocenteRepository(db)
        self.salon_repository = SalonRepository(db)
        self.curso_repository = CursoRepository(db)
        self.bloque_repository = BloqueRepository(db)
        self.horario_repository = HorarioRepository(db)
        
    def to_salon_response(self, salon):
        """Método auxiliar para crear un objeto SalonResponse a partir de un objeto salón."""
        return SalonResponse(
            id=salon.id,
            bloque=salon.bloque,
            numero=salon.numero,
            es_sistemas=salon.es_sistemas
        )
    
    def to_materia_response(self, materia):
        """Método auxiliar para crear un objeto MateriaResponse a partir de un objeto materia."""
        return MateriaResponse(
            id=materia.id,
            codigo=materia.codigo,
            nombre=materia.nombre,
            cantidad_horas=materia.cantidad_horas,
            requiere_sala_sistemas=materia.requiere_sala_sistemas
        )
        
    def to_docente_response(self, docente):
        """Método auxiliar para crear un objeto DocenteResponse a partir de un objeto docente."""
        return DocenteResponse(
            id=docente.id,
            cc=docente.cc,
            nombre=docente.nombre,
            restricciones=docente.restricciones,
            materias=docente.materias
        )
        
    def get_salones(self):
        """Obtiene todos los salones."""
        salones = self.salon_repository.get_all()
        
        return [self.to_salon_response(salon) for salon in salones]
    
    def get_salones(self):
        """Obtiene todos los salones."""
        salones = self.salon_repository.get_all()
        
        return [self.to_salon_response(salon) for salon in salones]
    
    def get_docentes(self):
        """Obtiene todos los docentes y retorna una lista de DocenteResponse."""
        docentes = self.docente_repository.get_all()
        
        return [self.to_docente_response(docente) for docente in docentes]
    
    def generar_horarios_automaticos(self):
        """
        Genera automáticamente horarios para todos los cursos basados en las reglas establecidas.
        
        Reglas:
        1. Los cursos se generan en base a docentes, materias y salones disponibles.
        2. Los bloques se crean según la cantidad de horas de la materia (ej: 4 horas = 2 bloques de 2 horas).
        3. Horarios disponibles: 8-12 (mañana), 14-18 (tarde), 18-22 (noche).
        4. Un docente puede dar máximo 6 cursos.
        5. No se pueden asignar bloques a docentes en horarios donde tienen restricciones.
        6. Materias que requieren sala de sistemas deben asignarse a salones de sistemas.
        7. Cursos de la misma materia con diferentes profesores deben tener el mismo horario.
        8. Los bloques de horario son: 8-10, 10-12, 14-16, 16-18, 18-20, 20-22.
        9. Para cada materia se intentará crear cursos en franja Diurna y Nocturna.
        
        Returns:
            Dict: Resultado de la generación con información de éxito y detalles.
        """
        try:
            # Obtener todos los datos necesarios
            materias = self.materia_repository.get_all()
            docentes = self.docente_repository.get_all()
            salones = self.salon_repository.get_all()
            
            # Verificar si hay datos suficientes
            if not materias or not docentes or not salones:
                return {
                    "exito": False,
                    "mensaje": "No hay suficientes datos para generar horarios (materias, docentes o salones)"
                }
            
            # Imprimir información sobre las materias que se pueden impartir
            print("\n===== MATERIAS QUE SE PUEDEN IMPARTIR =====")
            materias_impartibles = []
            materias_no_impartibles = []
            
            for materia in materias:
                # Filtrar docentes que pueden enseñar esta materia
                docentes_disponibles = [d for d in docentes if materia.id in (d.materias or [])]
                
                if docentes_disponibles:
                    materias_impartibles.append(materia)
                    nombres_docentes = [d.nombre for d in docentes_disponibles]
                    print(f"ID: {materia.id}, Código: {materia.codigo}, Nombre: {materia.nombre}")
                    print(f"   Docentes que pueden impartirla: {', '.join(nombres_docentes)}")
                    print(f"   Horas: {materia.cantidad_horas}, Requiere sala de sistemas: {materia.requiere_sala_sistemas}")
                    print("-------------------------------------------")
                else:
                    materias_no_impartibles.append(materia)
            
            print(f"\nTotal de materias en la base de datos: {len(materias)}")
            print(f"Materias que se pueden impartir: {len(materias_impartibles)}")
            print(f"Materias que NO se pueden impartir: {len(materias_no_impartibles)}")
            print("===========================================\n")
            
            # Definir los días y franjas horarias disponibles
            dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
            franjas_horarias = [(8, 10), (10, 12), (14, 16), (16, 18), (18, 20), (20, 22)]
            
            # Mapeo de franjas horarias a períodos del día
            franja_a_periodo = {
                (8, 10): "mañana", 
                (10, 12): "mañana",
                (14, 16): "tarde", 
                (16, 18): "tarde",
                (18, 20): "noche", 
                (20, 22): "noche"
            }
            
            # Mapeo de períodos a franjas (Diurna/Nocturna)
            periodo_a_franja = {
                "mañana": "Diurna",
                "tarde": "Diurna",
                "noche": "Nocturna"
            }
            
            # Estructura para seguimiento de asignaciones
            asignaciones_docentes = {docente.id: [] for docente in docentes}  # Cursos asignados a cada docente
            bloques_ocupados = {}  # Bloques ya ocupados por salón
            horarios_por_materia = {}  # Horarios asignados por materia (ahora será un diccionario de listas)
            plantillas_bloques_por_materia = {}  # Almacena la estructura de bloques para cada materia
            franjas_por_materia = {}  # Franjas (Diurna/Nocturna) asignadas a cada materia
            
            # Resultados
            cursos_creados = []
            horarios_creados = []
            bloques_creados = []
            
            # Crear un diccionario para rastrear qué docentes han sido asignados a cada materia
            docentes_asignados_por_materia = {}
            
            # Procesar cada materia
            for materia in materias:
                # Determinar cuántos bloques necesita esta materia
                horas_totales = materia.cantidad_horas
                bloques_necesarios = []
                
                # Dividir las horas en bloques de 2 horas (o 3 si son 3 horas)
                if horas_totales % 2 == 0:  # Si es par, bloques de 2 horas
                    num_bloques = horas_totales // 2
                    for _ in range(num_bloques):
                        bloques_necesarios.append(2)
                else:  # Si es impar, un bloque de 3 horas y el resto de 2
                    bloques_necesarios.append(3)
                    horas_restantes = horas_totales - 3
                    for _ in range(horas_restantes // 2):
                        bloques_necesarios.append(2)
                
                # Filtrar docentes que pueden enseñar esta materia
                docentes_disponibles = [d for d in docentes if materia.id in (d.materias or [])]
                
                if not docentes_disponibles:
                    continue  # Saltar esta materia si no hay docentes que puedan enseñarla
                
                # Filtrar salones adecuados para esta materia
                if materia.requiere_sala_sistemas:
                    salones_adecuados = [s for s in salones if s.es_sistemas]
                else:
                    salones_adecuados = salones
                
                if not salones_adecuados:
                    continue  # Saltar esta materia si no hay salones adecuados
                
                # Inicializar seguimiento de franjas para esta materia
                franjas_por_materia[materia.id] = set()
                docentes_asignados_por_materia[materia.id] = set()
                
                # Clasificar docentes por franja disponible
                docentes_diurnos = []
                docentes_nocturnos = []
                
                for docente in docentes_disponibles:
                    # Un docente puede dar en franja Diurna si no tiene restricciones en mañana y tarde
                    puede_dar_diurno = True
                    if docente.restricciones:
                        if "mañana" in docente.restricciones and "tarde" in docente.restricciones:
                            puede_dar_diurno = False
                    
                    # Un docente puede dar en franja Nocturna si no tiene restricción en noche
                    puede_dar_nocturno = True
                    if docente.restricciones and "noche" in docente.restricciones:
                        puede_dar_nocturno = False
                    
                    if puede_dar_diurno:
                        docentes_diurnos.append(docente)
                    if puede_dar_nocturno:
                        docentes_nocturnos.append(docente)
                
                # Crear plantillas de bloques para esta materia (una para diurna y otra para nocturna)
                if materia.id not in plantillas_bloques_por_materia:
                    plantillas_bloques_por_materia[materia.id] = {}
                    horarios_por_materia[materia.id] = {"Diurna": [], "Nocturna": []}
                    
                    # Crear plantilla para franja Diurna (mañana y tarde)
                    franjas_diurnas = [(8, 10), (10, 12), (14, 16), (16, 18)]
                    plantilla_diurna = self._crear_plantilla_bloques(
                        bloques_necesarios,
                        dias_semana,
                        franjas_diurnas
                    )
                    
                    if plantilla_diurna:
                        plantillas_bloques_por_materia[materia.id]["Diurna"] = plantilla_diurna
                    
                    # Crear plantilla para franja Nocturna (noche)
                    franjas_nocturnas = [(18, 20), (20, 22)]
                    plantilla_nocturna = self._crear_plantilla_bloques(
                        bloques_necesarios,
                        dias_semana,
                        franjas_nocturnas
                    )
                    
                    if plantilla_nocturna:
                        plantillas_bloques_por_materia[materia.id]["Nocturna"] = plantilla_nocturna
                
                # Ordenar docentes por cantidad de cursos asignados (priorizar los que tienen menos)
                docentes_diurnos.sort(key=lambda d: len(asignaciones_docentes[d.id]))
                docentes_nocturnos.sort(key=lambda d: len(asignaciones_docentes[d.id]))
                
                # Intentar asignar cursos en franja Diurna
                if "Diurna" in plantillas_bloques_por_materia[materia.id] and docentes_diurnos:
                    for docente in docentes_diurnos:
                        # Verificar si el docente ya tiene 6 cursos
                        if len(asignaciones_docentes[docente.id]) >= 6:
                            continue
                        
                        # Si ya hay un docente asignado a esta materia en esta franja, 
                        # y hay otros docentes disponibles que aún no tienen cursos, priorizar a esos
                        if "Diurna" in franjas_por_materia[materia.id] and docente.id in docentes_asignados_por_materia[materia.id]:
                            # Verificar si hay otros docentes disponibles que aún no tienen esta materia
                            otros_docentes = [d for d in docentes_diurnos if d.id != docente.id and d.id not in docentes_asignados_por_materia[materia.id]]
                            if otros_docentes:
                                continue  # Saltar este docente y probar con otro
                        
                        # Crear un nuevo horario para este docente y materia en franja Diurna
                        nuevo_horario = self.horario_repository.create({"franja": "Diurna"})
                        horarios_creados.append(nuevo_horario)
                        
                        # Asignar bloques al horario usando la plantilla diurna
                        bloques_asignados = self._asignar_bloques_con_plantilla(
                            nuevo_horario.id,
                            plantillas_bloques_por_materia[materia.id]["Diurna"],
                            salones_adecuados,
                            bloques_ocupados
                        )
                        
                        if not bloques_asignados:
                            # Si no se pudieron asignar bloques, eliminar el horario
                            self.horario_repository.delete(nuevo_horario.id)
                            continue
                        
                        bloques_creados.extend(bloques_asignados)
                        horarios_por_materia[materia.id]["Diurna"].append(nuevo_horario.id)
                        
                        # Verificar si el docente tiene restricciones para los bloques de este horario
                        restriccion_encontrada = False
                        for bloque in bloques_asignados:
                            hora_inicio = bloque.horaInicio
                            hora_fin = bloque.horaFin
                            periodo = next((franja_a_periodo[f] for f in franjas_horarias if f[0] == hora_inicio and f[1] == hora_fin), None)
                            
                            if periodo and docente.restricciones and periodo in docente.restricciones:
                                restriccion_encontrada = True
                                break
                        
                        if restriccion_encontrada:
                            # Si hay restricciones, eliminar el horario y sus bloques
                            for bloque in bloques_asignados:
                                self.bloque_repository.delete(bloque.id)
                            self.horario_repository.delete(nuevo_horario.id)
                            continue
                        
                        # Crear un nuevo curso para este docente y materia
                        codigo_curso = f"{materia.codigo}-{docente.id}-D"  # D para Diurno
                        grupo = f"Grupo-{len(cursos_creados) + 1}"
                        
                        nuevo_curso = self.curso_repository.create({
                            "codigo": codigo_curso,
                            "horario_id": nuevo_horario.id,
                            "docente_id": docente.id,
                            "grupo": grupo,
                            "materia_id": materia.id
                        })
                        
                        cursos_creados.append(nuevo_curso)
                        asignaciones_docentes[docente.id].append(nuevo_curso.id)
                        franjas_por_materia[materia.id].add("Diurna")
                        docentes_asignados_por_materia[materia.id].add(docente.id)
                        break  # Solo necesitamos un curso por franja
                
                # Intentar asignar cursos en franja Nocturna
                if "Nocturna" in plantillas_bloques_por_materia[materia.id] and docentes_nocturnos:
                    for docente in docentes_nocturnos:
                        # Verificar si el docente ya tiene 6 cursos
                        if len(asignaciones_docentes[docente.id]) >= 6:
                            continue
                        
                        # Si ya hay un docente asignado a esta materia en esta franja, 
                        # y hay otros docentes disponibles que aún no tienen cursos, priorizar a esos
                        if "Nocturna" in franjas_por_materia[materia.id] and docente.id in docentes_asignados_por_materia[materia.id]:
                            # Verificar si hay otros docentes disponibles que aún no tienen esta materia
                            otros_docentes = [d for d in docentes_nocturnos if d.id != docente.id and d.id not in docentes_asignados_por_materia[materia.id]]
                            if otros_docentes:
                                continue  # Saltar este docente y probar con otro
                        
                        # Crear un nuevo horario para este docente y materia en franja Nocturna
                        nuevo_horario = self.horario_repository.create({"franja": "Nocturna"})
                        horarios_creados.append(nuevo_horario)
                        
                        # Asignar bloques al horario usando la plantilla nocturna
                        bloques_asignados = self._asignar_bloques_con_plantilla(
                            nuevo_horario.id,
                            plantillas_bloques_por_materia[materia.id]["Nocturna"],
                            salones_adecuados,
                            bloques_ocupados
                        )
                        
                        if not bloques_asignados:
                            # Si no se pudieron asignar bloques, eliminar el horario
                            self.horario_repository.delete(nuevo_horario.id)
                            continue
                        
                        bloques_creados.extend(bloques_asignados)
                        horarios_por_materia[materia.id]["Nocturna"].append(nuevo_horario.id)
                        
                        # Verificar si el docente tiene restricciones para los bloques de este horario
                        restriccion_encontrada = False
                        for bloque in bloques_asignados:
                            hora_inicio = bloque.horaInicio
                            hora_fin = bloque.horaFin
                            periodo = next((franja_a_periodo[f] for f in franjas_horarias if f[0] == hora_inicio and f[1] == hora_fin), None)
                            
                            if periodo and docente.restricciones and periodo in docente.restricciones:
                                restriccion_encontrada = True
                                break
                        
                        if restriccion_encontrada:
                            # Si hay restricciones, eliminar el horario y sus bloques
                            for bloque in bloques_asignados:
                                self.bloque_repository.delete(bloque.id)
                            self.horario_repository.delete(nuevo_horario.id)
                            continue
                        
                        # Crear un nuevo curso para este docente y materia
                        codigo_curso = f"{materia.codigo}-{docente.id}-N"  # N para Nocturno
                        grupo = f"Grupo-{len(cursos_creados) + 1}"
                        
                        nuevo_curso = self.curso_repository.create({
                            "codigo": codigo_curso,
                            "horario_id": nuevo_horario.id,
                            "docente_id": docente.id,
                            "grupo": grupo,
                            "materia_id": materia.id
                        })
                        
                        cursos_creados.append(nuevo_curso)
                        asignaciones_docentes[docente.id].append(nuevo_curso.id)
                        franjas_por_materia[materia.id].add("Nocturna")
                        docentes_asignados_por_materia[materia.id].add(docente.id)
                        break  # Solo necesitamos un curso por franja
            
            # Verificar si se generaron cursos para todas las materias impartibles
            materias_con_cursos = set()
            for curso in cursos_creados:
                materias_con_cursos.add(curso.materia_id)
            
            materias_impartibles_ids = {materia.id for materia in materias_impartibles}
            materias_sin_cursos = materias_impartibles_ids - materias_con_cursos
            
            # Calcular porcentaje de cobertura
            porcentaje_cobertura = (len(materias_con_cursos) / len(materias_impartibles_ids)) * 100 if materias_impartibles_ids else 0
            
            # Verificar docentes sin cursos asignados
            docentes_sin_cursos = [docente for docente in docentes if not asignaciones_docentes[docente.id]]
            
            print("\n===== VERIFICACIÓN DE COBERTURA DE MATERIAS =====")
            print(f"Total de materias impartibles: {len(materias_impartibles_ids)}")
            print(f"Materias con cursos asignados: {len(materias_con_cursos)} ({porcentaje_cobertura:.2f}%)")
            print(f"Materias sin cursos asignados: {len(materias_sin_cursos)}")
            
            print("\n===== VERIFICACIÓN DE ASIGNACIÓN DE DOCENTES =====")
            print(f"Total de docentes: {len(docentes)}")
            print(f"Docentes con al menos un curso: {len(docentes) - len(docentes_sin_cursos)}")
            print(f"Docentes sin cursos asignados: {len(docentes_sin_cursos)}")
            if docentes_sin_cursos:
                print("Nombres de docentes sin cursos:")
                for docente in docentes_sin_cursos:
                    print(f"- {docente.nombre}")
            
            # Retornar resultado
            return {
                "exito": True,
                "mensaje": "Horarios generados con éxito",
                "detalles": {
                    "cursos_creados": len(cursos_creados),
                    "horarios_creados": len(horarios_creados),
                    "bloques_creados": len(bloques_creados),
                    "materias_con_cursos": len(materias_con_cursos),
                    "materias_sin_cursos": len(materias_sin_cursos),
                    "porcentaje_cobertura": porcentaje_cobertura,
                    "docentes_sin_cursos": len(docentes_sin_cursos)
                }
            }
            
        except Exception as e:
            print(f"Error al generar horarios: {str(e)}")
            return {
                "exito": False,
                "mensaje": f"Error al generar horarios: {str(e)}"
            }
    
    def _crear_plantilla_bloques(self, bloques_necesarios, dias_semana, franjas_horarias):
        """
        Crea una plantilla de bloques para una materia.
        
        Args:
            bloques_necesarios: Lista con la duración de cada bloque necesario (en horas).
            dias_semana: Lista de días disponibles.
            franjas_horarias: Lista de tuplas (hora_inicio, hora_fin) disponibles.
            
        Returns:
            List: Lista de diccionarios con la información de cada bloque.
        """
        # Si no hay suficientes bloques disponibles, retornar None
        if len(bloques_necesarios) > len(dias_semana):
            return None
        
        # Seleccionar días aleatorios para los bloques
        dias_seleccionados = random.sample(dias_semana, len(bloques_necesarios))
        
        # Crear la plantilla de bloques
        plantilla = []
        for i, duracion in enumerate(bloques_necesarios):
            dia = dias_seleccionados[i]
            
            # Filtrar franjas horarias que coincidan con la duración del bloque
            franjas_adecuadas = [f for f in franjas_horarias if f[1] - f[0] == duracion]
            
            if not franjas_adecuadas:
                # Si no hay franjas exactas, tomar cualquiera (esto podría mejorarse)
                if not franjas_horarias:
                    return None
                franja = random.choice(franjas_horarias)
            else:
                franja = random.choice(franjas_adecuadas)
            
            plantilla.append({
                "dia": dia,
                "horaInicio": franja[0],
                "horaFin": franja[1]
            })
        
        return plantilla
    
    def _asignar_bloques_con_plantilla(self, horario_id, plantilla, salones_disponibles, bloques_ocupados):
        """
        Asigna bloques a un horario usando una plantilla predefinida.
        
        Args:
            horario_id: ID del horario al que se asignarán los bloques.
            plantilla: Lista de diccionarios con la información de cada bloque.
            salones_disponibles: Lista de salones disponibles.
            bloques_ocupados: Diccionario para seguimiento de bloques ocupados.
            
        Returns:
            List: Lista de bloques creados.
        """
        bloques_creados = []
        
        for info_bloque in plantilla:
            dia = info_bloque["dia"]
            hora_inicio = info_bloque["horaInicio"]
            hora_fin = info_bloque["horaFin"]
            
            # Buscar un salón disponible para este bloque
            salon_asignado = None
            for salon in salones_disponibles:
                # Crear una clave única para este bloque de tiempo y salón
                clave_bloque = f"{dia}_{hora_inicio}_{hora_fin}_{salon.id}"
                
                # Verificar si este bloque ya está ocupado
                if clave_bloque not in bloques_ocupados:
                    salon_asignado = salon
                    bloques_ocupados[clave_bloque] = True
                    break
            
            if not salon_asignado:
                # Si no se encontró un salón disponible, no se puede asignar este bloque
                # Eliminar los bloques ya creados y retornar None
                for bloque in bloques_creados:
                    self.bloque_repository.delete(bloque.id)
                return []
            
            # Crear el bloque
            nuevo_bloque = self.bloque_repository.create({
                "dia": dia,
                "horaInicio": hora_inicio,
                "horaFin": hora_fin,
                "salon_id": salon_asignado.id,
                "horario_id": horario_id
            })
            
            bloques_creados.append(nuevo_bloque)
        
        return bloques_creados

    def limpiar_horarios(self):
        """
        Limpia todos los horarios, bloques y cursos generados.
        Útil para reiniciar el sistema antes de una nueva generación.
        
        Returns:
            Dict: Resultado de la operación
        """
        try:
            # Obtener todos los cursos, horarios y bloques
            cursos = self.curso_repository.get_all()
            horarios = self.horario_repository.get_all()
            bloques = self.bloque_repository.get_all()
            
            # Eliminar cursos
            for curso in cursos:
                self.curso_repository.delete(curso.id)
            
            # Eliminar bloques
            for bloque in bloques:
                self.bloque_repository.delete(bloque.id)
            
            # Eliminar horarios
            for horario in horarios:
                self.horario_repository.delete(horario.id)
            
            return {
                "exito": True,
                "mensaje": "Todos los horarios, bloques y cursos han sido eliminados",
                "cursos_eliminados": len(cursos),
                "horarios_eliminados": len(horarios),
                "bloques_eliminados": len(bloques)
            }
            
        except Exception as e:
            return {
                "exito": False,
                "mensaje": f"Error al limpiar horarios: {str(e)}"
            }
    
