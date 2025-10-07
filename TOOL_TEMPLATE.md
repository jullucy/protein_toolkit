"""
Template for creating new tools in the Protein Science Toolkit

This file provides a template and examples for adding new tools to your application.
Copy this template and modify it to create your own tools.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Signal, QObject
from typing import Any

# ==============================
# 1. VIEWMODEL TEMPLATE
# ==============================

class ExampleToolVM(QObject):
    """
    ViewModel template for new tools.
    
    ViewModels handle the business logic and data management for your tool.
    They emit signals when data changes so the view can update.
    """
    
    # Define signals for data changes
    data_changed = Signal()
    result_calculated = Signal(float)  # Example: emit a calculated result
    
    def __init__(self):
        super().__init__()
        self._input_value = 0.0
        self._result = 0.0
    
    @property
    def input_value(self) -> float:
        return self._input_value
    
    @input_value.setter
    def input_value(self, value: float):
        if self._input_value != value:
            self._input_value = value
            self._calculate_result()
            self.data_changed.emit()
    
    @property
    def result(self) -> float:
        return self._result
    
    def _calculate_result(self):
        """Example calculation - replace with your own logic"""
        self._result = self._input_value * 2.0  # Simple example
        self.result_calculated.emit(self._result)

# ==============================
# 2. VIEW TEMPLATE
# ==============================

class ExampleToolView(QWidget):
    """
    View template for new tools.
    
    Views handle the user interface and user interactions.
    They connect to ViewModels to display data and send user input.
    """
    
    def __init__(self, viewmodel: ExampleToolVM):
        super().__init__()
        self.vm = viewmodel
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Example Tool")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Input section
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Input:"))
        
        # Add your input widgets here (spinboxes, line edits, etc.)
        self.input_button = QPushButton("Click me")
        input_layout.addWidget(self.input_button)
        
        layout.addLayout(input_layout)
        
        # Result section
        self.result_label = QLabel("Result: 0.0")
        self.result_label.setStyleSheet("font-size: 14px; margin-top: 10px;")
        layout.addWidget(self.result_label)
        
        # Add stretch to push content to top
        layout.addStretch()
        
        self.setLayout(layout)
    
    def connect_signals(self):
        """Connect UI signals to ViewModel methods"""
        # Connect UI events to viewmodel
        self.input_button.clicked.connect(lambda: setattr(self.vm, 'input_value', self.vm.input_value + 1))
        
        # Connect viewmodel signals to UI updates
        self.vm.result_calculated.connect(self.update_result)
    
    def update_result(self, result: float):
        """Update the result display when the viewmodel emits a change"""
        self.result_label.setText(f"Result: {result:.2f}")

# ==============================
# 3. CORE CALCULATION MODULE
# ==============================

def example_calculation(input_value: float) -> float:
    """
    Example core calculation function.
    
    Keep your core calculations separate from the UI for better testing
    and code organization.
    """
    return input_value * 2.0

# ==============================
# 4. HOW TO ADD YOUR TOOL
# ==============================

"""
To add a new tool to the application:

1. Create your tool files:
   - protein_tool/core/calculators/your_tool_calc.py (calculations)
   - protein_tool/viewmodels/your_tool_vm.py (viewmodel)
   - protein_tool/ui/modules/your_tool_view.py (view)

2. Register your tool in main_window.py:
   
   def _register_tools(self):
       # ... existing registrations ...
       
       def create_your_tool():
           from .viewmodels.your_tool_vm import YourToolVM
           from .ui.modules.your_tool_view import YourToolView
           vm = YourToolVM()
           view = YourToolView(vm)
           return view
       
       tool_registry.register_tool("your_tool", "Your Tool Name", create_your_tool)

3. Update start_menu_view.py tools list:
   
   self.tools = [
       # ... existing tools ...
       ("Your Tool Name", "Description of what your tool does", "your_tool"),
   ]

4. Write tests in tests/test_your_tool.py

That's it! Your tool will appear in the start menu and be accessible via the Tools menu.
"""

# ==============================
# 5. USEFUL PATTERNS
# ==============================

"""
Common patterns you might need:

1. File I/O (CSV, Excel):
   - Use pandas: pd.read_csv(), df.to_csv()
   - Use QFileDialog for file selection

2. Plotting:
   - Use the existing MplPlotWidget from ui/common/mpl_plot_widget.py
   - Create matplotlib figures and add them to the widget

3. Data validation:
   - Use QValidator for input validation
   - Add try/except blocks for calculations

4. Background processing:
   - Use QThread for long-running calculations
   - Emit progress signals to update UI

5. Export functionality:
   - Add export buttons that save results to files
   - Support multiple formats (PNG, SVG, CSV, etc.)
"""
