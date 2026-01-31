import logging
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane
from universalviewer.plugins.manager import PluginManager

class Dashboard(App):
    """A dynamic Textual TUI for Universal Viewer."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("q", "quit", "Quit")]


    def compose(self) -> ComposeResult:
        import threading  
        import time
        def th():
            for i in range(0, 133):
                logging.info(i)
                time.sleep(1)

        th = threading.Thread(target=th, daemon=True)
        th.start()
        yield Header()

        plugins = PluginManager.load_plugins()
        with TabbedContent():
            if not plugins:
                with TabPane("Error"):
                    yield Header("No plugins found!")

            for plugin in plugins:
                with TabPane(plugin.title):
                    yield plugin.get_widget()
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


class InterfazLogHandler(logging.Handler):
    def __init__(self, widget_destino):
        super().__init__()
        self.widget_destino = widget_destino

    def emit(self, record):
        msg = self.format(record)
        self.widget_destino.append_text(msg + "\n")

    
