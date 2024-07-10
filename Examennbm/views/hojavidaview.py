import reflex as rx
from ..models.citas import HojaVida
from ..servicios.hojavidaservice import *
from Examennbm.templates import template

class HojaVidaState(rx.State):
    hojas_vida: list[HojaVida]
    buscar_persona_id: int = 0

    rx.background
    def get_todas_hojas_vida(self):
        self.hojas_vida = servicio_hojas_vida_all()

    rx.background
    def get_hoja_vida_persona(self):
        self.hojas_vida = servicio_consultar_hoja_vida(self.buscar_persona_id)

    def buscar_onchange(self, value: str):
        self.buscar_persona_id = int(value) if value.isdigit() else 0

    rx.background
    def crear_hoja_vida(self, data: dict):
        try:
            self.hojas_vida = servicio_crear_hoja_vida(
                int(data['persona_id']),
                data['experiencia'],
                data['educacion'],
                data['habilidades']
            )
        except Exception as e:
            print(e)

@template(route="/hojas_vida", title="Hojas de Vida", on_load=HojaVidaState.get_todas_hojas_vida)
def hoja_vida_page() -> rx.Component:
    return rx.flex(
        rx.heading("Hojas de Vida", title="Hojas de Vida", size="5", center=True),
        rx.vstack(
            buscar_hoja_vida_persona(),
            dialog_hoja_vida_form(),
            tabla_hojas_vida(HojaVidaState.hojas_vida),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

def tabla_hojas_vida(lista_hojas_vida: list[HojaVida]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Persona ID"),
                rx.table.column_header_cell("Experiencia"),
                rx.table.column_header_cell("Educación"),
                rx.table.column_header_cell("Habilidades"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_hojas_vida, row_table)
        ),
    )

def row_table(hoja_vida: HojaVida) -> rx.Component:
    return rx.table.row(
        rx.table.cell(hoja_vida.id),
        rx.table.cell(hoja_vida.persona_id),
        rx.table.cell(hoja_vida.experiencia),
        rx.table.cell(hoja_vida.educacion),
        rx.table.cell(hoja_vida.habilidades),
        rx.table.cell(
            rx.hstack(
                rx.button("Editar", variant="outline"),
                rx.button("Eliminar", variant="outline"),
            )
        ),
    )

def buscar_hoja_vida_persona() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="ID de la Persona", on_change=HojaVidaState.buscar_onchange),
        rx.button("Buscar Hoja de Vida", on_click=HojaVidaState.get_hoja_vida_persona)
    )

def dialog_hoja_vida_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear Hoja de Vida", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Hoja de Vida"),
                crear_hoja_vida_form(),
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

def crear_hoja_vida_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="ID de la Persona", name="persona_id", type="number"),
            rx.input(placeholder="Experiencia", name="experiencia"),
            rx.input(placeholder="Educación", name="educacion"),
            rx.input(placeholder="Habilidades", name="habilidades"),
            rx.dialog.close(
                rx.button("Crear Hoja de Vida", type="submit"),
            ),
        ),
        on_submit=HojaVidaState.crear_hoja_vida,
    )