from ..models.citas import Diagnostico
from .conexion import connect
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

def select_all_diagnosticos():
    engine = connect()
    with Session(engine) as session:
        consulta = select(Diagnostico)
        diagnosticos = session.exec(consulta)
        return diagnosticos.all()

def select_diagnostico_by_id(id: int):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Diagnostico).where(Diagnostico.id == id)
        resultado = session.exec(consulta)
        return resultado.first()

def crear_diagnostico(diagnostico: Diagnostico):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(diagnostico)
            session.commit()
            session.refresh(diagnostico)
            return diagnostico
    except SQLAlchemyError as e:
        print(f"Error al crear diagnóstico: {e}")
        return None

def eliminar_diagnostico(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            diagnostico = session.get(Diagnostico, id)
            if diagnostico:
                session.delete(diagnostico)
                session.commit()
                return True
            return False
    except SQLAlchemyError as e:
        print(f"Error al eliminar diagnóstico: {e}")
        return False

def actualizar_diagnostico(id: int, datos_actualizacion: dict):
    engine = connect()
    try:
        with Session(engine) as session:
            diagnostico = session.get(Diagnostico, id)
            if diagnostico:
                for key, value in datos_actualizacion.items():
                    setattr(diagnostico, key, value)
                session.add(diagnostico)
                session.commit()
                session.refresh(diagnostico)
                return diagnostico
            return None
    except SQLAlchemyError as e:
        print(f"Error al actualizar diagnóstico: {e}")
        return None