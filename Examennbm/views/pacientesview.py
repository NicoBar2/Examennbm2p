import reflex as rx
from ..models.citas import Pacientes
from ..servicios.pacienteservice import *
from Examennbm.templates import template

class PacienteState(rx.State):
    pacientes: list[Pacientes]
    buscar_cedula: str = ""

    rx.background
    def get_todos_pacientes(self):
        self.pacientes = servicio_pacientes_all()

    rx.background
    def get_paciente_cedula(self):
        self.pacientes = servicio_consultar_paciente(self.buscar_cedula)

    def buscar_onchange(self, value: str):
        self.buscar_cedula = value

    rx.background
    def crear_paciente(self, data: dict):
        try:
            self.pacientes = servicio_crear_paciente(
                data['nombres'], data['apellidos'], data['cedula'],
                data['correo'], data['celular'], data['direccion'],
                data['grupo_sanguineo'], data['alergias']
            )
        except Exception as e:
            print(e)

@template(route="/pacientes", title="Lista de Pacientes", on_load=PacienteState.get_todos_pacientes)
def paciente_page() -> rx.Component:
    return rx.flex(
        rx.heading("Pacientes", title="Pacientes", size="5", center=True),
        rx.vstack(
            buscar_paciente_cedula(),
            dialog_paciente_form(),
            tabla_pacientes(PacienteState.pacientes),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

def tabla_pacientes(lista_pacientes: list[Pacientes]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Cédula"),
                rx.table.column_header_cell("Nombres"),
                rx.table.column_header_cell("Apellidos"),
                rx.table.column_header_cell("Correo"),
                rx.table.column_header_cell("Celular"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_pacientes, row_table)
        ),
    )

def row_table(paciente: Pacientes) -> rx.Component:
    return rx.table.row(
        rx.table.cell(paciente.cedula),
        rx.table.cell(paciente.nombres),
        rx.table.cell(paciente.apellidos),
        rx.table.cell(paciente.correo),
        rx.table.cell(paciente.celular),
        rx.table.cell(
            rx.hstack(
                rx.button("Editar", variant="outline"),
                rx.button("Eliminar", variant="outline"),
            )
        ),
    )

def buscar_paciente_cedula() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Cédula", on_change=PacienteState.buscar_onchange),
        rx.button("Buscar paciente", on_click=PacienteState.get_paciente_cedula)
    )

def dialog_paciente_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear paciente", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear paciente"),
                crear_paciente_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancelar", variant="soft", color_scheme="red"),
                ),
                spacing="2",
                justify="end",
                margin_top="10px",
            ),
            style={"width": "400px"},
        ),
    )

def crear_paciente_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="Cédula", name="cedula"),
            rx.input(placeholder="Nombres", name="nombres"),
            rx.input(placeholder="Apellidos", name="apellidos"),
            rx.input(placeholder="Correo electrónico", name="correo"),
            rx.input(placeholder="# celular", name="celular"),
            rx.input(placeholder="Dirección", name="direccion"),
            rx.input(placeholder="Grupo sanguíneo", name="grupo_sanguineo"),
            rx.input(placeholder="Alergias", name="alergias"),
            rx.dialog.close(
                rx.button("Crear paciente", type="submit"),
            ),
        ),
        on_submit=PacienteState.crear_paciente,
    )