from sqlmodel import create_engine,SQLModel


def connect():
    usuario = "root"
    clave = ""
    host = "localhost"
    puerto = "3306"
    engine = create_engine(f"mysql+pymysql://{usuario}:{clave}@{host}:3306/exam")
    SQLModel.metadata.create_all(engine)
    return engine