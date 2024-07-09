from ..models.citas import Medicos
from .conexion import connect
from sqlmodel import SQLModel, Session, select
from sqlalchemy.exc import SQLAlchemyError

# Listar todos los médicos
def select_all_medicos():
    engine = connect()
    with Session(engine) as session:
        consulta = select(Medicos)
        medicos = session.exec(consulta)
        return medicos.all()

# Buscar médicos por número de licencia
def select_medico_by_licencia(licencia: str):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Medicos).where(Medicos.licencia_medica == licencia)
        resultado = session.exec(consulta)
        return resultado.all()

# Crear un nuevo médico
def crear_medico(medico: Medicos):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(medico)
            session.commit()
            session.refresh(medico)
            return medico
    except SQLAlchemyError as e:
        print(f"Error al crear médico: {e}")
        return None

# Eliminar un médico
def eliminar_medico(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            medico = session.get(Medicos, id)
            if medico:
                session.delete(medico)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(f"Error al eliminar médico: {e}")
        return False

# Actualizar un médico
def actualizar_medico(id: int, datos_actualizacion: dict):
    engine = connect()
    try:
        with Session(engine) as session:
            medico = session.get(Medicos, id)
            if medico:
                for key, value in datos_actualizacion.items():
                    setattr(medico, key, value)
                session.add(medico)
                session.commit()
                session.refresh(medico)
                return medico
            else:
                return None
    except SQLAlchemyError as e:
        print(f"Error al actualizar médico: {e}")
        return None