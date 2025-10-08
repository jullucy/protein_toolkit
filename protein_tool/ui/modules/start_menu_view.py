from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                               QLabel, QGroupBox, QGridLayout)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont

class ToolButton(QPushButton):
    """Custom button for tool selection"""
    def __init__(self, name, description, icon_name=None):
        super().__init__()
        self.tool_name = name
        self.setMinimumSize(200, 120)
        self.setMaximumSize(250, 140)
        
        # Create layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Tool name label
        name_label = QLabel(name)
        name_font = QFont()
        name_font.setBold(True)
        name_font.setPointSize(12)
        name_label.setFont(name_font)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("color: #90A4AE; font-size: 10px;")
        
        # Description label
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("color: #90A4AE; font-size: 10px;")
        
        layout.addWidget(name_label)
        layout.addWidget(desc_label)
        
        # Create a widget to hold the layout
        widget = QWidget()
        widget.setLayout(layout)
        
        # Set the widget as the button's layout (using a different approach)
        button_layout = QVBoxLayout()
        button_layout.addWidget(widget)
        self.setLayout(button_layout)
        
        # Style the button
        self.setStyleSheet("""
            QPushButton {
                border: 2px solid #BBDEFB;
                border-radius: 8px;
                background-color: #F8F9FA;
                padding: 10px;
                color: #90A4AE;
            }
            QPushButton:hover {
                border-color: #1976D2;
                background-color: #E3F2FD;
            }
            QPushButton:pressed {
                background-color: #BBDEFB;
            }
        """)

class StartMenuView(QWidget):
    # Signal emitted when a tool is selected
    tool_selected = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("Protein Science Toolkit")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1565C0; margin-bottom: 20px;")
        
        # Subtitle
        subtitle = QLabel("Choose a tool to get started")
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #1976D2; margin-bottom: 30px;")
        
        # Tools section
        tools_group = QGroupBox("Available Tools")
        tools_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #0D47A1;
                border: 2px solid #BBDEFB;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                background-color: #E3F2FD;
                border-radius: 4px;
                color: #0D47A1;
            }
        """)
        
        tools_layout = QGridLayout()
        tools_layout.setSpacing(15)
        
        # Define available tools
        self.tools = [
            ("Beer-Lambert Calculator", "Calculate absorbance using\nBeer-Lambert law (A = ε·l·c)", "beer_lambert"),
            ("Thermodynamics Calculator", "Calculate ΔG, ΔH, ΔS, T, and K\nfor chemical reactions", "thermodynamics"),
            ("Protein Calculator", "Calculate protein properties\n(MW, pI, extinction coeff.)", "protein_calc"),
            ("Dilution Calculator", "Calculate dilution ratios\nand final concentrations", "dilution_calc")
        ]
        
        # Create tool buttons
        self.tool_buttons = {}
        row, col = 0, 0
        for display_name, description, tool_id in self.tools:
            btn = ToolButton(display_name, description)
            btn.clicked.connect(lambda checked, tid=tool_id: self.on_tool_selected(tid))
            
            # Disable buttons for tools not yet implemented
            if tool_id not in ["beer_lambert", "thermodynamics"]:
                btn.setEnabled(False)
                btn.setStyleSheet(btn.styleSheet() + """
                    QPushButton:disabled {
                        background-color: #F5F5F5;
                        color: #90A4AE;
                        border-color: #E0E0E0;
                    }
                """)
            
            tools_layout.addWidget(btn, row, col)
            self.tool_buttons[tool_id] = btn
            
            col += 1
            if col > 1:  # 2 columns
                col = 0
                row += 1
        
        tools_group.setLayout(tools_layout)
        
        # Add components to main layout
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(tools_group)
        main_layout.addStretch()  # Push everything to the top
        
        self.setLayout(main_layout)
    
    def on_tool_selected(self, tool_id):
        """Handle tool selection"""
        self.tool_selected.emit(tool_id)
