from PySide6.QtWidgets import QMainWindow, QApplication, QMenuBar, QStackedWidget
from PySide6.QtGui import QAction
from .ui.modules.beer_lambert_view import BeerLambertView
from .ui.modules.thermodynamics_view import ThermodynamicsView
from .ui.modules.start_menu_view import StartMenuView
from .viewmodels.beer_lambert_vm import BeerLambertVM
from .viewmodels.thermodynamics_vm import ThermodynamicsViewModel
from .core.tool_registry import tool_registry

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Protein Science Toolkit")
        self.resize(1000, 700)
        
        # Current tool tracking
        self.current_tool_id = None
        
        # Register available tools
        self._register_tools()
        
        # Create stacked widget to manage different views
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create and add start menu
        self.start_menu = StartMenuView()
        self.start_menu.tool_selected.connect(self.load_tool)
        self.stacked_widget.addWidget(self.start_menu)
        
        # Setup menu bar
        self._setup_menu_bar()
        
        # Show start menu initially
        self.show_start_menu()
    
    def _register_tools(self):
        """Register all available tools with the tool registry"""
        def create_beer_lambert_tool():
            vm = BeerLambertVM()
            view = BeerLambertView(vm)
            return view
        
        tool_registry.register_tool("beer_lambert", "Beer-Lambert Calculator", create_beer_lambert_tool)
        
        def create_thermodynamics_tool():
            vm = ThermodynamicsViewModel()
            view = ThermodynamicsView(vm)
            return view
        
        tool_registry.register_tool("thermodynamics", "Thermodynamics Tool", create_thermodynamics_tool)
        
        # Placeholder functions for future tools
        def create_placeholder_tool():
            from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout
            widget = QWidget()
            layout = QVBoxLayout()
            label = QLabel("This tool is not yet implemented.\nComing soon!")
            label.setStyleSheet("font-size: 16px; color: #666; text-align: center;")
            layout.addWidget(label)
            widget.setLayout(layout)
            return widget
        
        tool_registry.register_tool("standard_curve", "Standard Curve", create_placeholder_tool)
        tool_registry.register_tool("protein_calc", "Protein Calculator", create_placeholder_tool)
        tool_registry.register_tool("dilution_calc", "Dilution Calculator", create_placeholder_tool)
    
    def _setup_menu_bar(self):
        """Setup the application menu bar"""
        menubar = QMenuBar(self)
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        # Home action
        act_home = QAction("&Home", self)
        act_home.setShortcut("Ctrl+H")
        act_home.triggered.connect(self.show_start_menu)
        file_menu.addAction(act_home)
        
        file_menu.addSeparator()
        
        # Quit action
        act_quit = QAction("&Quit", self)
        act_quit.setShortcut("Ctrl+Q")
        act_quit.triggered.connect(QApplication.instance().quit)
        file_menu.addAction(act_quit)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        # Add actions for each registered tool
        for tool_id, display_name in tool_registry.get_available_tools().items():
            action = QAction(display_name, self)
            action.triggered.connect(lambda checked, tid=tool_id: self.load_tool(tid))
            tools_menu.addAction(action)
        
        self.setMenuBar(menubar)
    
    def show_start_menu(self):
        """Show the start menu"""
        self.stacked_widget.setCurrentWidget(self.start_menu)
        self.current_tool_id = None
        self.setWindowTitle("Protein Science Toolkit")
    
    def load_tool(self, tool_id: str):
        """Load and display the specified tool"""
        if not tool_registry.is_tool_available(tool_id):
            print(f"Tool '{tool_id}' is not available")
            return
        
        try:
            # Create tool widget
            tool_widget = tool_registry.create_tool(tool_id)
            
            # Remove previous tool if exists
            if hasattr(self, 'current_tool_widget'):
                self.stacked_widget.removeWidget(self.current_tool_widget)
                self.current_tool_widget.deleteLater()
            
            # Add new tool widget
            self.current_tool_widget = tool_widget
            self.stacked_widget.addWidget(tool_widget)
            self.stacked_widget.setCurrentWidget(tool_widget)
            
            # Update window title and tracking
            self.current_tool_id = tool_id
            tool_name = tool_registry.get_tool_name(tool_id)
            self.setWindowTitle(f"Protein Science Toolkit - {tool_name}")
            
        except Exception as e:
            print(f"Error loading tool '{tool_id}': {e}")
            # Fall back to start menu
            self.show_start_menu()
