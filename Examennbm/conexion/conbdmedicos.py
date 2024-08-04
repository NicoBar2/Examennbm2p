from ..models.citas import Profesores
from .conexion import connect
from sqlmodel import SQLModel, Session, select
from sqlalchemy.exc import SQLAlchemyError

# Listar todos los profesores
def select_all_profesores():
    engine = connect()
    with Session(engine) as session:
        consulta = select(Profesores)
        profesores = session.exec(consulta)
        return profesores.all()

# Buscar profesores por número de identificación
def select_profesor_by_identificacion(identificacion: str):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Profesores).where(Profesores.identificacion == identificacion)
        resultado = session.exec(consulta)
        return resultado.all()

# Crear un nuevo profesor
def crear_profesor(profesor: Profesores):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(profesor)
            session.commit()
            session.refresh(profesor)
            return profesor
    except SQLAlchemyError as e:
        print(f"Error al crear profesor: {e}")
        return None

# Eliminar un profesor
def eliminar_profesor(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            profesor = session.get(Profesores, id)
            if profesor:
                session.delete(profesor)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(f"Error al eliminar profesor: {e}")
        return False

# Actualizar un profesor
def actualizar_profesor(id: int, datos_actualizacion: dict):
    engine = connect()
    try:
        with Session(engine) as session:
            profesor = session.get(Profesores, id)
            if profesor:
                for key, value in datos_actualizacion.items():
                    setattr(profesor, key, value)
                session.add(profesor)
                session.commit()
                session.refresh(profesor)
                return profesor
            else:
                return None
    except SQLAlchemyError as e:
        print(f"Error al actualizar profesor: {e}")
        return None