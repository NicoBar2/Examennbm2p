from sqlmodel import create_engine,SQLModel


def connect():
    clave= ""
    engine = create_engine(f"mysql+pymysql://root:{clave}@localhost:3306/exam")
    SQLModel.metadata.create_all(engine)
    return engine