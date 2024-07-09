from ..models.citas import Receta
from .conexion import connect
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

def select_all_recetas():
    engine = connect()
    with Session(engine) as session:
        consulta = select(Receta)
        recetas = session.exec(consulta)
        return recetas.all()

def select_receta_by_id(id: int):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Receta).where(Receta.id == id)
        resultado = session.exec(consulta)
        return resultado.first()

def crear_receta(receta: Receta):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(receta)
            session.commit()
            session.refresh(receta)
            return receta
    except SQLAlchemyError as e:
        print(f"Error al crear receta: {e}")
        return None

def eliminar_receta(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            receta = session.get(Receta, id)
            if receta:
                session.delete(receta)
                session.commit()
                return True
            return False
    except SQLAlchemyError as e:
        print(f"Error al eliminar receta: {e}")
        return False

def actualizar_receta(id: int, datos_actualizacion: dict):
    engine = connect()
    try:
        with Session(engine) as session:
            receta = session.get(Receta, id)
            if receta:
                for key, value in datos_actualizacion.items():
                    setattr(receta, key, value)
                session.add(receta)
                session.commit()
                session.refresh(receta)
                return receta
            return None
    except SQLAlchemyError as e:
        print(f"Error al actualizar receta: {e}")
        return None