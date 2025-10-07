from PySide6.QtCore import QObject, Signal
from typing import List, Optional, Tuple
from ..core.calculators.beer_lambert import (
    BeerLambertInput, CalculationMode, DataPoint, LinearRegressionResult,
    calculate_beer_lambert, linear_regression, generate_standard_curve_points
)

class BeerLambertVM(QObject):
    # Existing signals
    output_changed = Signal(float)
    error = Signal(str)
    
    # New signals for enhanced functionality
    regression_completed = Signal(object)  # LinearRegressionResult
    curve_points_updated = Signal(list)    # List of (x, y) tuples for plotting
    calculation_mode_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._calculation_mode = CalculationMode.ABSORBANCE
        self._data_points: List[DataPoint] = []
        self._path_length: Optional[float] = 1.0  # Default 1 cm cuvette
        
    @property
    def calculation_mode(self) -> CalculationMode:
        return self._calculation_mode
    
    @calculation_mode.setter
    def calculation_mode(self, mode: CalculationMode):
        if self._calculation_mode != mode:
            self._calculation_mode = mode
            self.calculation_mode_changed.emit(mode.value)
    
    @property
    def data_points(self) -> List[DataPoint]:
        return self._data_points.copy()
    
    @property
    def path_length(self) -> Optional[float]:
        return self._path_length
    
    @path_length.setter  
    def path_length(self, value: float):
        if value and value > 0:
            self._path_length = value
    
    def calculate_parameter(self, **kwargs):
        """
        Calculate the target parameter based on current mode.
        
        Expected kwargs depending on mode:
        - ABSORBANCE: epsilon, path_length, concentration
        - CONCENTRATION: absorbance, epsilon, path_length  
        - EPSILON: absorbance, path_length, concentration
        - PATH_LENGTH: absorbance, epsilon, concentration
        """
        try:
            # Create input object with provided parameters
            params = BeerLambertInput(
                epsilon_Minv_cm=kwargs.get('epsilon'),
                path_cm=kwargs.get('path_length'),
                conc_M=kwargs.get('concentration'),
                absorbance=kwargs.get('absorbance')
            )
            
            result = calculate_beer_lambert(params, self._calculation_mode)
            self.output_changed.emit(result)
            
        except Exception as e:
            self.error.emit(str(e))
    
    def add_data_point(self, concentration: float, absorbance: float):
        """Add a data point for standard curve analysis"""
        try:
            if concentration < 0 or absorbance < 0:
                raise ValueError("Concentration and absorbance must be non-negative")
                
            point = DataPoint(concentration=concentration, absorbance=absorbance)
            self._data_points.append(point)
            
            # Update curve visualization
            self._update_curve_visualization()
            
        except Exception as e:
            self.error.emit(str(e))
    
    def remove_data_point(self, index: int):
        """Remove a data point by index"""
        try:
            if 0 <= index < len(self._data_points):
                self._data_points.pop(index)
                self._update_curve_visualization()
        except Exception as e:
            self.error.emit(str(e))
    
    def clear_data_points(self):
        """Clear all data points"""
        self._data_points.clear()
        self.curve_points_updated.emit([])
    
    def perform_linear_regression(self):
        """Perform linear regression on current data points"""
        try:
            if len(self._data_points) < 2:
                raise ValueError("At least 2 data points are required for regression")
            
            result = linear_regression(self._data_points, self._path_length)
            self.regression_completed.emit(result)
            
            # Update curve visualization with regression line
            self._update_curve_visualization(include_regression=True, regression_result=result)
            
        except Exception as e:
            self.error.emit(str(e))
    
    def generate_theoretical_curve(self, epsilon: float, max_concentration: float = None):
        """Generate and display theoretical Beer-Lambert curve"""
        try:
            if not self._path_length or self._path_length <= 0:
                raise ValueError("Path length must be set to generate theoretical curve")
            
            if epsilon <= 0:
                raise ValueError("Epsilon must be positive")
            
            # Default max concentration based on existing data or reasonable value
            if max_concentration is None:
                if self._data_points:
                    max_conc = max(point.concentration for point in self._data_points)
                    max_concentration = max_conc * 1.2  # 20% beyond max data point
                else:
                    max_concentration = 1e-4  # 100 μM default
            
            curve_points = generate_standard_curve_points(
                epsilon=epsilon,
                path_length=self._path_length,
                max_concentration=max_concentration,
                num_points=100
            )
            
            # Convert to (x, y) tuples for plotting
            curve_data = [(point.concentration, point.absorbance) for point in curve_points]
            self.curve_points_updated.emit(curve_data)
            
        except Exception as e:
            self.error.emit(str(e))
    
    def _update_curve_visualization(self, include_regression=False, regression_result=None):
        """Update the curve visualization with current data"""
        if not self._data_points:
            self.curve_points_updated.emit([])
            return
        
        # Prepare data points for plotting
        plot_data = {
            'data_points': [(point.concentration, point.absorbance) for point in self._data_points],
            'regression_line': None
        }
        
        if include_regression and regression_result:
            # Generate regression line points
            x_min = min(point.concentration for point in self._data_points)
            x_max = max(point.concentration for point in self._data_points)
            x_range = x_max - x_min
            
            # Extend line slightly beyond data range
            x_start = max(0, x_min - 0.1 * x_range)
            x_end = x_max + 0.1 * x_range
            
            x_line = [x_start, x_end]
            y_line = [regression_result.slope * x + regression_result.intercept for x in x_line]
            
            plot_data['regression_line'] = list(zip(x_line, y_line))
        
        self.curve_points_updated.emit([plot_data])
    
    # Legacy method for backward compatibility
    def compute(self, epsilon, path, conc):
        """Legacy compute method for backward compatibility"""
        self.calculate_parameter(
            epsilon=epsilon,
            path_length=path,
            concentration=conc
        )
