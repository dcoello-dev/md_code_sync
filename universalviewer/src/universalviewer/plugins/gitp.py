import logging
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from textual.widgets import Static
from universalviewer.plugins.base import ViewerPlugin

class GitWatcherHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_any_event(self, event):
        # Ignoramos cambios dentro de la carpeta .git para evitar bucles
        if ".git" in event.src_path:
            return
        # Ejecutamos la actualización en el hilo principal de Textual
        self.callback()

class GitStatusWidget(Static):
    def on_mount(self) -> None:
        self.styles.padding = (1, 2)
        self.update_git_status()
        self.start_watcher()

    def update_git_status(self) -> None:
        """Ejecuta git status y actualiza el widget con colores de Rich."""
        try:
            # Ejecutamos git status --short para una vista limpia
            result = subprocess.run(
                ["git", "status", "--short", "--branch"],
                capture_output=True,
                text=True,
                check=True
            )
            
            status_text = result.stdout.strip()
            if not status_text:
                output = "[green]✔ Working tree clean[/green]"
            else:
                # Formateo simple para resaltar el estado
                output = f"[bold cyan]Git Status:[/bold cyan]\n\n{status_text}"
            
            # Usamos call_from_thread porque esto lo llamará el Watcher (hilo externo)
            self.app.call_from_thread(self.update, output)
            
        except subprocess.CalledProcessError:
            self.update("[red]Error:[/] No es un repositorio git.")
        except Exception as e:
            logging.error(f"Error en GitWatcher: {e}")

    def start_watcher(self):
        self.event_handler = GitWatcherHandler(self.update_git_status)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path=".", recursive=True)
        self.observer.start()

    def on_unmount(self) -> None:
        if hasattr(self, "observer"):
            self.observer.stop()
            self.observer.join()

class GitStatusPlugin(ViewerPlugin):
    @property
    def title(self) -> str:
        return "Git Status"

    def get_widget(self) -> GitStatusWidget:
        return GitStatusWidget()

