from ..models.citas import Usuarios
from ..conexion.conbdusuarios import (select_all_usuarios,
                                select_usuario_by_username,
                                crear_usuario,
                                eliminar_usuario,
                                actualizar_usuario)

def servicio_usuarios_all():
    usuarios = select_all_usuarios()
    print(usuarios)
    return usuarios

def servicio_consultar_usuario(username: str):
    if len(username) != 0:
        usuario = select_usuario_by_username(username)
        print(usuario)
        return usuario
    else:
        return select_all_usuarios()

def servicio_crear_usuario(username: str, password: str, rol: str, nombres: str, 
                           apellidos: str, cedula: str, correo: str, celular: str, direccion: str):
    usuario_existente = servicio_consultar_usuario(username)
    if not usuario_existente:
        nuevo_usuario = Usuarios(username=username, password=password, rol=rol, nombres=nombres,
                                 apellidos=apellidos, cedula=cedula, correo=correo, celular=celular, direccion=direccion)
        return crear_usuario(nuevo_usuario)
    else:
        return "El usuario ya existe"

def servicio_eliminar_usuario(id: int):
    return eliminar_usuario(id)

def servicio_actualizar_usuario(id: int, datos_actualizacion: dict):
    return actualizar_usuario(id, datos_actualizacion)