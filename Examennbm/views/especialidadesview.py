import reflex as rx
from ..models.citas import Especialidad
from ..servicios.especialidadesservices import *
from Examennbm.templates import template

class EspecialidadState(rx.State):
    especialidades: list[Especialidad]
    buscar_nombre: str = ""

    rx.background
    def get_todas_especialidades(self):
        self.especialidades = servicio_especialidades_all()

    rx.background
    def get_especialidad_nombre(self):
        self.especialidades = servicio_consultar_especialidad(self.buscar_nombre)

    def buscar_onchange(self, value: str):
        self.buscar_nombre = value

    rx.background
    def crear_especialidad(self, data: dict):
        try:
            self.especialidades = servicio_crear_especialidad(
                data['nombre'], data['descripcion']
            )
        except Exception as e:
            print(e)

@template(route="/especialidades", title="Lista de Especialidades", on_load=EspecialidadState.get_todas_especialidades)
def especialidad_page() -> rx.Component:
    return rx.flex(
        rx.heading("Especialidades", title="Especialidades", size="5", center=True),
        rx.vstack(
            buscar_especialidad_nombre(),
            dialog_especialidad_form(),
            tabla_especialidades(EspecialidadState.especialidades),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

def tabla_especialidades(lista_especialidades: list[Especialidad]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Nombre"),
                rx.table.column_header_cell("Descripción"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_especialidades, row_table)
        ),
    )

def row_table(especialidad: Especialidad) -> rx.Component:
    return rx.table.row(
        rx.table.cell(especialidad.nombre),
        rx.table.cell(especialidad.descripcion),
        rx.table.cell(
            rx.hstack(
                rx.button("Editar", variant="outline"),
                rx.button("Eliminar", variant="outline"),
            )
        ),
    )

def buscar_especialidad_nombre() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Nombre", on_change=EspecialidadState.buscar_onchange),
        rx.button("Buscar especialidad", on_click=EspecialidadState.get_especialidad_nombre)
    )

def dialog_especialidad_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear especialidad", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear especialidad"),
                crear_especialidad_form(),
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

def crear_especialidad_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="Nombre", name="nombre"),
            rx.input(placeholder="Descripción", name="descripcion"),
            rx.dialog.close(
                rx.button("Crear especialidad", type="submit"),
            ),
        ),
        on_submit=EspecialidadState.crear_especialidad,
    )