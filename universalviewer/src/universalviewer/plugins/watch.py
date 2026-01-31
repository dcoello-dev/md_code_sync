import logging
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from textual.widgets import Static
from universalviewer.plugins.base import ViewerPlugin

class LogOnChangeHandler(FileSystemEventHandler):
    """Manejador que envía logs cuando detecta cambios."""
    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"Archivo modificado: [yellow]{os.path.basename(event.src_path)}[/]")

    def on_created(self, event):
        tipo = "Directorio" if event.is_directory else "Archivo"
        logging.info(f"[green]{tipo} creado:[/] {os.path.basename(event.src_path)}")

    def on_deleted(self, event):
        logging.info(f"[red]Eliminado:[/] {os.path.basename(event.src_path)}")

class WatcherWidget(Static):
    def on_mount(self) -> None:
        self.update(f" Vigilando cambios en: [bold]{os.getcwd()}[/]")
        
        # Configuración de Watchdog
        self.event_handler = LogOnChangeHandler()
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path=".", recursive=False)
        self.observer.start()
        logging.info("Watcher iniciado en el directorio actual.")

    def on_unmount(self) -> None:
        # Es vital detener el hilo al cerrar el tab o la app
        self.observer.stop()
        self.observer.join()
        logging.info("Watcher detenido.")

class WatcherPlugin(ViewerPlugin):
    @property
    def title(self) -> str:
        return "Watcher"

    def get_widget(self) -> WatcherWidget:
        return WatcherWidget()
