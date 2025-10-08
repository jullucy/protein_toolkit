from PySide6.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QDoubleSpinBox, QLabel, QGroupBox, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QTextEdit, QScrollArea,
    QFrame, QGridLayout, QSpinBox, QCheckBox, QHeaderView
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
from ...core.calculators.thermodynamics import ThermodynamicsMode

class TheoryPanel(QScrollArea):
    """Panel displaying thermodynamics theory and information"""
    
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
        params_group = QGroupBox("Thermodynamic Parameters")
        params_group.setStyleSheet(get_group_box_style())
        params_layout = QVBoxLayout(params_group)
        
        params_text = QTextEdit()
        params_text.setReadOnly(True)
        params_text.setMaximumHeight(250)
        params_text.setStyleSheet(get_text_edit_style())
        params_text.setHtml(self._get_parameters_html())
        
        params_layout.addWidget(params_text)
        
        # Applications
        apps_group = QGroupBox("Applications in Protein Science")
        apps_group.setStyleSheet(get_group_box_style())
        apps_layout = QVBoxLayout(apps_group)
        
        apps_text = QTextEdit()
        apps_text.setReadOnly(True)
        apps_text.setMaximumHeight(200)
        apps_text.setStyleSheet(get_text_edit_style())
        apps_text.setHtml(self._get_applications_html())
        
        apps_layout.addWidget(apps_text)
        
        layout.addWidget(theory_text)
        layout.addWidget(params_group)
        layout.addWidget(apps_group)
        layout.addStretch()
        
        self.setWidget(content)
    
    def _get_theory_html(self):
        return """
        <h2 style="color: #1565C0;">Chemical Thermodynamics</h2>

        <p>Thermodynamics governs the spontaneity and equilibrium of chemical reactions, including protein folding, binding, and enzymatic processes.</p>

        <h3 style="color: #1976D2;">Fundamental Equations</h3>
        
        <div style="background: #2F2F2F; padding: 15px; border-radius: 5px; border-left: 4px solid #2196F3;">
        <p><strong>Gibbs-Helmholtz Equation:</strong></p>
        <p style="font-size: 16px;"><strong>ΔG = ΔH - TΔS</strong></p>
        
        <p><strong>Equilibrium Relationship:</strong></p>
        <p style="font-size: 16px;"><strong>ΔG = -RT ln(K)</strong></p>
        
        <p><strong>van't Hoff Equation:</strong></p>
        <p style="font-size: 16px;"><strong>ln(K) = -ΔH/RT + ΔS/R</strong></p>
        </div>

        <h3 style="color: #1976D2;">Physical Meaning</h3>
        <ul>
            <li><strong>ΔG < 0:</strong> Spontaneous process (thermodynamically favorable)</li>
            <li><strong>ΔG = 0:</strong> System at equilibrium</li>
            <li><strong>ΔG > 0:</strong> Non-spontaneous process (requires energy input)</li>
            <li><strong>ΔH:</strong> Heat absorbed/released during reaction</li>
            <li><strong>ΔS:</strong> Change in system disorder/entropy</li>
        </ul>
        """
    
    def _get_parameters_html(self):
        return """
        <table style="width: 100%; border-collapse: collapse; border-radius: 5px; overflow: hidden;">
        <tr style="background: #1976D2; color: white;">
            <th style="padding: 12px; border: none;">Parameter</th>
            <th style="padding: 12px; border: none;">Symbol</th>
            <th style="padding: 12px; border: none;">Units</th>
            <th style="padding: 12px; border: none;">Typical Range</th>
        </tr>
        <tr style="background: #2F2F2F; color: #BBDEFB;">
            <td style="padding: 10px; border: none;"><strong>Gibbs Free Energy</strong></td>
            <td style="padding: 10px; border: none;">ΔG</td>
            <td style="padding: 10px; border: none;">kJ/mol</td>
            <td style="padding: 10px; border: none;">-100 to +100</td>
        </tr>
        <tr style="background: #424242; color: #BBDEFB;">
            <td style="padding: 10px; border: none;"><strong>Enthalpy</strong></td>
            <td style="padding: 10px; border: none;">ΔH</td>
            <td style="padding: 10px; border: none;">kJ/mol</td>
            <td style="padding: 10px; border: none;">-200 to +200</td>
        </tr>
        <tr style="background: #2F2F2F; color: #BBDEFB;">
            <td style="padding: 10px; border: none;"><strong>Entropy</strong></td>
            <td style="padding: 10px; border: none;">ΔS</td>
            <td style="padding: 10px; border: none;">J/mol·K</td>
            <td style="padding: 10px; border: none;">-500 to +500</td>
        </tr>
        <tr style="background: #424242; color: #BBDEFB;">
            <td style="padding: 10px; border: none;"><strong>Temperature</strong></td>
            <td style="padding: 10px; border: none;">T</td>
            <td style="padding: 10px; border: none;">K (°C)</td>
            <td style="padding: 10px; border: none;">273-373 (0-100°C)</td>
        </tr>
        <tr style="background: #2F2F2F; color: #BBDEFB;">
            <td style="padding: 10px; border: none;"><strong>Equilibrium Constant</strong></td>
            <td style="padding: 10px; border: none;">K</td>
            <td style="padding: 10px; border: none;">dimensionless</td>
            <td style="padding: 10px; border: none;">10⁻¹⁰ to 10¹⁰</td>
        </tr>
        </table>
        """
    
    def _get_applications_html(self):
        return """
        <ul>
            <li><strong>Protein Folding:</strong> Calculate folding energetics and stability</li>
            <li><strong>Ligand Binding:</strong> Determine binding affinity and thermodynamics</li>
            <li><strong>Enzyme Catalysis:</strong> Analyze activation barriers and equilibria</li>
            <li><strong>Phase Transitions:</strong> Protein denaturation and aggregation</li>
            <li><strong>Drug Design:</strong> Optimize binding thermodynamics</li>
            <li><strong>Allosteric Effects:</strong> Cooperative binding and regulation</li>
        </ul>
        """

class CalculatorTab(QWidget):
    """Tab for thermodynamic parameter calculations"""
    
    def __init__(self, vm):
        super().__init__()
        self.vm = vm
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        layout = QHBoxLayout()
        
        # Left panel - inputs
        left_panel = QGroupBox("Calculation Parameters")
        left_panel.setStyleSheet(get_group_box_style())
        left_layout = QFormLayout(left_panel)
        
        # Calculation mode selector
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "Calculate ΔG (Gibbs Free Energy)",
            "Calculate ΔH (Enthalpy)", 
            "Calculate ΔS (Entropy)",
            "Calculate T (Temperature)",
            "Calculate K (Equilibrium Constant)",
            "Calculate ΔG from K and T"
        ])
        self.mode_combo.setStyleSheet(get_input_style())
        left_layout.addRow("Calculate:", self.mode_combo)
        
        # Add separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        left_layout.addRow(line)
        
        # Input fields
        self.delta_G_input = QDoubleSpinBox()
        self.delta_G_input.setRange(-1000, 1000)
        self.delta_G_input.setDecimals(2)
        self.delta_G_input.setSuffix(" kJ/mol")
        self.delta_G_input.setStyleSheet(get_input_style())
        
        self.delta_H_input = QDoubleSpinBox()
        self.delta_H_input.setRange(-1000, 1000)
        self.delta_H_input.setDecimals(2)
        self.delta_H_input.setSuffix(" kJ/mol")
        self.delta_H_input.setStyleSheet(get_input_style())
        
        self.delta_S_input = QDoubleSpinBox()
        self.delta_S_input.setRange(-2000, 2000)
        self.delta_S_input.setDecimals(1)
        self.delta_S_input.setSuffix(" J/mol·K")
        self.delta_S_input.setStyleSheet(get_input_style())
        
        self.temp_K_input = QDoubleSpinBox()
        self.temp_K_input.setRange(0, 1000)
        self.temp_K_input.setDecimals(1)
        self.temp_K_input.setValue(298.15)  # Room temperature
        self.temp_K_input.setSuffix(" K")
        self.temp_K_input.setStyleSheet(get_input_style())
        
        self.temp_C_input = QDoubleSpinBox()
        self.temp_C_input.setRange(-273, 727)
        self.temp_C_input.setDecimals(1)
        self.temp_C_input.setValue(25.0)  # Room temperature
        self.temp_C_input.setSuffix(" °C")
        self.temp_C_input.setStyleSheet(get_input_style())
        
        self.K_input = QDoubleSpinBox()
        self.K_input.setRange(1e-15, 1e15)
        self.K_input.setDecimals(3)
        self.K_input.setValue(1.0)
        self.K_input.setStyleSheet(get_input_style())
        
        left_layout.addRow("ΔG (Gibbs Free Energy):", self.delta_G_input)
        left_layout.addRow("ΔH (Enthalpy):", self.delta_H_input)
        left_layout.addRow("ΔS (Entropy):", self.delta_S_input)
        left_layout.addRow("Temperature (K):", self.temp_K_input)
        left_layout.addRow("Temperature (°C):", self.temp_C_input)
        left_layout.addRow("Equilibrium Constant:", self.K_input)
        
        # Calculate button
        self.calc_button = QPushButton("Calculate")
        self.calc_button.setStyleSheet(get_button_style('primary'))
        left_layout.addRow(self.calc_button)
        
        # Result display
        self.result_label = QLabel("Result will appear here")
        self.result_label.setStyleSheet(get_label_style('normal'))
        self.result_label.setWordWrap(True)
        left_layout.addRow("Result:", self.result_label)
        
        # Right panel - visualization
        right_panel = QGroupBox("Visualization")
        right_panel.setStyleSheet(get_group_box_style())
        right_layout = QVBoxLayout(right_panel)
        
        self.plot = MplPlotWidget()
        right_layout.addWidget(self.plot)
        
        # Plot controls
        plot_controls = QVBoxLayout()
        
        # Temperature range for plots
        temp_range_layout = QHBoxLayout()
        temp_range_layout.addWidget(QLabel("T range:"))
        
        self.temp_min_input = QDoubleSpinBox()
        self.temp_min_input.setRange(0, 1000)
        self.temp_min_input.setValue(273)
        self.temp_min_input.setSuffix(" K")
        self.temp_min_input.setStyleSheet(get_input_style())
        temp_range_layout.addWidget(self.temp_min_input)
        
        temp_range_layout.addWidget(QLabel("to"))
        
        self.temp_max_input = QDoubleSpinBox()
        self.temp_max_input.setRange(0, 1000)
        self.temp_max_input.setValue(373)
        self.temp_max_input.setSuffix(" K")
        self.temp_max_input.setStyleSheet(get_input_style())
        temp_range_layout.addWidget(self.temp_max_input)
        
        plot_controls.addLayout(temp_range_layout)
        
        # Plot buttons
        plot_buttons = QHBoxLayout()
        
        self.plot_temp_button = QPushButton("Plot ΔG vs T")
        self.plot_temp_button.setStyleSheet(get_button_style('secondary'))
        plot_buttons.addWidget(self.plot_temp_button)
        
        self.plot_keq_button = QPushButton("Plot K vs T")
        self.plot_keq_button.setStyleSheet(get_button_style('secondary'))
        plot_buttons.addWidget(self.plot_keq_button)
        
        plot_controls.addLayout(plot_buttons)
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
        self.plot_temp_button.clicked.connect(self._plot_temperature_dependence)
        self.plot_keq_button.clicked.connect(self._plot_equilibrium_temperature)
        
        # Temperature conversion
        self.temp_K_input.valueChanged.connect(self._update_celsius)
        self.temp_C_input.valueChanged.connect(self._update_kelvin)
        
        self.vm.calculation_completed.connect(self._on_result_calculated)
        self.vm.error.connect(self._on_error)
        self.vm.plot_data_updated.connect(self._update_plot)
    
    def _on_mode_changed(self):
        mode_index = self.mode_combo.currentIndex()
        modes = [
            ThermodynamicsMode.GIBBS_FREE_ENERGY,
            ThermodynamicsMode.ENTHALPY,
            ThermodynamicsMode.ENTROPY,
            ThermodynamicsMode.TEMPERATURE,
            ThermodynamicsMode.EQUILIBRIUM_CONSTANT,
            ThermodynamicsMode.GIBBS_FROM_KEQR
        ]
        
        self.vm.calculation_mode = modes[mode_index]
        self._update_input_states()
    
    def _update_input_states(self):
        """Enable/disable input fields based on calculation mode"""
        mode = self.vm.calculation_mode
        
        # Reset all to enabled
        inputs = [self.delta_G_input, self.delta_H_input, self.delta_S_input, 
                 self.temp_K_input, self.temp_C_input, self.K_input]
        for input_widget in inputs:
            input_widget.setEnabled(True)
            input_widget.setStyleSheet(get_input_style())
        
        # Disable the field being calculated
        if mode == ThermodynamicsMode.GIBBS_FREE_ENERGY:
            self.delta_G_input.setEnabled(False)
            self.delta_G_input.setStyleSheet(get_input_highlighted_style())
        elif mode == ThermodynamicsMode.ENTHALPY:
            self.delta_H_input.setEnabled(False)
            self.delta_H_input.setStyleSheet(get_input_highlighted_style())
        elif mode == ThermodynamicsMode.ENTROPY:
            self.delta_S_input.setEnabled(False)
            self.delta_S_input.setStyleSheet(get_input_highlighted_style())
        elif mode == ThermodynamicsMode.TEMPERATURE:
            self.temp_K_input.setEnabled(False)
            self.temp_C_input.setEnabled(False)
            self.temp_K_input.setStyleSheet(get_input_highlighted_style())
            self.temp_C_input.setStyleSheet(get_input_highlighted_style())
        elif mode == ThermodynamicsMode.EQUILIBRIUM_CONSTANT:
            self.K_input.setEnabled(False)
            self.K_input.setStyleSheet(get_input_highlighted_style())
        elif mode == ThermodynamicsMode.GIBBS_FROM_KEQR:
            self.delta_G_input.setEnabled(False)
            self.delta_G_input.setStyleSheet(get_input_highlighted_style())
    
    def _update_celsius(self):
        """Update Celsius value when Kelvin changes"""
        kelvin = self.temp_K_input.value()
        celsius = kelvin - 273.15
        self.temp_C_input.blockSignals(True)
        self.temp_C_input.setValue(celsius)
        self.temp_C_input.blockSignals(False)
    
    def _update_kelvin(self):
        """Update Kelvin value when Celsius changes"""
        celsius = self.temp_C_input.value()
        kelvin = celsius + 273.15
        self.temp_K_input.blockSignals(True)
        self.temp_K_input.setValue(kelvin)
        self.temp_K_input.blockSignals(False)
    
    def _calculate(self):
        """Perform calculation based on current mode"""
        try:
            kwargs = {
                'delta_G_kJ_mol': self.delta_G_input.value() if self.delta_G_input.isEnabled() else None,
                'delta_H_kJ_mol': self.delta_H_input.value() if self.delta_H_input.isEnabled() else None,
                'delta_S_J_mol_K': self.delta_S_input.value() if self.delta_S_input.isEnabled() else None,
                'temperature_K': self.temp_K_input.value() if self.temp_K_input.isEnabled() else None,
                'equilibrium_constant': self.K_input.value() if self.K_input.isEnabled() else None
            }
            
            # Remove None values
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            
            self.vm.calculate_parameter(**kwargs)
            
        except Exception as e:
            self._on_error(str(e))
    
    def _on_result_calculated(self, result):
        """Display calculation result"""
        text = f"{result.calculated_value:.3f} {result.units}\n"
        text += f"Equation: {result.equation_used}"
        
        self.result_label.setText(text)
        self.result_label.setStyleSheet(get_label_style('result_success'))
        
        # Update the corresponding input field
        mode = result.calculation_mode
        if mode == ThermodynamicsMode.GIBBS_FREE_ENERGY:
            self.delta_G_input.setValue(result.calculated_value)
        elif mode == ThermodynamicsMode.ENTHALPY:
            self.delta_H_input.setValue(result.calculated_value)
        elif mode == ThermodynamicsMode.ENTROPY:
            self.delta_S_input.setValue(result.calculated_value)
        elif mode == ThermodynamicsMode.TEMPERATURE:
            self.temp_K_input.setValue(result.calculated_value)
            self._update_celsius()
        elif mode == ThermodynamicsMode.EQUILIBRIUM_CONSTANT:
            self.K_input.setValue(result.calculated_value)
        elif mode == ThermodynamicsMode.GIBBS_FROM_KEQR:
            self.delta_G_input.setValue(result.calculated_value)
    
    def _on_error(self, error_msg):
        """Display error message"""
        self.result_label.setText(f"Error: {error_msg}")
        self.result_label.setStyleSheet(get_label_style('result_error'))
    
    def _plot_temperature_dependence(self):
        """Plot ΔG vs Temperature"""
        delta_H = self.delta_H_input.value()
        delta_S = self.delta_S_input.value()
        temp_range = (self.temp_min_input.value(), self.temp_max_input.value())
        
        self.vm.generate_temperature_plot(delta_H, delta_S, temp_range)
    
    def _plot_equilibrium_temperature(self):
        """Plot K vs Temperature"""
        delta_G = self.delta_G_input.value()
        temp_range = (self.temp_min_input.value(), self.temp_max_input.value())
        
        self.vm.generate_equilibrium_plot(delta_G, temp_range)
    
    def _update_plot(self, plot_data):
        """Update the plot with new data"""
        try:
            ax = self.plot.figure.clear()
            ax = self.plot.figure.add_subplot(111)
            
            x_data = plot_data['x']
            y_data = plot_data['y']
            
            ax.plot(x_data, y_data, 'b-', linewidth=2)
            ax.set_xlabel(plot_data['xlabel'])
            ax.set_ylabel(plot_data['ylabel'])
            ax.set_title(plot_data['title'])
            ax.grid(True, alpha=0.3)
            
            # Set log scale if requested
            if plot_data.get('log_scale_y', False):
                ax.set_yscale('log')
            
            self.plot.canvas.draw()
            
        except Exception as e:
            print(f"Plot error: {e}")

class VanHoffTab(QWidget):
    """Tab for van't Hoff analysis"""
    
    def __init__(self, vm):
        super().__init__()
        self.vm = vm
        self.data_points = []
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        layout = QHBoxLayout()
        
        # Left panel - data input
        left_panel = QGroupBox("Experimental Data")
        left_panel.setStyleSheet(get_group_box_style())
        left_layout = QVBoxLayout(left_panel)
        
        # Data input
        input_layout = QGridLayout()
        input_layout.addWidget(QLabel("Temperature (K):"), 0, 0)
        input_layout.addWidget(QLabel("Equilibrium Constant:"), 0, 1)
        
        self.temp_data_input = QDoubleSpinBox()
        self.temp_data_input.setRange(200, 500)
        self.temp_data_input.setDecimals(1)
        self.temp_data_input.setValue(298.15)
        self.temp_data_input.setStyleSheet(get_input_style())
        
        self.K_data_input = QDoubleSpinBox()
        self.K_data_input.setRange(1e-15, 1e15)
        self.K_data_input.setDecimals(6)
        self.K_data_input.setValue(1.0)
        self.K_data_input.setStyleSheet(get_input_style())
        
        self.add_point_button = QPushButton("Add Point")
        self.add_point_button.setStyleSheet(get_button_style('primary'))
        
        input_layout.addWidget(self.temp_data_input, 1, 0)
        input_layout.addWidget(self.K_data_input, 1, 1)
        input_layout.addWidget(self.add_point_button, 1, 2)
        
        left_layout.addLayout(input_layout)
        
        # Data table
        self.data_table = QTableWidget(0, 3)
        self.data_table.setHorizontalHeaderLabels(["Temperature (K)", "K", "Actions"])
        self.data_table.setMaximumHeight(200)
        # Use blue styling to match Beer-Lambert
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
        header.setSectionResizeMode(0, header.ResizeMode.Stretch)  # Temperature column stretches
        header.setSectionResizeMode(1, header.ResizeMode.Stretch)  # K column stretches  
        header.setSectionResizeMode(2, header.ResizeMode.Fixed)    # Actions column fixed width
        self.data_table.setColumnWidth(2, 80)  # Set fixed width for Actions column
        
        left_layout.addWidget(self.data_table)
        
        # Analysis buttons
        button_layout = QHBoxLayout()
        self.clear_data_button = QPushButton("Clear All")
        self.clear_data_button.setStyleSheet(get_button_style('error'))
        
        self.analyze_button = QPushButton("Analyze Data")
        self.analyze_button.setStyleSheet(get_button_style('primary'))
        
        button_layout.addWidget(self.clear_data_button)
        button_layout.addWidget(self.analyze_button)
        left_layout.addLayout(button_layout)
        
        # Results display
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(200)
        self.results_text.setReadOnly(True)
        self.results_text.setStyleSheet(get_text_edit_style())
        left_layout.addWidget(QLabel("Analysis Results:"))
        left_layout.addWidget(self.results_text)
        
        # Right panel - plot
        right_panel = QGroupBox("van't Hoff Plot")
        right_panel.setStyleSheet(get_group_box_style())
        right_layout = QVBoxLayout(right_panel)
        
        self.vanhoff_plot = MplPlotWidget()
        right_layout.addWidget(self.vanhoff_plot)
        
        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)
        self.setLayout(layout)
    
    def connect_signals(self):
        self.add_point_button.clicked.connect(self._add_data_point)
        self.clear_data_button.clicked.connect(self._clear_all_data)
        self.analyze_button.clicked.connect(self._analyze_data)
        
        self.vm.plot_data_updated.connect(self._update_vanhoff_plot)
        self.vm.error.connect(self._on_error)
    
    def _add_data_point(self):
        """Add a new data point"""
        temp = self.temp_data_input.value()
        K_val = self.K_data_input.value()
        
        # Add to internal list
        self.data_points.append((temp, K_val))
        
        # Add to table
        row = self.data_table.rowCount()
        self.data_table.insertRow(row)
        
        self.data_table.setItem(row, 0, QTableWidgetItem(f"{temp:.1f}"))
        self.data_table.setItem(row, 1, QTableWidgetItem(f"{K_val:.2e}"))
        
        # Add remove button
        remove_button = QPushButton("Remove")
        remove_button.setStyleSheet(get_button_style('error'))
        remove_button.clicked.connect(lambda: self._remove_data_point(row))
        self.data_table.setCellWidget(row, 2, remove_button)
        
        # Clear inputs
        self.temp_data_input.setValue(298.15)
        self.K_data_input.setValue(1.0)
    
    def _remove_data_point(self, row):
        """Remove a data point"""
        if 0 <= row < len(self.data_points):
            self.data_points.pop(row)
            self.data_table.removeRow(row)
    
    def _clear_all_data(self):
        """Clear all data points"""
        self.data_points.clear()
        self.data_table.setRowCount(0)
        self.results_text.clear()
    
    def _analyze_data(self):
        """Perform van't Hoff analysis"""
        if len(self.data_points) < 2:
            self._on_error("Need at least 2 data points for analysis")
            return
        
        self.vm.generate_van_hoff_plot(self.data_points)
    
    def _update_vanhoff_plot(self, plot_data):
        """Update the van't Hoff plot"""
        if plot_data.get('plot_type') != 'van_hoff':
            return
            
        try:
            ax = self.vanhoff_plot.figure.clear()
            ax = self.vanhoff_plot.figure.add_subplot(111)
            
            # Plot data points
            if 'data_points' in plot_data:
                x_data, y_data = zip(*plot_data['data_points'])
                ax.scatter(x_data, y_data, c='blue', s=50, alpha=0.7, label='Data Points')
            
            # Plot regression line
            if 'regression_line' in plot_data:
                x_line, y_line = zip(*plot_data['regression_line'])
                ax.plot(x_line, y_line, 'r-', linewidth=2, label='Linear Fit')
            
            ax.set_xlabel(plot_data['xlabel'])
            ax.set_ylabel(plot_data['ylabel'])
            ax.set_title(plot_data['title'])
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            self.vanhoff_plot.canvas.draw()
            
            # Display results
            if 'results' in plot_data:
                results = plot_data['results']
                html = f"""
                <div style="background: #2F2F2F; padding: 10px; border-radius: 5px; border-left: 4px solid #2196F3;">
                <h3 style="color: #1565C0; margin-top: 0;">van't Hoff Analysis Results</h3>
                <table style="width: 100%; background: #424242; border-radius: 3px; color: #BBDEFB;">
                <tr style="background: #1976D2; color: white;"><td style="padding: 6px;"><strong>ΔH (from slope):</strong></td><td style="padding: 6px;">{results['delta_H']:.2f} kJ/mol</td></tr>
                <tr><td style="padding: 6px;"><strong>ΔS (from intercept):</strong></td><td style="padding: 6px;">{results['delta_S']:.1f} J/mol·K</td></tr>
                <tr style="background: #1976D2; color: white;"><td style="padding: 6px;"><strong>R² Value:</strong></td><td style="padding: 6px;">{results['r_squared']:.4f}</td></tr>
                </table>
                </div>
                """
                self.results_text.setHtml(html)
            
        except Exception as e:
            print(f"van't Hoff plot error: {e}")
    
    def _on_error(self, error_msg):
        """Display error message"""
        self.results_text.setHtml(f'<div style="background: #F44336; padding: 10px; border-radius: 5px; border-left: 4px solid #D32F2F;"><p style="color: white; margin: 0;"><strong>Error:</strong> {error_msg}</p></div>')

class ThermodynamicsView(QWidget):
    """Main thermodynamics calculator view with tabbed interface"""
    
    def __init__(self, vm):
        super().__init__()
        self.vm = vm
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setStyleSheet(get_main_widget_style())
        
        # Title - matched font size (16) with Beer-Lambert
        title = QLabel("Thermodynamics Calculator")
        title_font = QFont()
        title_font.setPointSize(16)  # Match Beer-Lambert font size
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
        
        # van't Hoff analysis tab  
        self.vanhoff_tab = VanHoffTab(self.vm)
        self.tab_widget.addTab(self.vanhoff_tab, "van't Hoff Analysis")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
