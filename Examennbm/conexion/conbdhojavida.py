from ..models.citas import HojaVida
from .conexion import connect
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

def select_all_hojas_vida():
    engine = connect()
    with Session(engine) as session:
        consulta = select(HojaVida)
        hojas_vida = session.exec(consulta)
        return hojas_vida.all()

def select_hoja_vida_by_persona_id(persona_id: int):
    engine = connect()
    with Session(engine) as session:
        consulta = select(HojaVida).where(HojaVida.persona_id == persona_id)
        resultado = session.exec(consulta)
        return resultado.first()

def crear_hoja_vida(hoja_vida: HojaVida):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(hoja_vida)
            session.commit()
            session.refresh(hoja_vida)
            return hoja_vida
    except SQLAlchemyError as e:
        print(f"Error al crear hoja de vida: {e}")
        return None

def eliminar_hoja_vida(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            hoja_vida = session.get(HojaVida, id)
            if hoja_vida:
                session.delete(hoja_vida)
                session.commit()
                return True
            return False
    except SQLAlchemyError as e:
        print(f"Error al eliminar hoja de vida: {e}")
        return False

def actualizar_hoja_vida(id: int, datos_actualizacion: dict):
    engine = connect()
    try:
        with Session(engine) as session:
            hoja_vida = session.get(HojaVida, id)
            if hoja_vida:
                for key, value in datos_actualizacion.items():
                    setattr(hoja_vida, key, value)
                session.add(hoja_vida)
                session.commit()
                session.refresh(hoja_vida)
                return hoja_vida
            return None
    except SQLAlchemyError as e:
        print(f"Error al actualizar hoja de vida: {e}")
        return None