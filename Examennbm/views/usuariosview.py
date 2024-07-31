import reflex as rx
from ..models.citas import Usuarios
from ..servicios.userservice import *
from Examennbm.templates import template


class UsuarioState(rx.State):
    usuarios: list[Usuarios]
    buscar_username: str = ""

    @rx.background
    async def get_todos_usuarios(self):
        async with self:
         self.usuarios = servicio_usuarios_all()

    @rx.background
    async def get_usuario_username(self):
        async with self:
            self.usuarios = servicio_consultar_usuario(self.buscar_username)

    def buscar_onchange(self, value: str):
        self.buscar_username = value

    @rx.background
    async def crear_usuario(self, data: dict):
        async with self:
        try:
            self.usuarios = servicio_crear_usuario(
                data['username'], data['password'], data['rol'],
                data['nombres'], data['apellidos'], data['cedula'],
                data['correo'], data['celular'], data['direccion']
            )
        except Exception as e:
            print(e)


@template(route="/usuarios", title="Lista de Usuarios", on_load=UsuarioState.get_todos_usuarios)
def usuario_page() -> rx.Component:
    return rx.flex(
        rx.heading("Usuarios", title="Usuarios", size="5", center=True),
        rx.vstack(
            buscar_usuario_username(),
            dialog_usuario_form(),
            tabla_usuarios(UsuarioState.usuarios),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )


def tabla_usuarios(lista_usuarios: list[Usuarios]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Username"),
                rx.table.column_header_cell("Nombres"),
                rx.table.column_header_cell("Apellidos"),
                rx.table.column_header_cell("Rol"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_usuarios, row_table)
        ),
    )


def row_table(usuario: Usuarios) -> rx.Component:
    return rx.table.row(
        rx.table.cell(usuario.username),
        rx.table.cell(usuario.nombres),
        rx.table.cell(usuario.apellidos),
        rx.table.cell(usuario.rol),
        rx.table.cell(
            rx.hstack(
                rx.button("Editar", variant="outline"),
                rx.button("Eliminar", variant="outline"),
            )
        ),
    )


def buscar_usuario_username() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Username",
                 on_change=UsuarioState.buscar_onchange),
        rx.button("Buscar usuario", on_click=UsuarioState.get_usuario_username)
    )


def dialog_usuario_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear usuario", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear usuario"),
                crear_usuario_form(),
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


def crear_usuario_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="Username", name="username"),
            rx.input(placeholder="Password", name="password", type="password"),
            rx.input(placeholder="Rol", name="rol"),
            rx.input(placeholder="Nombres", name="nombres"),
            rx.input(placeholder="Apellidos", name="apellidos"),
            rx.input(placeholder="Cédula", name="cedula"),
            rx.input(placeholder="Correo electrónico", name="correo"),
            rx.input(placeholder="# celular", name="celular"),
            rx.input(placeholder="Dirección", name="direccion"),
            rx.dialog.close(
                rx.button("Crear usuario", type="submit"),
            ),
        ),
        on_submit=UsuarioState.crear_usuario,
    )
