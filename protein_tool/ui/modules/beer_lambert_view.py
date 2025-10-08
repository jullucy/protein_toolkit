from PySide6.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QDoubleSpinBox, QLabel, QGroupBox, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QTextEdit, QSplitter,
    QFrame, QScrollArea, QGridLayout, QSpinBox, QHeaderView
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
import numpy as np
from ..common.mpl_plot_widget import MplPlotWidget
from ..common.styles import (
    get_group_box_style, get_button_style, get_input_style, get_input_highlighted_style,
    get_label_style, get_table_style, get_text_edit_style, get_tab_widget_style,
    get_main_widget_style, generate_theory_html, generate_parameters_table,
    generate_results_html, get_html_colors
)
from ...core.calculators.beer_lambert import CalculationMode

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
        theory_text.setStyleSheet(get_text_edit_style())
        theory_text.setHtml(self._get_theory_html())
        
        # Parameters explanation
        params_group = QGroupBox("Parameters Explanation")
        params_group.setStyleSheet(get_group_box_style())
        params_layout = QVBoxLayout(params_group)
        
        params_text = QTextEdit()
        params_text.setReadOnly(True)
        params_text.setMaximumHeight(200)
        params_text.setStyleSheet(get_text_edit_style())
        params_text.setHtml(self._get_parameters_html())
        params_layout.addWidget(params_text)
        
        # Applications
        apps_group = QGroupBox("Common Applications")
        apps_group.setStyleSheet(get_group_box_style())
        apps_layout = QVBoxLayout(apps_group)
        
        apps_text = QTextEdit()
        apps_text.setReadOnly(True)
        apps_text.setMaximumHeight(150)
        apps_text.setStyleSheet(get_text_edit_style())
        apps_text.setHtml(self._get_applications_html())
        apps_layout.addWidget(apps_text)
        
        layout.addWidget(theory_text)
        layout.addWidget(params_group)
        layout.addWidget(apps_group)
        layout.addStretch()
        
        self.setWidget(content)
    
    def _get_theory_html(self):
        content = """The Lambert–Beer law describes how the absorbance of light passing through a solution 
        is related to the concentration of the absorbing species and the path length of the light."""
        
        equations = """
        <p style="font-size: 16px; text-align: center;"><strong>A = ε × l × c</strong></p>
        <p><strong>Key Points:</strong></p>
        <ul>
            <li><strong>Concentration:</strong> More molecules = more light absorbed</li>
            <li><strong>Path length:</strong> Longer path = more interactions</li>
            <li><strong>Molar absorptivity:</strong> How strongly the molecule absorbs light</li>
        </ul>
        """
        
        return generate_theory_html("Beer-Lambert Law", content, equations)
    
    def _get_parameters_html(self):
        parameters = [
            ("Absorbance", "A", "unitless", "0.05 - 2.0"),
            ("Molar Absorptivity", "ε", "M⁻¹cm⁻¹", "10 - 100,000+"),
            ("Path Length", "l", "cm", "0.1 - 10"),
            ("Concentration", "c", "M (mol/L)", "1×10⁻⁶ - 1×10⁻³")
        ]
        return generate_parameters_table(parameters)
    
    def _get_applications_html(self):
        applications = """
        <ul>
            <li><strong>Protein Quantification:</strong> Measuring protein concentration at 280 nm</li>
            <li><strong>DNA/RNA Analysis:</strong> Nucleic acid quantification at 260 nm</li>
            <li><strong>Enzyme Assays:</strong> Monitoring substrate conversion or product formation</li>
            <li><strong>Drug Analysis:</strong> Pharmaceutical compound concentration determination</li>
            <li><strong>Environmental Monitoring:</strong> Pollutant concentration in water/air</li>
        </ul>
        """
        return generate_theory_html("", "", "", "", applications)

class CalculatorTab(QWidget):
    """Tab for individual parameter calculations"""
    
    def __init__(self, vm):
        super().__init__()
        self.vm = vm
        self.setStyleSheet(get_main_widget_style())
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Left panel - inputs
        left_panel = QGroupBox("Calculation Parameters")
        left_panel.setStyleSheet(get_group_box_style())
        left_layout = QFormLayout(left_panel)
        left_layout.setSpacing(10)
        
        # Calculation mode selector
        self.mode_combo = QComboBox()
        self.mode_combo.setStyleSheet(get_input_style())
        self.mode_combo.addItems([
            "Calculate Absorbance (A = ε×l×c)",
            "Calculate Concentration (c = A/(ε×l))",
            "Calculate Epsilon (ε = A/(l×c))",
            "Calculate Path Length (l = A/(ε×c))"
        ])
        
        calc_label = QLabel("Calculate:")
        calc_label.setStyleSheet(get_label_style('subtitle'))
        left_layout.addRow(calc_label, self.mode_combo)
        
        # Add separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        left_layout.addRow(line)
        
        # Input fields
        self.absorbance_input = QDoubleSpinBox()
        self.absorbance_input.setRange(0, 5.0)
        self.absorbance_input.setDecimals(4)
        self.absorbance_input.setSingleStep(0.001)
        self.absorbance_input.setStyleSheet(get_input_style())
        
        self.epsilon_input = QDoubleSpinBox()
        self.epsilon_input.setRange(1, 1e6)
        self.epsilon_input.setDecimals(0)
        self.epsilon_input.setValue(55000)
        self.epsilon_input.setStyleSheet(get_input_style())
        
        self.path_input = QDoubleSpinBox()
        self.path_input.setRange(0.01, 100)
        self.path_input.setDecimals(3)
        self.path_input.setValue(1.0)
        self.path_input.setStyleSheet(get_input_style())
        
        self.conc_input = QDoubleSpinBox()
        self.conc_input.setRange(0, 1)
        self.conc_input.setDecimals(9)
        self.conc_input.setSingleStep(1e-6)
        self.conc_input.setValue(1e-6)
        self.conc_input.setStyleSheet(get_input_style())
        
        # Add labels with proper styling
        abs_label = QLabel("Absorbance (A):")
        abs_label.setStyleSheet(get_label_style('subtitle'))
        left_layout.addRow(abs_label, self.absorbance_input)
        
        eps_label = QLabel("Epsilon (M⁻¹cm⁻¹):")
        eps_label.setStyleSheet(get_label_style('subtitle'))
        left_layout.addRow(eps_label, self.epsilon_input)
        
        path_label = QLabel("Path Length (cm):")
        path_label.setStyleSheet(get_label_style('subtitle'))
        left_layout.addRow(path_label, self.path_input)
        
        conc_label = QLabel("Concentration (M):")
        conc_label.setStyleSheet(get_label_style('subtitle'))
        left_layout.addRow(conc_label, self.conc_input)
        
        # Calculate button
        self.calc_button = QPushButton("Calculate")
        self.calc_button.setStyleSheet(get_button_style('primary'))
        left_layout.addRow(self.calc_button)
        
        # Result display
        self.result_label = QLabel("Result will appear here")
        self.result_label.setStyleSheet(get_label_style('normal'))
        self.result_label.setWordWrap(True)
        
        result_title = QLabel("Result:")
        result_title.setStyleSheet(get_label_style('subtitle'))
        left_layout.addRow(result_title, self.result_label)
        
        # Right panel - visualization
        right_panel = QGroupBox("Theoretical Curve")
        right_panel.setStyleSheet(get_group_box_style())
        right_layout = QVBoxLayout(right_panel)
        
        self.plot = MplPlotWidget()
        right_layout.addWidget(self.plot)
        
        # Plot controls
        plot_controls = QHBoxLayout()
        max_conc_label = QLabel("Max Concentration:")
        max_conc_label.setStyleSheet(get_label_style('subtitle'))
        plot_controls.addWidget(max_conc_label)
        
        self.max_conc_input = QDoubleSpinBox()
        self.max_conc_input.setRange(1e-9, 1e-2)
        self.max_conc_input.setDecimals(9)
        self.max_conc_input.setSingleStep(1e-6)
        self.max_conc_input.setValue(1e-4)
        self.max_conc_input.setStyleSheet(get_input_style())
        plot_controls.addWidget(self.max_conc_input)
        
        self.update_plot_button = QPushButton("Update Plot")
        self.update_plot_button.setStyleSheet(get_button_style('secondary'))
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
        
        # Auto-update plot when parameters change
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
        
        # Reset all inputs to normal styling
        for input_widget in [self.absorbance_input, self.epsilon_input, self.path_input, self.conc_input]:
            input_widget.setEnabled(True)
            input_widget.setStyleSheet(get_input_style())
        
        # Highlight the field being calculated
        if mode == CalculationMode.ABSORBANCE:
            self.absorbance_input.setEnabled(False)
            self.absorbance_input.setStyleSheet(get_input_highlighted_style())
        elif mode == CalculationMode.CONCENTRATION:
            self.conc_input.setEnabled(False)
            self.conc_input.setStyleSheet(get_input_highlighted_style())
        elif mode == CalculationMode.EPSILON:
            self.epsilon_input.setEnabled(False)
            self.epsilon_input.setStyleSheet(get_input_highlighted_style())
        elif mode == CalculationMode.PATH_LENGTH:
            self.path_input.setEnabled(False)
            self.path_input.setStyleSheet(get_input_highlighted_style())
    
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
        self.result_label.setStyleSheet(get_label_style('result_success'))
    
    def _on_error(self, error_msg):
        """Display error message"""
        self.result_label.setText(f"Error: {error_msg}")
        self.result_label.setStyleSheet(get_label_style('result_error'))
    
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
        self.setStyleSheet(get_main_widget_style())
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Left panel - data input and management
        left_panel = QGroupBox("Data Points")
        left_panel.setStyleSheet(get_group_box_style())
        left_panel.setMinimumWidth(400)  # Set minimum width to prevent label cutoff
        left_layout = QVBoxLayout(left_panel)
        
        # Data input
        input_layout = QGridLayout()
        input_layout.setSpacing(10)
        input_layout.setColumnStretch(0, 1)  # Make concentration column expandable
        input_layout.setColumnStretch(1, 1)  # Make absorbance column expandable
        input_layout.setColumnStretch(2, 0)  # Keep button column fixed
        
        conc_label = QLabel("Concentration (M):")
        conc_label.setStyleSheet(get_label_style('subtitle'))
        conc_label.setWordWrap(True)  # Allow label text to wrap if needed
        abs_label = QLabel("Absorbance:")
        abs_label.setStyleSheet(get_label_style('subtitle'))
        abs_label.setWordWrap(True)
        
        input_layout.addWidget(conc_label, 0, 0)
        input_layout.addWidget(abs_label, 0, 1)
        
        self.conc_data_input = QDoubleSpinBox()
        self.conc_data_input.setRange(0, 1)
        self.conc_data_input.setDecimals(9)
        self.conc_data_input.setSingleStep(1e-6)
        self.conc_data_input.setStyleSheet(get_input_style())
        self.conc_data_input.setMinimumWidth(120)  # Ensure minimum width
        
        self.abs_data_input = QDoubleSpinBox()
        self.abs_data_input.setRange(0, 5)
        self.abs_data_input.setDecimals(4)
        self.abs_data_input.setSingleStep(0.001)
        self.abs_data_input.setStyleSheet(get_input_style())
        self.abs_data_input.setMinimumWidth(100)
        
        self.add_point_button = QPushButton("Add Point")
        self.add_point_button.setStyleSheet(get_button_style('primary'))
        self.add_point_button.setMinimumWidth(80)
        
        input_layout.addWidget(self.conc_data_input, 1, 0)
        input_layout.addWidget(self.abs_data_input, 1, 1)
        input_layout.addWidget(self.add_point_button, 1, 2)
        
        left_layout.addLayout(input_layout)
        
        # Data table
        self.data_table = QTableWidget(0, 3)
        self.data_table.setHorizontalHeaderLabels(["Concentration (M)", "Absorbance", "Actions"])
        self.data_table.setMaximumHeight(200)
        # Use blue styling to match thermodynamics
        self.data_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #BBDEFB;
                border-radius: 5px;
                background-color: #F5F5F5;
                color: #0D47A1;
                font-weight: bold;
            }
            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        # Fix column widths to prevent user resizing
        header = self.data_table.horizontalHeader()
        header.setSectionResizeMode(0, header.ResizeMode.Stretch)  # Concentration column stretches
        header.setSectionResizeMode(1, header.ResizeMode.Stretch)  # Absorbance column stretches  
        header.setSectionResizeMode(2, header.ResizeMode.Fixed)    # Actions column fixed width
        self.data_table.setColumnWidth(2, 80)  # Set fixed width for Actions column
        
        left_layout.addWidget(self.data_table)
        
        # Data management buttons
        button_layout = QHBoxLayout()
        self.clear_data_button = QPushButton("Clear All")
        self.clear_data_button.setStyleSheet(get_button_style('error'))
        
        self.regression_button = QPushButton("Perform Regression")
        self.regression_button.setStyleSheet(get_button_style('primary'))
        
        button_layout.addWidget(self.clear_data_button)
        button_layout.addWidget(self.regression_button)
        left_layout.addLayout(button_layout)
        
        # Results display
        results_label = QLabel("Regression Results:")
        results_label.setStyleSheet(get_label_style('subtitle'))
        left_layout.addWidget(results_label)
        
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(150)
        self.results_text.setReadOnly(True)
        self.results_text.setStyleSheet(get_text_edit_style())
        left_layout.addWidget(self.results_text)
        
        # Right panel - plot
        right_panel = QGroupBox("Standard Curve")
        right_panel.setStyleSheet(get_group_box_style())
        right_layout = QVBoxLayout(right_panel)
        
        self.curve_plot = MplPlotWidget()
        right_layout.addWidget(self.curve_plot)
        
        # Plot settings
        plot_settings = QHBoxLayout()
        path_label = QLabel("Path Length (cm):")
        path_label.setStyleSheet(get_label_style('subtitle'))
        plot_settings.addWidget(path_label)
        
        self.path_length_input = QDoubleSpinBox()
        self.path_length_input.setRange(0.01, 100)
        self.path_length_input.setDecimals(3)
        self.path_length_input.setValue(1.0)
        self.path_length_input.setStyleSheet(get_input_style())
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
        remove_button.setStyleSheet(get_button_style('error'))
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
        results = {
            "Slope (ε×l)": f"{result.slope:.2e} M⁻¹",
            "Intercept": f"{result.intercept:.4f}",
            "R² Value": f"{result.r_squared:.4f}",
            "Std Error": f"{result.std_error:.2e}"
        }
        
        if result.epsilon is not None:
            results["Calculated ε"] = f"{result.epsilon:.0f} M⁻¹cm⁻¹"
        
        # Determine quality
        quality_info = None
        if result.r_squared > 0.99:
            quality_info = {'quality': 'Excellent'}
        elif result.r_squared > 0.95:
            quality_info = {'quality': 'Good'}
        else:
            quality_info = {'quality': 'Poor'}
        
        html = generate_results_html("Linear Regression Results", results, quality_info)
        self.results_text.setHtml(html)
    
    def _update_curve_plot(self, plot_data):
        """Update the curve plot with data points and regression line"""
        if not plot_data:
            return
            
        try:
            colors = get_html_colors()
            ax = self.curve_plot.figure.clear()
            ax = self.curve_plot.figure.add_subplot(111)
            
            if isinstance(plot_data[0], dict):
                data = plot_data[0]
                
                # Plot data points
                if 'data_points' in data:
                    x_data, y_data = zip(*data['data_points'])
                    ax.scatter(x_data, y_data, c=colors['primary'], s=50, alpha=0.7, label='Data Points')
                
                # Plot regression line
                if 'regression_line' in data and data['regression_line']:
                    x_line, y_line = zip(*data['regression_line'])
                    ax.plot(x_line, y_line, color=colors['error'], linewidth=2, label='Linear Fit')
                    
                ax.legend()
            else:
                # Theoretical curve
                x_data, y_data = zip(*plot_data)
                ax.plot(x_data, y_data, color=colors['success'], linewidth=2, label='Theoretical Curve')
            
            ax.set_xlabel('Concentration (M)')
            ax.set_ylabel('Absorbance')
            ax.set_title('Beer-Lambert Standard Curve')
            ax.grid(True, alpha=0.3)
            
            self.curve_plot.canvas.draw()
            
        except Exception as e:
            print(f"Plot error: {e}")
    
    def _on_error(self, error_msg):
        """Display error message"""
        colors = get_html_colors()
        self.results_text.setHtml(f'<div style="padding: 15px; color: {colors["error"]};"><strong>Error:</strong> {error_msg}</div>')

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
        title_font.setPointSize(16)  # Match thermodynamics font size
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(get_label_style('title'))
        layout.addWidget(title)
        
        # Create tabbed interface
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(get_tab_widget_style())
        
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
                colors = get_html_colors()
                ax = self.calculator_tab.plot.figure.clear()
                ax = self.calculator_tab.plot.figure.add_subplot(111)
                
                x_data, y_data = zip(*plot_data)
                ax.plot(x_data, y_data, color=colors['primary'], linewidth=2)
                ax.set_xlabel('Concentration (M)')
                ax.set_ylabel('Absorbance')
                ax.set_title('Theoretical Beer-Lambert Curve')
                ax.grid(True, alpha=0.3)
                
                self.calculator_tab.plot.canvas.draw()
            except Exception as e:
                print(f"Calculator plot error: {e}")
