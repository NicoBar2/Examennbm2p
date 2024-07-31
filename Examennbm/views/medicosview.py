import reflex as rx
from ..models.citas import Medicos
from ..servicios.medicosservice import *
from Examennbm.templates import template

class MedicoState(rx.State):
    medicos: list[Medicos]
    buscar_licencia: str = ""

    @rx.background
    async def get_todos_medicos(self):
        async with self:
          self.medicos = servicio_medicos_all()

    @rx.background
    async def get_medico_licencia(self):
        async with self:
          self.medicos = servicio_consultar_medico(self.buscar_licencia)

    def buscar_onchange(self, value: str):
        self.buscar_licencia = value

    @rx.background
    async def crear_medico(self, data: dict):
        async with self:
          try:
            self.medicos = servicio_crear_medico(
                data['licencia_medica'], data['nombres'],
                data['apellidos'], data['cedula'],
                data['correo'], data['celular'],
                data['direccion']
            )
          except Exception as e:
            print(e)

@template(route="/medicos", title="Lista de Médicos", on_load=MedicoState.get_todos_medicos)
def medico_page() -> rx.Component:
    return rx.flex(
        rx.heading("Médicos", title="Médicos", size="5", center=True),
        rx.vstack(
            buscar_medico_licencia(),
            dialog_medico_form(),
            tabla_medicos(MedicoState.medicos),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

def tabla_medicos(lista_medicos: list[Medicos]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Licencia"),
                rx.table.column_header_cell("Nombres"),
                rx.table.column_header_cell("Apellidos"),
                rx.table.column_header_cell("Correo"),
                rx.table.column_header_cell("Celular"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_medicos, row_table)
        ),
    )

def row_table(medico: Medicos) -> rx.Component:
    return rx.table.row(
        rx.table.cell(medico.licencia_medica),
        rx.table.cell(medico.nombres),
        rx.table.cell(medico.apellidos),
        rx.table.cell(medico.correo),
        rx.table.cell(medico.celular),
        rx.table.cell(
            rx.hstack(
                rx.button("Editar", variant="outline"),
                rx.button("Eliminar", variant="outline"),
            )
        ),
    )

def buscar_medico_licencia() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Licencia", on_change=MedicoState.buscar_onchange),
        rx.button("Buscar médico", on_click=MedicoState.get_medico_licencia)
    )

def dialog_medico_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear médico", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear médico"),
                crear_medico_form(),
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

def crear_medico_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="Licencia médica", name="licencia_medica"),
            rx.input(placeholder="Nombres", name="nombres"),
            rx.input(placeholder="Apellidos", name="apellidos"),
            rx.input(placeholder="Cédula", name="cedula"),
            rx.input(placeholder="Correo electrónico", name="correo"),
            rx.input(placeholder="# celular", name="celular"),
            rx.input(placeholder="Dirección", name="direccion"),
            rx.dialog.close(
                rx.button("Crear médico", type="submit"),
            ),
        ),
        on_submit=MedicoState.crear_medico,
    )