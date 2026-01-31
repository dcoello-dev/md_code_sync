import sys
from universalviewer.cli import app as cli_app
from universalviewer.tui import Dashboard

def run():
    # If no arguments or help is not requested, we could default to TUI
    # But for simplicity, let's keep Typer as the main entry
    if len(sys.argv) > 1 and sys.argv[1] == "tui":
        tui = Dashboard()
        tui.run()
    else:
        cli_app()

if __name__ == "__main__":
    run()
