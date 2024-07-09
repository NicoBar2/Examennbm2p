from ..models.citas import Diagnostico
from ..conexion.conbddiagnostico import (select_all_diagnosticos,
                                   select_diagnostico_by_id,
                                   crear_diagnostico,
                                   eliminar_diagnostico,
                                   actualizar_diagnostico)

def servicio_diagnosticos_all():
    diagnosticos = select_all_diagnosticos()
    print(diagnosticos)
    return diagnosticos

def servicio_consultar_diagnostico(id: int):
    if id:
        diagnostico = select_diagnostico_by_id(id)
        print(diagnostico)
        return diagnostico
    else:
        return select_all_diagnosticos()

def servicio_crear_diagnostico(fecha: str, descripcion: str, medico_id: int, paciente_id: int):
    nuevo_diagnostico = Diagnostico(fecha=fecha, descripcion=descripcion,
                                    medico_id=medico_id, paciente_id=paciente_id)
    return crear_diagnostico(nuevo_diagnostico)

def servicio_eliminar_diagnostico(id: int):
    return eliminar_diagnostico(id)

def servicio_actualizar_diagnostico(id: int, datos_actualizacion: dict):
    return actualizar_diagnostico(id, datos_actualizacion)