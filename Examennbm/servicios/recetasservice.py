from ..models.citas import Receta
from ..conexion.conbdrecetas import (select_all_recetas,
                              select_receta_by_id,
                              crear_receta,
                              eliminar_receta,
                              actualizar_receta)

def servicio_recetas_all():
    recetas = select_all_recetas()
    print(recetas)
    return recetas

def servicio_consultar_receta(id: int):
    if id:
        receta = select_receta_by_id(id)
        print(receta)
        return receta
    else:
        return select_all_recetas()

def servicio_crear_receta(fecha: str, medicamentos: str, indicaciones: str, 
                          medico_id: int, paciente_id: int, diagnostico_id: int):
    nueva_receta = Receta(fecha=fecha, medicamentos=medicamentos, indicaciones=indicaciones,
                          medico_id=medico_id, paciente_id=paciente_id, diagnostico_id=diagnostico_id)
    return crear_receta(nueva_receta)

def servicio_eliminar_receta(id: int):
    return eliminar_receta(id)

def servicio_actualizar_receta(id: int, datos_actualizacion: dict):
    return actualizar_receta(id, datos_actualizacion)