import datetime
from textual.widgets import RichLog
from universalviewer.plugins.base import ViewerPlugin

class LogWidget(RichLog):
    def on_mount(self) -> None:
        self.write("Log viewer started...")
        self.set_interval(2.0, self.add_log_entry)

    def add_log_entry(self) -> None:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.write(f"[[bold cyan]{now}[/]] Event simulated in hot-update tab.")

class LogPlugin(ViewerPlugin):
    @property
    def title(self) -> str:
        return "Real-time Logs"

    def get_widget(self) -> LogWidget:
        return LogWidget(highlight=True, markup=True)
