import reflex as rx
from ..models.citas import Profesores
from ..servicios.profesoresservice import *
from Examennbm.templates import template

class ProfesorState(rx.State):
    profesores: list[Profesores]
    buscar_identificacion: str = ""

    @rx.background
    async def get_todos_profesores(self):
        async with self:
          self.profesores = servicio_profesores_all()

    @rx.background
    async def get_profesor_identificacion(self):
        async with self:
          self.profesores = servicio_consultar_profesor(self.buscar_identificacion)

    def buscar_onchange(self, value: str):
        self.buscar_identificacion = value

    @rx.background
    async def crear_profesor(self, data: dict):
        async with self:
          try:
            self.profesores = servicio_crear_profesor(
                data['identificacion'], data['nombres'],
                data['apellidos'], data['cedula'],
                data['correo'], data['celular'],
                data['direccion']
            )
          except Exception as e:
            print(e)

@template(route="/profesores", title="Lista de Profesores", on_load=ProfesorState.get_todos_profesores)
def profesor_page() -> rx.Component:
    return rx.flex(
        rx.heading("Profesores", title="Profesores", size="5", center=True),
        rx.vstack(
            buscar_profesor_identificacion(),
            dialog_profesor_form(),
            tabla_profesores(ProfesorState.profesores),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

def tabla_profesores(lista_profesores: list[Profesores]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Identificación"),
                rx.table.column_header_cell("Nombres"),
                rx.table.column_header_cell("Apellidos"),
                rx.table.column_header_cell("Correo"),
                rx.table.column_header_cell("Celular"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_profesores, row_table)
        ),
    )

def row_table(profesor: Profesores) -> rx.Component:
    return rx.table.row(
        rx.table.cell(profesor.identificacion),
        rx.table.cell(profesor.nombres),
        rx.table.cell(profesor.apellidos),
        rx.table.cell(profesor.correo),
        rx.table.cell(profesor.celular),
        rx.table.cell(
            rx.hstack(
                rx.button("Editar", variant="outline"),
                rx.button("Eliminar", variant="outline"),
            )
        ),
    )

def buscar_profesor_identificacion() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Identificación", on_change=ProfesorState.buscar_onchange),
        rx.button("Buscar profesor", on_click=ProfesorState.get_profesor_identificacion)
    )

def dialog_profesor_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear profesor", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear profesor"),
                crear_profesor_form(),
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

def crear_profesor_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="Identificación", name="identificacion"),
            rx.input(placeholder="Nombres", name="nombres"),
            rx.input(placeholder="Apellidos", name="apellidos"),
            rx.input(placeholder="Cédula", name="cedula"),
            rx.input(placeholder="Correo electrónico", name="correo"),
            rx.input(placeholder="# celular", name="celular"),
            rx.input(placeholder="Dirección", name="direccion"),
            rx.dialog.close(
                rx.button("Crear profesor", type="submit"),
            ),
        ),
        on_submit=ProfesorState.crear_profesor,
    )