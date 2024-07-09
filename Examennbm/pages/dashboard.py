from Examennbm.templates import template
import reflex as rx


@template(route="/dashboard", title="Dashboard")
def dashboard() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.vstack(
        rx.heading("UIDE", size="8"),
        rx.text("Sistema de Gestión de Citas Médicas "),
        rx.text(
            " ",
        ),
    )
