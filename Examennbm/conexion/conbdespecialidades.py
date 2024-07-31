from ..models.citas import Especialidad
from .conexion import connect
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

def select_all_especialidades():
    print("Estoy en el repositorio")
    engine = connect()
    with Session(engine) as session:
        consulta = select(Especialidad)
        especialidades = session.exec(consulta)
        return especialidades.all()

def select_especialidad_by_nombre(nombre: str):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Especialidad).where(Especialidad.nombre == nombre)
        resultado = session.exec(consulta)
        return resultado.first()

def crear_especialidad(especialidad: Especialidad):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(especialidad)
            session.commit()
            session.refresh(especialidad)
            return especialidad
    except SQLAlchemyError as e:
        print(f"Error al crear especialidad: {e}")
        return None

def eliminar_especialidad(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            especialidad = session.get(Especialidad, id)
            if especialidad:
                session.delete(especialidad)
                session.commit()
                return True
            return False
    except SQLAlchemyError as e:
        print(f"Error al eliminar especialidad: {e}")
        return False

def actualizar_especialidad(id: int, datos_actualizacion: dict):
    engine = connect()
    try:
        with Session(engine) as session:
            especialidad = session.get(Especialidad, id)
            if especialidad:
                for key, value in datos_actualizacion.items():
                    setattr(especialidad, key, value)
                session.add(especialidad)
                session.commit()
                session.refresh(especialidad)
                return especialidad
            return None
    except SQLAlchemyError as e:
        print(f"Error al actualizar especialidad: {e}")
        return None