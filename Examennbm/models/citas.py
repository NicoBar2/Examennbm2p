import reflex as rx
from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel

class Persona(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombres: str = Field(index=True)
    apellidos: str
    cedula: str = Field(unique=True)
    correo: str = Field(unique=True)
    celular: str
    direccion: str
    hoja_vida: Optional['HojaVida'] = Relationship(back_populates="persona")

class Usuarios(rx.Model, table=True):
    username: str = Field(unique=True)
    password: str
    rol: str

class HojaVida(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    experiencia: str
    educacion: str
    habilidades: str
    persona_id: Optional[int] = Field(foreign_key="persona.id")
    persona: Optional['Persona'] = Relationship(back_populates="hoja_vida")

class Profesores(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    identificacion: str = Field(unique=True)
    nombres: str
    correo: str
    apellidos: str
    celular: str
    especialidades: List["Especialidad"] = Relationship(back_populates="profesor")
    evaluaciones: List["Evaluacion"] = Relationship(back_populates="profesor")
    tareas: List["Tarea"] = Relationship(back_populates="profesor")

class Estudiantes(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    grado: str
    notas_adicionales: str
    cedula: str
    nombres: str
    apellidos: str
    correo: str
    celular: str
    evaluaciones: List["Evaluacion"] = Relationship(back_populates="estudiante")
    tareas: List["Tarea"] = Relationship(back_populates="estudiante")

class Especialidad(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    descripcion: str
    profesores_id: Optional[int] = Field(foreign_key="profesores.id")
    profesor: Optional['Profesores'] = Relationship(back_populates="especialidades")

class Evaluacion(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: str
    descripcion: str
    profesor_id: Optional[int] = Field(foreign_key="profesores.id")
    estudiante_id: Optional[int] = Field(foreign_key="estudiantes.id")
    profesor: Optional['Profesores'] = Relationship(back_populates="evaluaciones")
    estudiante: Optional['Estudiantes'] = Relationship(back_populates="evaluaciones")
    tareas: List["Tarea"] = Relationship(back_populates="evaluacion")

class Tarea(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: str
    descripcion: str
    instrucciones: str
    profesor_id: Optional[int] = Field(foreign_key="profesores.id")
    estudiante_id: Optional[int] = Field(foreign_key="estudiantes.id")
    evaluacion_id: Optional[int] = Field(foreign_key="evaluacion.id")
    profesor: Optional['Profesores'] = Relationship(back_populates="tareas")
    estudiante: Optional['Estudiantes'] = Relationship(back_populates="tareas")
    evaluacion: Optional['Evaluacion'] = Relationship(back_populates="tareas")