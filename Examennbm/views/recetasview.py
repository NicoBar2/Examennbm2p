import reflex as rx
from ..models.citas import Receta
from ..servicios.recetasservice import *

class RecetaState(rx.State):
    recetas: list[Receta]
    buscar_id: int = 0

    rx.background
    def get_todas_recetas(self):
        self.recetas = servicio_recetas_all()

    rx.background
    def get_receta_id(self):
        self.recetas = servicio_consultar_receta(self.buscar_id)

    def buscar_onchange(self, value: str):
        self.buscar_id = int(value) if value.isdigit() else 0

    rx.background
    def crear_receta(self, data: dict):
        try:
            self.recetas = servicio_crear_receta(
                data['fecha'], data['medicamentos'], data['indicaciones'],
                int(data['medico_id']), int(data['paciente_id']), int(data['diagnostico_id'])
            )
        except Exception as e:
            print(e)

@rx.page(route="/recetas", title="Lista de Recetas", on_load=RecetaState.get_todas_recetas)
def receta_page() -> rx.Component:
    return rx.flex(
        rx.heading("Recetas", title="Recetas", size="5", center=True),
        rx.vstack(
            buscar_receta_id(),
            dialog_receta_form(),
            tabla_recetas(RecetaState.recetas),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

def tabla_recetas(lista_recetas: list[Receta]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Fecha"),
                rx.table.column_header_cell("Medicamentos"),
                rx.table.column_header_cell("Indicaciones"),
                rx.table.column_header_cell("Médico ID"),
                rx.table.column_header_cell("Paciente ID"),
                rx.table.column_header_cell("Diagnóstico ID"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_recetas, row_table)
        ),
    )

def row_table(receta: Receta) -> rx.Component:
    return rx.table.row(
        rx.table.cell(receta.id),
        rx.table.cell(receta.fecha),
        rx.table.cell(receta.medicamentos),
        rx.table.cell(receta.indicaciones),
        rx.table.cell(receta.medico_id),
        rx.table.cell(receta.paciente_id),
        rx.table.cell(receta.diagnostico_id),
        rx.table.cell(
            rx.hstack(
                rx.button("Editar", variant="outline"),
                rx.button("Eliminar", variant="outline"),
            )
        ),
    )

def buscar_receta_id() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="ID", on_change=RecetaState.buscar_onchange),
        rx.button("Buscar receta", on_click=RecetaState.get_receta_id)
    )

def dialog_receta_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear receta", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear receta"),
                crear_receta_form(),
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

def crear_receta_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="Fecha", name="fecha", type="date"),
            rx.input(placeholder="Medicamentos", name="medicamentos"),
            rx.input(placeholder="Indicaciones", name="indicaciones"),
            rx.input(placeholder="ID del Médico", name="medico_id", type="number"),
            rx.input(placeholder="ID del Paciente", name="paciente_id", type="number"),
            rx.input(placeholder="ID del Diagnóstico", name="diagnostico_id", type="number"),
            rx.dialog.close(
                rx.button("Crear receta", type="submit"),
            ),
        ),
        on_submit=RecetaState.crear_receta,
    )