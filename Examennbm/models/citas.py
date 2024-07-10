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

class Medicos(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    licencia_medica: str = Field(unique=True)
    nombres: str
    apellidos: str
    correo: str
    celular: str
    especialidades: List["Especialidad"] = Relationship(back_populates="medico")
    diagnosticos: List["Diagnostico"] = Relationship(back_populates="medico")
    recetas: List["Receta"] = Relationship(back_populates="medico")

class Pacientes(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    grupo_sanguineo: str
    alergias: str
    cedula: str
    nombres: str
    apellidos: str
    correo: str
    celular: str
    diagnosticos: List["Diagnostico"] = Relationship(back_populates="paciente")
    recetas: List["Receta"] = Relationship(back_populates="paciente")

class Especialidad(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    descripcion: str
    medicos_id: Optional[int] = Field(foreign_key="medicos.id")
    medico: Optional['Medicos'] = Relationship(back_populates="especialidades")

class Diagnostico(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: str
    descripcion: str
    medico_id: Optional[int] = Field(foreign_key="medicos.id")
    paciente_id: Optional[int] = Field(foreign_key="pacientes.id")
    medico: Optional['Medicos'] = Relationship(back_populates="diagnosticos")
    paciente: Optional['Pacientes'] = Relationship(back_populates="diagnosticos")
    recetas: List["Receta"] = Relationship(back_populates="diagnostico")

class Receta(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: str
    medicamentos: str
    indicaciones: str
    medico_id: Optional[int] = Field(foreign_key="medicos.id")
    paciente_id: Optional[int] = Field(foreign_key="pacientes.id")
    diagnostico_id: Optional[int] = Field(foreign_key="diagnostico.id")
    medico: Optional['Medicos'] = Relationship(back_populates="recetas")
    paciente: Optional['Pacientes'] = Relationship(back_populates="recetas")
    diagnostico: Optional['Diagnostico'] = Relationship(back_populates="recetas")