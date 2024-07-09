from ..models.citas import Usuarios
from .conexion import connect
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

def select_all_usuarios():
    engine = connect()
    with Session(engine) as session:
        consulta = select(Usuarios)
        usuarios = session.exec(consulta)
        return usuarios.all()

def select_usuario_by_username(username: str):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Usuarios).where(Usuarios.username == username)
        resultado = session.exec(consulta)
        return resultado.first()

def crear_usuario(usuario: Usuarios):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(usuario)
            session.commit()
            session.refresh(usuario)
            return usuario
    except SQLAlchemyError as e:
        print(f"Error al crear usuario: {e}")
        return None

def eliminar_usuario(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            usuario = session.get(Usuarios, id)
            if usuario:
                session.delete(usuario)
                session.commit()
                return True
            return False
    except SQLAlchemyError as e:
        print(f"Error al eliminar usuario: {e}")
        return False

def actualizar_usuario(id: int, datos_actualizacion: dict):
    engine = connect()
    try:
        with Session(engine) as session:
            usuario = session.get(Usuarios, id)
            if usuario:
                for key, value in datos_actualizacion.items():
                    setattr(usuario, key, value)
                session.add(usuario)
                session.commit()
                session.refresh(usuario)
                return usuario
            return None
    except SQLAlchemyError as e:
        print(f"Error al actualizar usuario: {e}")
        return None