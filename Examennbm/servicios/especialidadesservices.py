from ..models.citas import Especialidad
from ..conexion.conbdespecialidades import (select_all_especialidades,
                                      select_especialidad_by_nombre,
                                      crear_especialidad,
                                      eliminar_especialidad,
                                      actualizar_especialidad)

def servicio_especialidades_all():
    print("Estoy en el servicio")
    especialidades = select_all_especialidades()
    return especialidades

def servicio_consultar_especialidad(nombre: str):
    if len(nombre) != 0:
        especialidad = select_especialidad_by_nombre(nombre)
        print(especialidad)
        return especialidad
    else:
        return select_all_especialidades()

def servicio_crear_especialidad(nombre: str, descripcion: str):
    especialidad_existente = servicio_consultar_especialidad(nombre)
    if not especialidad_existente:
        nueva_especialidad = Especialidad(nombre=nombre, descripcion=descripcion)
        return crear_especialidad(nueva_especialidad)
    else:
        return "La especialidad ya existe"

def servicio_eliminar_especialidad(id: int):
    return eliminar_especialidad(id)

def servicio_actualizar_especialidad(id: int, datos_actualizacion: dict):
    return actualizar_especialidad(id, datos_actualizacion)