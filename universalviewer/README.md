# Universal Viewer

A modern Python project templates with:
- **Rich**: For beautiful console output.
- **Pydantic**: For data validation.
- **Typer**: For easy CLI creation.
- **Textual**: For interactive terminal user interfaces (TUI).

## Installation

```bash
pip install -e .
```

## Usage

### CLI Mode (Default)

```bash
python -m src.main --help
python -m src.main hello --name "Antigravity"
python -m src.main list-users
```

### TUI Mode

```bash
python -m src.main tui
```

## Structure

- `src/models.py`: Pydantic data models.
- `src/cli.py`: Typer command definitions with Rich.
- `src/tui.py`: Textual application.
- `src/main.py`: Entry point.
- `universalviewer/main.py`: Entry point.
