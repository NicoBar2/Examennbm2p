import reflex as rx
from ..models.citas import Diagnostico
from ..servicios.diagnosticoservice import *
from Examennbm.templates import template

class DiagnosticoState(rx.State):
    diagnosticos: list[Diagnostico]
    buscar_id: int = 0

    rx.background
    def get_todos_diagnosticos(self):
        self.diagnosticos = servicio_diagnosticos_all()

    rx.background
    def get_diagnostico_id(self):
        self.diagnosticos = servicio_consultar_diagnostico(self.buscar_id)

    def buscar_onchange(self, value: str):
        self.buscar_id = int(value) if value.isdigit() else 0

    rx.background
    def crear_diagnostico(self, data: dict):
        try:
            self.diagnosticos = servicio_crear_diagnostico(
                data['fecha'], data['descripcion'],
                int(data['medico_id']), int(data['paciente_id'])
            )
        except Exception as e:
            print(e)

@template(route="/diagnosticos", title="Lista de Diagnósticos", on_load=DiagnosticoState.get_todos_diagnosticos)
def diagnostico_page() -> rx.Component:
    return rx.flex(
        rx.heading("Diagnósticos", title="Diagnósticos", size="5", center=True),
        rx.vstack(
            buscar_diagnostico_id(),
            dialog_diagnostico_form(),
            tabla_diagnosticos(DiagnosticoState.diagnosticos),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

def tabla_diagnosticos(lista_diagnosticos: list[Diagnostico]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Fecha"),
                rx.table.column_header_cell("Descripción"),
                rx.table.column_header_cell("Médico ID"),
                rx.table.column_header_cell("Paciente ID"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_diagnosticos, row_table)
        ),
    )

def row_table(diagnostico: Diagnostico) -> rx.Component:
    return rx.table.row(
        rx.table.cell(diagnostico.id),
        rx.table.cell(diagnostico.fecha),
        rx.table.cell(diagnostico.descripcion),
        rx.table.cell(diagnostico.medico_id),
        rx.table.cell(diagnostico.paciente_id),
        rx.table.cell(
            rx.hstack(
                rx.button("Editar", variant="outline"),
                rx.button("Eliminar", variant="outline"),
            )
        ),
    )

def buscar_diagnostico_id() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="ID", on_change=DiagnosticoState.buscar_onchange),
        rx.button("Buscar diagnóstico", on_click=DiagnosticoState.get_diagnostico_id)
    )

def dialog_diagnostico_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear diagnóstico", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear diagnóstico"),
                crear_diagnostico_form(),
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

def crear_diagnostico_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="Fecha", name="fecha", type="date"),
            rx.input(placeholder="Descripción", name="descripcion"),
            rx.input(placeholder="ID del Médico", name="medico_id", type="number"),
            rx.input(placeholder="ID del Paciente", name="paciente_id", type="number"),
            rx.dialog.close(
                rx.button("Crear diagnóstico", type="submit"),
            ),
        ),
        on_submit=DiagnosticoState.crear_diagnostico,
    )