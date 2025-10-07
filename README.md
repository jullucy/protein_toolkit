# Protein Tool

## Features in this starter
- **Start Menu**: Choose between different protein science tools
- **Beer–Lambert calculator** (A = ε · l · c) with live preview plot
- **Tool Registry System**: Easy framework for adding new tools
- **Modern UI**: Clean, professional interface with Qt6/PySide6
- **Modular Architecture**: Separating UI, viewmodels, and core science logic
- **Menu Navigation**: File menu with Home/Quit, Tools menu for quick access

## 1) Set up
```bash
# Use Python 3.11+ if possible
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## 2) Run the app
```bash
python -m protein_tool
```

You should see a start menu with available tools. Click on "Beer-Lambert Calculator" to access the original functionality.

## 3) Package as a single executable (PyInstaller)
```bash
pip install pyinstaller
pyinstaller -n ProteinTool --noconsole --onefile protein_tool/__main__.py
# Output is in the dist/ folder
```

> On macOS you can build an .app bundle with additional PyInstaller flags; on Windows, you'll get a .exe.

## Project structure
```
protein_tool/
  __init__.py
  __main__.py
  app.py
  main_window.py
  ui/
    common/mpl_plot_widget.py
    modules/beer_lambert_view.py
    modules/start_menu_view.py
  viewmodels/beer_lambert_vm.py
  core/
    calculators/beer_lambert.py
    tool_registry.py
requirements.txt
README.md
TOOL_TEMPLATE.md
```
