from PySide6.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QDoubleSpinBox, QLabel, QGroupBox, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QTextEdit, QSplitter,
    QFrame, QScrollArea, QGridLayout, QSpinBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPixmap, QIcon
import numpy as np
from ..common.mpl_plot_widget import MplPlotWidget
from ...core.calculators.beer_lambert import CalculationMode

# Simplified and consistent styling constants
BLUE_THEME = {
    'primary': "#1E6FBC",      # Main blue
    'primary_light': '#BBDEFB', # Light blue for borders/highlights
    'background': "#333333",   # Light gray background
    'surface': "#2F2F2F",      # White surface
    'success': '#4CAF50',      # Green for success
    'error': '#F44336',        # Red for errors
    'warning': '#FF9800',      # Orange for warnings
}

def get_group_style():
    """Simple, consistent group box styling"""
    return f"""
        QGroupBox {{
            font-size: 14px;
            font-weight: bold;
            color: {BLUE_THEME['primary_light']};
            border: 2px solid {BLUE_THEME['primary_light']};
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 15px;
            background-color: {BLUE_THEME['surface']};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 8px;
            background-color: {BLUE_THEME['primary']};
            color: white;
            border-radius: 4px;
        }}
    """

def get_button_style(color=None):
    """Simple button styling"""
    bg_color = color or BLUE_THEME['primary']
    hover_color = BLUE_THEME['primary_light'] if color == BLUE_THEME['primary'] else '#D32F2F'
    
    return f"""
        QPushButton {{
            background-color: {bg_color};
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        QPushButton:pressed {{
            background-color: {BLUE_THEME['primary_light']};
        }}
    """

class TheoryPanel(QScrollArea):
    """Panel displaying Beer-Lambert law theory and information"""
    
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(15)
        
        # Create theory content
        theory_text = QTextEdit()
        theory_text.setReadOnly(True)
        theory_text.setMaximumHeight(400)
        theory_text.setHtml(self._get_theory_html())
        
        # Parameters explanation
        params_group = QGroupBox("Parameters Explanation")
        params_group.setStyleSheet(get_group_style())
        params_layout = QVBoxLayout(params_group)
        
        params_text = QTextEdit()
        params_text.setReadOnly(True)
        params_text.setMaximumHeight(200)
        params_text.setHtml(self._get_parameters_html())
        params_layout.addWidget(params_text)
        
        # Applications
        apps_group = QGroupBox("Common Applications")
        apps_group.setStyleSheet(get_group_style())
        apps_layout = QVBoxLayout(apps_group)
        
        apps_text = QTextEdit()
        apps_text.setReadOnly(True)
        apps_text.setMaximumHeight(150)
        apps_text.setHtml(self._get_applications_html())
        apps_layout.addWidget(apps_text)
        
        layout.addWidget(theory_text)
        layout.addWidget(params_group)
        layout.addWidget(apps_group)
        layout.addStretch()
        
        self.setWidget(content)
    
    def _get_theory_html(self):
        return f"""
        <div style="padding: 15px; background: {BLUE_THEME['surface']}; border-radius: 8px;">
        <h2 style="color: {BLUE_THEME['primary']}; margin-top: 0;">Beer-Lambert Law</h2>

        <p style="color: {BLUE_THEME['primary_light']};">The Lambert–Beer law describes how the absorbance of light passing through a solution is related to the concentration of the absorbing species and the path length of the light.</p>

        <h3 style="color: {BLUE_THEME['primary_light']};">Mathematical Expression</h3>
        <div style="padding: 15px; border-radius: 8px; text-align: center; margin: 15px 0;">
            <strong>A = εlc</strong>
        </div>
        
        <h3 style="color: {BLUE_THEME['primary']};">Key Points</h3>
        <ul style="color: {BLUE_THEME['primary_light']};">
            <li><strong>Concentration:</strong> More molecules = more light absorbed</li>
            <li><strong>Path length:</strong> Longer path = more interactions</li>
            <li><strong>Molar absorptivity:</strong> How strongly the molecule absorbs light</li>
        </ul>
        </div>
        """
    
    def _get_parameters_html(self):
        return f"""
        <table style="width: 100%; border-collapse: collapse; background: {BLUE_THEME['surface']}; color: {BLUE_THEME['primary_light']};">
        <tr style="background: {BLUE_THEME['primary']}; color: white;">
            <th style="padding: 12px; text-align: left;">Parameter</th>
            <th style="padding: 12px; text-align: left;">Symbol</th>
            <th style="padding: 12px; text-align: left;">Units</th>
            <th style="padding: 12px; text-align: left;">Typical Range</th>
        </tr>
        <tr>
            <td style="padding: 10px;"><strong>Absorbance</strong></td>
            <td style="padding: 10px;">A</td>
            <td style="padding: 10px;">unitless</td>
            <td style="padding: 10px;">0.05 - 2.0</td>
        </tr>
        <tr style="background: {BLUE_THEME['background']};">
            <td style="padding: 10px;"><strong>Molar Absorptivity</strong></td>
            <td style="padding: 10px;">ε</td>
            <td style="padding: 10px;">M⁻¹cm⁻¹</td>
            <td style="padding: 10px;">10 - 100,000+</td>
        </tr>
        <tr>
            <td style="padding: 10px;"><strong>Path Length</strong></td>
            <td style="padding: 10px;">l</td>
            <td style="padding: 10px;">cm</td>
            <td style="padding: 10px;">0.1 - 10</td>
        </tr>
        <tr style="background: {BLUE_THEME['background']};">
            <td style="padding: 10px;"><strong>Concentration</strong></td>
            <td style="padding: 10px;">c</td>
            <td style="padding: 10px;">M (mol/L)</td>
            <td style="padding: 10px;">1×10⁻⁶ - 1×10⁻³</td>
        </tr>
        </table>
        """
    
    def _get_applications_html(self):
        return f"""
        <div style="color: {BLUE_THEME['primary_light']}; padding: 10px;">
        <ul>
            <li><strong>Protein Quantification:</strong> Measuring protein concentration at 280 nm</li>
            <li><strong>DNA/RNA Analysis:</strong> Nucleic acid quantification at 260 nm</li>
            <li><strong>Enzyme Assays:</strong> Monitoring substrate conversion or product formation</li>
            <li><strong>Drug Analysis:</strong> Pharmaceutical compound concentration determination</li>
            <li><strong>Environmental Monitoring:</strong> Pollutant concentration in water/air</li>
        </ul>
        </div>
        """

class CalculatorTab(QWidget):
    """Tab for individual parameter calculations"""
    
    def __init__(self, vm):
        super().__init__()
        self.vm = vm
        self.setStyleSheet(f"background-color: {BLUE_THEME['background']};")
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Left panel - inputs
        left_panel = QGroupBox("Calculation Parameters")
        left_panel.setStyleSheet(get_group_style())
        left_layout = QFormLayout(left_panel)
        left_layout.setSpacing(10)
        
        # Calculation mode selector
        self.mode_combo = QComboBox()
        self.mode_combo.setStyleSheet(f"""
            QComboBox {{
                padding: 8px;
                border: 2px solid {BLUE_THEME['primary_light']};
                border-radius: 4px;
                background: {BLUE_THEME['surface']};
                color: {BLUE_THEME['primary_light']};
            }}
        """)
        self.mode_combo.addItems([
            "Calculate Absorbance (A = ε×l×c)",
            "Calculate Concentration (c = A/(ε×l))",
            "Calculate Epsilon (ε = A/(l×c))",
            "Calculate Path Length (l = A/(ε×c))"
        ])
        left_layout.addRow(QLabel("Calculate:"), self.mode_combo)
        
        # Add separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {BLUE_THEME['primary_light']};")
        left_layout.addRow(line)
        
        # Input fields with simple styling
        input_style = f"""
            QDoubleSpinBox {{
                padding: 8px;
                border: 2px solid {BLUE_THEME['primary_light']};
                border-radius: 4px;
                background: {BLUE_THEME['surface']};
                color: {BLUE_THEME['primary_light']};
            }}
        """
        
        self.absorbance_input = QDoubleSpinBox()
        self.absorbance_input.setRange(0, 5.0)
        self.absorbance_input.setDecimals(4)
        self.absorbance_input.setSingleStep(0.001)
        self.absorbance_input.setStyleSheet(input_style)
        
        self.epsilon_input = QDoubleSpinBox()
        self.epsilon_input.setRange(1, 1e6)
        self.epsilon_input.setDecimals(0)
        self.epsilon_input.setValue(55000)
        self.epsilon_input.setStyleSheet(input_style)
        
        self.path_input = QDoubleSpinBox()
        self.path_input.setRange(0.01, 100)
        self.path_input.setDecimals(3)
        self.path_input.setValue(1.0)
        self.path_input.setStyleSheet(input_style)
        
        self.conc_input = QDoubleSpinBox()
        self.conc_input.setRange(0, 1)
        self.conc_input.setDecimals(9)
        self.conc_input.setSingleStep(1e-6)
        self.conc_input.setValue(1e-6)
        self.conc_input.setStyleSheet(input_style)
        
        # Add labels with proper styling
        label_style = f"color: {BLUE_THEME['primary_light']}; font-weight: bold;"
        
        left_layout.addRow(QLabel("Absorbance (A):").setStyleSheet(label_style) or QLabel("Absorbance (A):"), 
                          self.absorbance_input)
        left_layout.addRow(QLabel("Epsilon (M⁻¹cm⁻¹):").setStyleSheet(label_style) or QLabel("Epsilon (M⁻¹cm⁻¹):"), 
                          self.epsilon_input)
        left_layout.addRow(QLabel("Path Length (cm):").setStyleSheet(label_style) or QLabel("Path Length (cm):"), 
                          self.path_input)
        left_layout.addRow(QLabel("Concentration (M):").setStyleSheet(label_style) or QLabel("Concentration (M):"), 
                          self.conc_input)
        
        # Calculate button
        self.calc_button = QPushButton("Calculate")
        self.calc_button.setStyleSheet(get_button_style())
        left_layout.addRow(self.calc_button)
        
        # Result display
        self.result_label = QLabel("Result will appear here")
        self.result_label.setStyleSheet(f"""
            QLabel {{
                background-color: {BLUE_THEME['background']};
                color: {BLUE_THEME['primary_light']};
                padding: 15px;
                border-radius: 8px;
                border: 2px solid {BLUE_THEME['primary_light']};
                font-size: 14px;
                font-weight: bold;
            }}
        """)
        self.result_label.setWordWrap(True)
        left_layout.addRow(QLabel("Result:").setStyleSheet(label_style) or QLabel("Result:"), 
                          self.result_label)
        
        # Right panel - visualization
        right_panel = QGroupBox("Theoretical Curve")
        right_panel.setStyleSheet(get_group_style())
        right_layout = QVBoxLayout(right_panel)
        
        self.plot = MplPlotWidget()
        right_layout.addWidget(self.plot)
        
        # Plot controls
        plot_controls = QHBoxLayout()
        plot_controls.addWidget(QLabel("Max Concentration:"))
        
        self.max_conc_input = QDoubleSpinBox()
        self.max_conc_input.setRange(1e-9, 1e-2)
        self.max_conc_input.setDecimals(9)
        self.max_conc_input.setSingleStep(1e-6)
        self.max_conc_input.setValue(1e-4)
        self.max_conc_input.setStyleSheet(input_style)
        plot_controls.addWidget(self.max_conc_input)
        
        self.update_plot_button = QPushButton("Update Plot")
        self.update_plot_button.setStyleSheet(get_button_style(BLUE_THEME['success']))
        plot_controls.addWidget(self.update_plot_button)
        plot_controls.addStretch()
        
        right_layout.addLayout(plot_controls)
        
        # Main layout
        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)
        self.setLayout(layout)
        
        # Initialize UI state
        self._update_input_states()
    
    def connect_signals(self):
        self.mode_combo.currentIndexChanged.connect(self._on_mode_changed)
        self.calc_button.clicked.connect(self._calculate)
        self.update_plot_button.clicked.connect(self._update_theoretical_plot)
        
        self.vm.output_changed.connect(self._on_result_calculated)
        self.vm.error.connect(self._on_error)
        
        # Auto-update plot when epsilon or path changes
        self.epsilon_input.valueChanged.connect(self._auto_update_plot)
        self.path_input.valueChanged.connect(self._auto_update_plot)
        self.max_conc_input.valueChanged.connect(self._auto_update_plot)
    
    def _on_mode_changed(self):
        mode_index = self.mode_combo.currentIndex()
        modes = [CalculationMode.ABSORBANCE, CalculationMode.CONCENTRATION, 
                CalculationMode.EPSILON, CalculationMode.PATH_LENGTH]
        
        self.vm.calculation_mode = modes[mode_index]
        self._update_input_states()
    
    def _update_input_states(self):
        """Enable/disable input fields based on calculation mode"""
        mode = self.vm.calculation_mode
        
        # Reset all to enabled with normal styling
        normal_style = f"""
            QDoubleSpinBox {{
                padding: 8px;
                border: 2px solid {BLUE_THEME['primary_light']};
                border-radius: 4px;
                background: {BLUE_THEME['surface']};
                color: {BLUE_THEME['primary_light']};
            }}
        """
        
        disabled_style = f"""
            QDoubleSpinBox {{
                padding: 8px;
                border: 2px solid {BLUE_THEME['primary']};
                border-radius: 4px;
                background: {BLUE_THEME['primary_light']};
                color: {BLUE_THEME['primary_light']};
                font-weight: bold;
            }}
        """
        
        # Reset all inputs
        for input_widget in [self.absorbance_input, self.epsilon_input, self.path_input, self.conc_input]:
            input_widget.setEnabled(True)
            input_widget.setStyleSheet(normal_style)
        
        # Disable and highlight the field being calculated
        if mode == CalculationMode.ABSORBANCE:
            self.absorbance_input.setEnabled(False)
            self.absorbance_input.setStyleSheet(disabled_style)
        elif mode == CalculationMode.CONCENTRATION:
            self.conc_input.setEnabled(False)
            self.conc_input.setStyleSheet(disabled_style)
        elif mode == CalculationMode.EPSILON:
            self.epsilon_input.setEnabled(False)
            self.epsilon_input.setStyleSheet(disabled_style)
        elif mode == CalculationMode.PATH_LENGTH:
            self.path_input.setEnabled(False)
            self.path_input.setStyleSheet(disabled_style)
    
    def _calculate(self):
        """Perform calculation based on current mode"""
        try:
            kwargs = {}
            
            mode = self.vm.calculation_mode
            if mode == CalculationMode.ABSORBANCE:
                kwargs = {
                    'epsilon': self.epsilon_input.value(),
                    'path_length': self.path_input.value(),
                    'concentration': self.conc_input.value()
                }
            elif mode == CalculationMode.CONCENTRATION:
                kwargs = {
                    'absorbance': self.absorbance_input.value(),
                    'epsilon': self.epsilon_input.value(),
                    'path_length': self.path_input.value()
                }
            elif mode == CalculationMode.EPSILON:
                kwargs = {
                    'absorbance': self.absorbance_input.value(),
                    'path_length': self.path_input.value(),
                    'concentration': self.conc_input.value()
                }
            elif mode == CalculationMode.PATH_LENGTH:
                kwargs = {
                    'absorbance': self.absorbance_input.value(),
                    'epsilon': self.epsilon_input.value(),
                    'concentration': self.conc_input.value()
                }
            
            self.vm.calculate_parameter(**kwargs)
            
        except Exception as e:
            self._on_error(str(e))
    
    def _on_result_calculated(self, result):
        """Display calculation result"""
        mode = self.vm.calculation_mode
        
        if mode == CalculationMode.ABSORBANCE:
            text = f"Absorbance: {result:.4f}"
            self.absorbance_input.setValue(result)
        elif mode == CalculationMode.CONCENTRATION:
            text = f"Concentration: {result:.2e} M"
            self.conc_input.setValue(result)
        elif mode == CalculationMode.EPSILON:
            text = f"Molar Absorptivity: {result:.0f} M⁻¹cm⁻¹"
            self.epsilon_input.setValue(result)
        elif mode == CalculationMode.PATH_LENGTH:
            text = f"Path Length: {result:.3f} cm"
            self.path_input.setValue(result)
        
        self.result_label.setText(text)
        self.result_label.setStyleSheet(f"""
            QLabel {{
                background-color: #E8F5E9;
                color: #2E7D32;
                padding: 15px;
                border-radius: 8px;
                border: 2px solid {BLUE_THEME['success']};
                font-size: 14px;
                font-weight: bold;
            }}
        """)
    
    def _on_error(self, error_msg):
        """Display error message"""
        self.result_label.setText(f"Error: {error_msg}")
        self.result_label.setStyleSheet(f"""
            QLabel {{
                background-color: #FFEBEE;
                color: #C62828;
                padding: 15px;
                border-radius: 8px;
                border: 2px solid {BLUE_THEME['error']};
                font-size: 14px;
                font-weight: bold;
            }}
        """)
    
    def _auto_update_plot(self):
        """Auto-update plot when parameters change"""
        QTimer.singleShot(100, self._update_theoretical_plot)
    
    def _update_theoretical_plot(self):
        """Update theoretical curve plot"""
        try:
            epsilon = self.epsilon_input.value()
            path_length = self.path_input.value()
            max_conc = self.max_conc_input.value()
            
            if epsilon > 0 and path_length > 0 and max_conc > 0:
                self.vm.path_length = path_length
                self.vm.generate_theoretical_curve(epsilon, max_conc)
        except Exception as e:
            print(f"Plot update error: {e}")

class StandardCurveTab(QWidget):
    """Tab for standard curve analysis and linear regression"""
    
    def __init__(self, vm):
        super().__init__()
        self.vm = vm
        self.setStyleSheet(f"background-color: {BLUE_THEME['background']};")
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Left panel - data input and management
        left_panel = QGroupBox("Data Points")
        left_panel.setStyleSheet(get_group_style())
        left_layout = QVBoxLayout(left_panel)
        
        # Data input
        input_layout = QGridLayout()
        input_layout.setSpacing(10)
        
        # Input styling
        input_style = f"""
            QDoubleSpinBox {{
                padding: 8px;
                border: 2px solid {BLUE_THEME['primary_light']};
                border-radius: 4px;
                background: {BLUE_THEME['surface']};
                color: {BLUE_THEME['primary_light']};
            }}
        """
        
        label_style = f"color: {BLUE_THEME['primary_light']}; font-weight: bold;"
        
        conc_label = QLabel("Concentration (M):")
        conc_label.setStyleSheet(label_style)
        abs_label = QLabel("Absorbance:")
        abs_label.setStyleSheet(label_style)
        
        input_layout.addWidget(conc_label, 0, 0)
        input_layout.addWidget(abs_label, 0, 1)
        
        self.conc_data_input = QDoubleSpinBox()
        self.conc_data_input.setRange(0, 1)
        self.conc_data_input.setDecimals(9)
        self.conc_data_input.setSingleStep(1e-6)
        self.conc_data_input.setStyleSheet(input_style)
        
        self.abs_data_input = QDoubleSpinBox()
        self.abs_data_input.setRange(0, 5)
        self.abs_data_input.setDecimals(4)
        self.abs_data_input.setSingleStep(0.001)
        self.abs_data_input.setStyleSheet(input_style)
        
        self.add_point_button = QPushButton("Add Point")
        self.add_point_button.setStyleSheet(get_button_style())
        
        input_layout.addWidget(self.conc_data_input, 1, 0)
        input_layout.addWidget(self.abs_data_input, 1, 1)
        input_layout.addWidget(self.add_point_button, 1, 2)
        
        left_layout.addLayout(input_layout)
        
        # Data table
        self.data_table = QTableWidget(0, 3)
        self.data_table.setHorizontalHeaderLabels(["Concentration (M)", "Absorbance", "Actions"])
        self.data_table.setMaximumHeight(200)
        self.data_table.setStyleSheet(f"""
            QTableWidget {{
                border: 2px solid {BLUE_THEME['primary_light']};
                border-radius: 8px;
                background-color: {BLUE_THEME['surface']};
                color: {BLUE_THEME['primary_light']};
                gridline-color: {BLUE_THEME['primary_light']};
            }}
            QHeaderView::section {{
                background-color: {BLUE_THEME['primary']};
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {BLUE_THEME['primary_light']};
            }}
        """)
        left_layout.addWidget(self.data_table)
        
        # Data management buttons
        button_layout = QHBoxLayout()
        self.clear_data_button = QPushButton("Clear All")
        self.clear_data_button.setStyleSheet(get_button_style(BLUE_THEME['error']))
        
        self.regression_button = QPushButton("Perform Regression")
        self.regression_button.setStyleSheet(get_button_style())
        
        button_layout.addWidget(self.clear_data_button)
        button_layout.addWidget(self.regression_button)
        left_layout.addLayout(button_layout)
        
        # Results display
        results_label = QLabel("Regression Results:")
        results_label.setStyleSheet(label_style)
        left_layout.addWidget(results_label)
        
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(150)
        self.results_text.setReadOnly(True)
        self.results_text.setStyleSheet(f"""
            QTextEdit {{
                border: 2px solid {BLUE_THEME['primary_light']};
                border-radius: 8px;
                background-color: {BLUE_THEME['surface']};
                color: {BLUE_THEME['primary_light']};
                padding: 10px;
            }}
        """)
        left_layout.addWidget(self.results_text)
        
        # Right panel - plot
        right_panel = QGroupBox("Standard Curve")
        right_panel.setStyleSheet(get_group_style())
        right_layout = QVBoxLayout(right_panel)
        
        self.curve_plot = MplPlotWidget()
        right_layout.addWidget(self.curve_plot)
        
        # Plot settings
        plot_settings = QHBoxLayout()
        path_label = QLabel("Path Length (cm):")
        path_label.setStyleSheet(label_style)
        plot_settings.addWidget(path_label)
        
        self.path_length_input = QDoubleSpinBox()
        self.path_length_input.setRange(0.01, 100)
        self.path_length_input.setDecimals(3)
        self.path_length_input.setValue(1.0)
        self.path_length_input.setStyleSheet(input_style)
        plot_settings.addWidget(self.path_length_input)
        plot_settings.addStretch()
        
        right_layout.addLayout(plot_settings)
        
        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)
        self.setLayout(layout)
    
    def connect_signals(self):
        self.add_point_button.clicked.connect(self._add_data_point)
        self.clear_data_button.clicked.connect(self._clear_all_data)
        self.regression_button.clicked.connect(self._perform_regression)
        self.path_length_input.valueChanged.connect(self._update_path_length)
        
        self.vm.regression_completed.connect(self._display_regression_results)
        self.vm.curve_points_updated.connect(self._update_curve_plot)
        self.vm.error.connect(self._on_error)
    
    def _add_data_point(self):
        """Add a new data point to the table and viewmodel"""
        conc = self.conc_data_input.value()
        abs_val = self.abs_data_input.value()
        
        # Add to viewmodel
        self.vm.add_data_point(conc, abs_val)
        
        # Add to table
        row = self.data_table.rowCount()
        self.data_table.insertRow(row)
        
        self.data_table.setItem(row, 0, QTableWidgetItem(f"{conc:.2e}"))
        self.data_table.setItem(row, 1, QTableWidgetItem(f"{abs_val:.4f}"))
        
        # Add remove button
        remove_button = QPushButton("Remove")
        remove_button.setStyleSheet(get_button_style(BLUE_THEME['error']))
        remove_button.clicked.connect(lambda: self._remove_data_point(row))
        self.data_table.setCellWidget(row, 2, remove_button)
        
        # Clear inputs
        self.conc_data_input.setValue(0)
        self.abs_data_input.setValue(0)
    
    def _remove_data_point(self, row):
        """Remove a data point"""
        self.vm.remove_data_point(row)
        self.data_table.removeRow(row)
    
    def _clear_all_data(self):
        """Clear all data points"""
        self.vm.clear_data_points()
        self.data_table.setRowCount(0)
        self.results_text.clear()
    
    def _perform_regression(self):
        """Perform linear regression analysis"""
        if len(self.vm.data_points) < 2:
            self._on_error("Need at least 2 data points for regression")
            return
        
        self.vm.path_length = self.path_length_input.value()
        self.vm.perform_linear_regression()
    
    def _update_path_length(self):
        """Update path length in viewmodel"""
        self.vm.path_length = self.path_length_input.value()
    
    def _display_regression_results(self, result):
        """Display regression analysis results"""
        html = f"""
        <div style="padding: 15px;">
        <h3 style="color: {BLUE_THEME['primary']}; margin-top: 0;">Regression Results</h3>
        
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px;">
        <tr><td style="padding: 8px; font-weight: bold;">Slope (ε×l):</td><td style="padding: 8px;">{result.slope:.2e} M⁻¹</td></tr>
        <tr><td style="padding: 8px; font-weight: bold;">Intercept:</td><td style="padding: 8px;">{result.intercept:.4f}</td></tr>
        <tr><td style="padding: 8px; font-weight: bold;">R² Value:</td><td style="padding: 8px;">{result.r_squared:.4f}</td></tr>
        <tr><td style="padding: 8px; font-weight: bold;">Std Error:</td><td style="padding: 8px;">{result.std_error:.2e}</td></tr>
        """
        
        if result.epsilon is not None:
            html += f"<tr><td style='padding: 8px; font-weight: bold;'>Calculated ε:</td><td style='padding: 8px;'>{result.epsilon:.0f} M⁻¹cm⁻¹</td></tr>"
        
        html += "</table>"
        
        # Add quality assessment
        if result.r_squared > 0.99:
            quality = "Excellent"
            color = BLUE_THEME['success']
        elif result.r_squared > 0.95:
            quality = "Good"
            color = BLUE_THEME['warning']
        else:
            quality = "Poor"
            color = BLUE_THEME['error']
            
        html += f'<div style="padding: 10px; background-color: {color}20; border-left: 4px solid {color}; border-radius: 4px;"><strong style="color: {color};">Fit Quality: {quality}</strong></div>'
        html += "</div>"
        
        self.results_text.setHtml(html)
    
    def _update_curve_plot(self, plot_data):
        """Update the curve plot with data points and regression line"""
        if not plot_data:
            return
            
        try:
            # Clear previous plot
            ax = self.curve_plot.figure.clear()
            ax = self.curve_plot.figure.add_subplot(111)
            
            if isinstance(plot_data[0], dict):
                data = plot_data[0]
                
                # Plot data points
                if 'data_points' in data:
                    x_data, y_data = zip(*data['data_points'])
                    ax.scatter(x_data, y_data, c=BLUE_THEME['primary'], s=50, alpha=0.7, label='Data Points')
                
                # Plot regression line
                if 'regression_line' in data and data['regression_line']:
                    x_line, y_line = zip(*data['regression_line'])
                    ax.plot(x_line, y_line, color=BLUE_THEME['error'], linewidth=2, label='Linear Fit')
                    
                ax.legend()
            else:
                # Theoretical curve
                x_data, y_data = zip(*plot_data)
                ax.plot(x_data, y_data, color=BLUE_THEME['success'], linewidth=2, label='Theoretical Curve')
            
            ax.set_xlabel('Concentration (M)')
            ax.set_ylabel('Absorbance')
            ax.set_title('Beer-Lambert Standard Curve')
            ax.grid(True, alpha=0.3)
            
            self.curve_plot.canvas.draw()
            
        except Exception as e:
            print(f"Plot error: {e}")
    
    def _on_error(self, error_msg):
        """Display error message"""
        self.results_text.setHtml(f'<div style="padding: 15px; color: {BLUE_THEME["error"]};"><strong>Error:</strong> {error_msg}</div>')

class BeerLambertView(QWidget):
    """Main Beer-Lambert tool view with tabbed interface"""
    
    def __init__(self, vm):
        super().__init__()
        self.vm = vm
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title = QLabel("Beer-Lambert Law Calculator & Analysis")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                color: {BLUE_THEME['primary']};
                background: {BLUE_THEME['surface']};
                padding: 20px;
                border: 2px solid {BLUE_THEME['primary_light']};
                border-radius: 10px;
                margin-bottom: 15px;
            }}
        """)
        layout.addWidget(title)
        
        # Create tabbed interface
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 2px solid {BLUE_THEME['primary_light']};
                border-radius: 8px;
                background-color: {BLUE_THEME['surface']};
            }}
            QTabBar::tab {{
                background-color: {BLUE_THEME['background']};
                color: {BLUE_THEME['primary_light']};
                padding: 12px 20px;
                margin: 2px;
                border: 2px solid {BLUE_THEME['primary_light']};
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                min-width: 120px;
            }}
            QTabBar::tab:selected {{
                background-color: {BLUE_THEME['primary']};
                color: white;
                border-color: {BLUE_THEME['primary']};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {BLUE_THEME['primary_light']};
                color: {BLUE_THEME['primary_light']};
            }}
        """)
        
        # Theory tab
        self.theory_tab = TheoryPanel()
        self.tab_widget.addTab(self.theory_tab, "Theory")
        
        # Calculator tab
        self.calculator_tab = CalculatorTab(self.vm)
        self.tab_widget.addTab(self.calculator_tab, "Calculator")
        
        # Standard curve tab  
        self.curve_tab = StandardCurveTab(self.vm)
        self.tab_widget.addTab(self.curve_tab, "Standard Curve")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
    
    def connect_signals(self):
        """Connect viewmodel signals"""
        self.vm.curve_points_updated.connect(self._update_calculator_plot)
    
    def _update_calculator_plot(self, plot_data):
        """Update the calculator tab plot"""
        if hasattr(self.calculator_tab, 'plot') and plot_data:
            try:
                ax = self.calculator_tab.plot.figure.clear()
                ax = self.calculator_tab.plot.figure.add_subplot(111)
                
                x_data, y_data = zip(*plot_data)
                ax.plot(x_data, y_data, color=BLUE_THEME['primary'], linewidth=2)
                ax.set_xlabel('Concentration (M)')
                ax.set_ylabel('Absorbance')
                ax.set_title('Theoretical Beer-Lambert Curve')
                ax.grid(True, alpha=0.3)
                
                self.calculator_tab.plot.canvas.draw()
            except Exception as e:
                print(f"Calculator plot error: {e}")
