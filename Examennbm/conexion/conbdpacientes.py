from ..models.citas import Pacientes
from .conexion import connect
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

def select_all_pacientes():
    engine = connect()
    with Session(engine) as session:
        consulta = select(Pacientes)
        pacientes = session.exec(consulta)
        return pacientes.all()

def select_paciente_by_cedula(cedula: str):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Pacientes).where(Pacientes.cedula == cedula)
        resultado = session.exec(consulta)
        return resultado.first()

def crear_paciente(paciente: Pacientes):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(paciente)
            session.commit()
            session.refresh(paciente)
            return paciente
    except SQLAlchemyError as e:
        print(f"Error al crear paciente: {e}")
        return None

def eliminar_paciente(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            paciente = session.get(Pacientes, id)
            if paciente:
                session.delete(paciente)
                session.commit()
                return True
            return False
    except SQLAlchemyError as e:
        print(f"Error al eliminar paciente: {e}")
        return False

def actualizar_paciente(id: int, datos_actualizacion: dict):
    engine = connect()
    try:
        with Session(engine) as session:
            paciente = session.get(Pacientes, id)
            if paciente:
                for key, value in datos_actualizacion.items():
                    setattr(paciente, key, value)
                session.add(paciente)
                session.commit()
                session.refresh(paciente)
                return paciente
            return None
    except SQLAlchemyError as e:
        print(f"Error al actualizar paciente: {e}")
        return None