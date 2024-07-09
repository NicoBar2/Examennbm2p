"""The home page of the app."""

from Examennbm import styles
from Examennbm.templates import template

import reflex as rx


@template(route="/", title="Pagina Principal")
def index() -> rx.Component:
    """Medicos.

    Returns:
        The UI for the home page.
    """
    with open("README.md", encoding="utf-8") as readme:
        content = readme.read()
    return rx.markdown(content, component_map=styles.markdown_style)
