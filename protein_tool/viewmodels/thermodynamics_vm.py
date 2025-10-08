from PySide6.QtCore import QObject, Signal
from typing import Optional, List
import numpy as np

from ..core.calculators.thermodynamics import (
    ThermodynamicsInput, ThermodynamicsResult, ThermodynamicsMode,
    calculate_thermodynamics, get_thermodynamics_info
)

class ThermodynamicsViewModel(QObject):
    """ViewModel for thermodynamics calculator"""
    
    # Signals
    calculation_completed = Signal(object)  # ThermodynamicsResult
    error = Signal(str)
    plot_data_updated = Signal(object)  # Plot data for visualization
    
    def __init__(self):
        super().__init__()
        self.calculation_mode = ThermodynamicsMode.GIBBS_FREE_ENERGY
        self.last_result: Optional[ThermodynamicsResult] = None
        
    def calculate_parameter(self, **kwargs) -> None:
        """
        Calculate thermodynamic parameter based on current mode
        
        Args:
            **kwargs: Parameters for calculation (delta_G_kJ_mol, delta_H_kJ_mol, etc.)
        """
        try:
            # Create input object
            params = ThermodynamicsInput(**kwargs)
            
            # Perform calculation
            result = calculate_thermodynamics(params, self.calculation_mode)
            
            # Store result and emit signal
            self.last_result = result
            self.calculation_completed.emit(result)
            
        except Exception as e:
            self.error.emit(str(e))
    
    def generate_temperature_plot(self, delta_H: float, delta_S: float, 
                                temp_range: tuple = (200, 400)) -> None:
        """
        Generate ΔG vs T plot for given ΔH and ΔS
        
        Args:
            delta_H: Enthalpy change (kJ/mol)
            delta_S: Entropy change (J/mol·K) 
            temp_range: Temperature range (K) as (min, max)
        """
        try:
            t_min, t_max = temp_range
            temperatures = np.linspace(t_min, t_max, 100)
            
            delta_S_kJ = delta_S / 1000  # Convert to kJ/mol·K
            delta_G_values = delta_H - temperatures * delta_S_kJ
            
            plot_data = {
                'x': temperatures,
                'y': delta_G_values,
                'xlabel': 'Temperature (K)',
                'ylabel': 'ΔG (kJ/mol)',
                'title': f'ΔG vs Temperature\n(ΔH = {delta_H} kJ/mol, ΔS = {delta_S} J/mol·K)',
                'plot_type': 'temperature_dependence'
            }
            
            self.plot_data_updated.emit(plot_data)
            
        except Exception as e:
            self.error.emit(f"Plot generation error: {str(e)}")
    
    def generate_equilibrium_plot(self, delta_G: float, 
                                temp_range: tuple = (200, 400)) -> None:
        """
        Generate K vs T plot for given ΔG
        
        Args:
            delta_G: Gibbs free energy change (kJ/mol)
            temp_range: Temperature range (K) as (min, max)
        """
        try:
            t_min, t_max = temp_range
            temperatures = np.linspace(t_min, t_max, 100)
            
            # K = exp(-ΔG/RT), convert ΔG to J/mol
            delta_G_J = delta_G * 1000
            R = 8.314  # J/(mol·K)
            
            K_values = np.exp(-delta_G_J / (R * temperatures))
            
            plot_data = {
                'x': temperatures,
                'y': K_values,
                'xlabel': 'Temperature (K)',
                'ylabel': 'Equilibrium Constant (K)',
                'title': f'Equilibrium Constant vs Temperature\n(ΔG = {delta_G} kJ/mol)',
                'plot_type': 'equilibrium_temperature',
                'log_scale_y': True  # K can vary over many orders of magnitude
            }
            
            self.plot_data_updated.emit(plot_data)
            
        except Exception as e:
            self.error.emit(f"Plot generation error: {str(e)}")
    
    def generate_van_hoff_plot(self, data_points: List[tuple]) -> None:
        """
        Generate van't Hoff plot (ln(K) vs 1/T) for determining ΔH and ΔS
        
        Args:
            data_points: List of (temperature_K, equilibrium_constant) tuples
        """
        try:
            if len(data_points) < 2:
                raise ValueError("At least 2 data points required for van't Hoff plot")
            
            temperatures, K_values = zip(*data_points)
            
            # Convert to arrays
            T_array = np.array(temperatures)
            K_array = np.array(K_values)
            
            # Check for positive values
            if np.any(T_array <= 0) or np.any(K_array <= 0):
                raise ValueError("Temperature and equilibrium constant must be positive")
            
            # Calculate 1/T and ln(K)
            inv_T = 1 / T_array
            ln_K = np.log(K_array)
            
            # Perform linear regression: ln(K) = -ΔH/R * (1/T) + ΔS/R
            slope, intercept = np.polyfit(inv_T, ln_K, 1)
            
            # Calculate thermodynamic parameters
            R = 8.314  # J/(mol·K)
            delta_H = -slope * R / 1000  # Convert to kJ/mol
            delta_S = intercept * R      # J/mol·K
            
            # Generate regression line
            inv_T_line = np.linspace(inv_T.min(), inv_T.max(), 100)
            ln_K_line = slope * inv_T_line + intercept
            
            plot_data = {
                'data_points': list(zip(inv_T, ln_K)),
                'regression_line': list(zip(inv_T_line, ln_K_line)),
                'xlabel': '1/T (K⁻¹)',
                'ylabel': 'ln(K)',
                'title': 'van\'t Hoff Plot',
                'plot_type': 'van_hoff',
                'results': {
                    'slope': slope,
                    'intercept': intercept,
                    'delta_H': delta_H,
                    'delta_S': delta_S,
                    'r_squared': self._calculate_r_squared(ln_K, slope * inv_T + intercept)
                }
            }
            
            self.plot_data_updated.emit(plot_data)
            
        except Exception as e:
            self.error.emit(f"van't Hoff plot error: {str(e)}")
    
    def _calculate_r_squared(self, y_actual, y_predicted) -> float:
        """Calculate R² for regression analysis"""
        ss_res = np.sum((y_actual - y_predicted) ** 2)
        ss_tot = np.sum((y_actual - np.mean(y_actual)) ** 2)
        return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    def get_info(self) -> dict:
        """Get information about thermodynamics calculations"""
        return get_thermodynamics_info()
