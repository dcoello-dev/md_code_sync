from textual.widgets import DirectoryTree, Static
from textual.containers import Horizontal, Vertical
from textual.events import MouseDown, MouseMove, MouseUp
from universalviewer.plugins.base import ViewerPlugin

class Resizer(Static):
    """Widget que actúa como la barra de separación."""
    def on_mount(self) -> None:
        self.styles.width = 1
        self.styles.background = "gray"
        self.styles.cursor = "col-resize"

class EditorWidget(Horizontal):
    # Definimos el CSS de la clase de forma estática
    CSS = """
    #sidebar {
        min-width: 10;
        max-width: 70%;
    }
    #main-content {
        background: $canvas;
    }
    #resizer:hover {
        background: $accent;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sidebar_width = 30
        self.dragging = False

    def compose(self):
        with Vertical(id="sidebar"):
            yield DirectoryTree(".")
        yield Resizer(id="resizer")
        with Vertical(id="main-content"):
            yield Static("Zona de trabajo principal", id="content-text")

    def on_mount(self) -> None:
        self.query_one("#sidebar").styles.width = self.sidebar_width

    def on_mouse_down(self, event: MouseDown) -> None:
        # Si clickeamos el resizer, activamos el arrastre
        if event.target.id == "resizer":
            self.dragging = True
            self.capture_mouse()

    def on_mouse_move(self, event: MouseMove) -> None:
        if self.dragging:
            # event.x nos da la posición relativa al widget contenedor
            self.sidebar_width = event.x
            self.query_one("#sidebar").styles.width = self.sidebar_width

    def on_mouse_up(self, event: MouseUp) -> None:
        self.dragging = False
        self.release_mouse()

class EditorPlugin(ViewerPlugin):
    @property
    def title(self) -> str:
        return "Editor Pro"

    def get_widget(self) -> EditorWidget:
        return EditorWidget()
