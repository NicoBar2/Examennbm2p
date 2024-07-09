from ..models.citas import Pacientes
from ..conexion.conbdpacientes import (select_all_pacientes,
                                 select_paciente_by_cedula,
                                 crear_paciente,
                                 eliminar_paciente,
                                 actualizar_paciente)

def servicio_pacientes_all():
    pacientes = select_all_pacientes()
    print(pacientes)
    return pacientes

def servicio_consultar_paciente(cedula: str):
    if len(cedula) != 0:
        paciente = select_paciente_by_cedula(cedula)
        print(paciente)
        return paciente
    else:
        return select_all_pacientes()

def servicio_crear_paciente(nombres: str, apellidos: str, cedula: str, correo: str, 
                            celular: str, direccion: str, grupo_sanguineo: str, alergias: str):
    paciente_existente = servicio_consultar_paciente(cedula)
    if not paciente_existente:
        nuevo_paciente = Pacientes(nombres=nombres, apellidos=apellidos, cedula=cedula,
                                   correo=correo, celular=celular, direccion=direccion,
                                   grupo_sanguineo=grupo_sanguineo, alergias=alergias)
        return crear_paciente(nuevo_paciente)
    else:
        return "El paciente ya existe"

def servicio_eliminar_paciente(id: int):
    return eliminar_paciente(id)

def servicio_actualizar_paciente(id: int, datos_actualizacion: dict):
    return actualizar_paciente(id, datos_actualizacion)