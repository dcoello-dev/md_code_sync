import logging
from textual.widgets import RichLog
from universalviewer.plugins.base import ViewerPlugin

class LogHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        niveles = {
            "INFO": "bold blue",
            "WARNING": "bold yellow",
            "ERROR": "bold red",
            "CRITICAL": "white on red"
        }
        color = niveles.get(record.levelname, "white")
        
        message = f"[[{color}]{record.levelname:8}[/]] {self.format(record)}"
        
        try:
            self.widget.app.call_from_thread(self.widget.write, message)
        except Exception:
            pass

class InfoWidget(RichLog):
    def __init__(self, **kwargs):
        super().__init__(markup=True, highlight=True, **kwargs)
        self.handler = LogHandler(self)

    def on_mount(self) -> None:
        self.write("[bold magenta]## Universal Viewer Core[/bold magenta]\n")
        
        self.handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt="%X"))
        
        logging.getLogger().addHandler(self.handler)
        logging.getLogger().setLevel(logging.INFO)
        
        logging.info("Sistema de logs con estilo Rich iniciado.")

    def on_unmount(self) -> None:
        logging.getLogger().removeHandler(self.handler)

class InfoPlugin(ViewerPlugin):
    @property
    def title(self) -> str:
        return "Info"

    def get_widget(self) -> InfoWidget:
        return InfoWidget()
