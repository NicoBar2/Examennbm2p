from ..models.citas import Medicos
from ..conexion.conbdmedicos import (select_all_medicos,
                               select_medico_by_licencia,
                               crear_medico,
                               eliminar_medico,
                               actualizar_medico)

def servicio_medicos_all():
    medicos = select_all_medicos()
    print(medicos)
    return medicos

def servicio_consultar_medico(licencia: str):
    if len(licencia) != 0:
        medico = select_medico_by_licencia(licencia)
        print(medico)
        return medico
    else:
        return select_all_medicos()

def servicio_crear_medico(licencia_medica: str, nombres: str, apellidos: str, cedula: str, 
                          correo: str, celular: str, direccion: str):
    medico_existente = servicio_consultar_medico(licencia_medica)
    if not medico_existente:
        nuevo_medico = Medicos(licencia_medica=licencia_medica, nombres=nombres, apellidos=apellidos,
                               cedula=cedula, correo=correo, celular=celular, direccion=direccion)
        return crear_medico(nuevo_medico)
    else:
        return "El médico ya existe"

def servicio_eliminar_medico(id: int):
    return eliminar_medico(id)

def servicio_actualizar_medico(id: int, datos_actualizacion: dict):
    return actualizar_medico(id, datos_actualizacion)