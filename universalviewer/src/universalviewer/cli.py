import typer
from rich.console import Console
from rich.table import Table
from universalviewer.models import User

app = typer.Typer(help="Universal Viewer CLI")
console = Console()

@app.command()
def hello(name: str = "World"):
    """
    Say hello with Rich formatting.
    """
    console.print(f"Hello [bold magenta]{name}[/bold magenta]!", style="italic")

@app.command()
def list_users():
    """
    Display a list of users in a Rich table.
    """
    # Sample data using Pydantic model
    users = [
        User(id=1, name="Alice", email="alice@example.com"),
        User(id=2, name="Bob", email="bob@example.com", is_active=False),
    ]

    table = Table(title="App Users")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Email", style="green")
    table.add_column("Status", justify="center")

    for user in users:
        status = "[green]Active[/]" if user.is_active else "[red]Inactive[/]"
        table.add_row(str(user.id), user.name, user.email, status)

    console.print(table)

if __name__ == "__main__":
    app()
