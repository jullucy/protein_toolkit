from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np
from enum import Enum

class CalculationMode(Enum):
    """Different calculation modes for Beer-Lambert law"""
    ABSORBANCE = "absorbance"           # A = ε * l * c
    CONCENTRATION = "concentration"     # c = A / (ε * l)
    EPSILON = "epsilon"                 # ε = A / (l * c)
    PATH_LENGTH = "path_length"         # l = A / (ε * c)

@dataclass
class BeerLambertInput:
    epsilon_Minv_cm: Optional[float] = None  # molar absorptivity (M^-1 cm^-1)
    path_cm: Optional[float] = None          # path length (cm)
    conc_M: Optional[float] = None           # concentration (M)
    absorbance: Optional[float] = None       # absorbance (unitless)

@dataclass
class DataPoint:
    """Single data point for standard curve analysis"""
    concentration: float  # M
    absorbance: float     # unitless

@dataclass
class LinearRegressionResult:
    """Results from linear regression analysis"""
    slope: float           # ε * l (if x=concentration, y=absorbance)
    intercept: float       # y-intercept
    r_squared: float       # coefficient of determination
    std_error: float       # standard error of the slope
    epsilon: Optional[float] = None  # calculated ε (if path length known)

def calculate_beer_lambert(params: BeerLambertInput, mode: CalculationMode) -> float:
    """
    Calculate any parameter of Beer-Lambert law given the others.
    
    Beer-Lambert Law: A = ε * l * c
    Where:
    - A = absorbance (unitless)
    - ε = molar absorptivity (M^-1 cm^-1)
    - l = path length (cm)  
    - c = concentration (M)
    
    Args:
        params: BeerLambertInput with known parameters
        mode: Which parameter to calculate
        
    Returns:
        Calculated parameter value
        
    Raises:
        ValueError: If required parameters are missing or invalid
    """
    
    if mode == CalculationMode.ABSORBANCE:
        if any(x is None for x in [params.epsilon_Minv_cm, params.path_cm, params.conc_M]):
            raise ValueError("Epsilon, path length, and concentration are required to calculate absorbance")
        if any(x <= 0 for x in [params.epsilon_Minv_cm, params.path_cm, params.conc_M]):
            raise ValueError("All parameters must be positive")
        return params.epsilon_Minv_cm * params.path_cm * params.conc_M
    
    elif mode == CalculationMode.CONCENTRATION:
        if any(x is None for x in [params.absorbance, params.epsilon_Minv_cm, params.path_cm]):
            raise ValueError("Absorbance, epsilon, and path length are required to calculate concentration")
        if params.epsilon_Minv_cm <= 0 or params.path_cm <= 0:
            raise ValueError("Epsilon and path length must be positive")
        if params.absorbance < 0:
            raise ValueError("Absorbance cannot be negative")
        return params.absorbance / (params.epsilon_Minv_cm * params.path_cm)
    
    elif mode == CalculationMode.EPSILON:
        if any(x is None for x in [params.absorbance, params.path_cm, params.conc_M]):
            raise ValueError("Absorbance, path length, and concentration are required to calculate epsilon")
        if params.path_cm <= 0 or params.conc_M <= 0:
            raise ValueError("Path length and concentration must be positive")
        if params.absorbance < 0:
            raise ValueError("Absorbance cannot be negative")
        return params.absorbance / (params.path_cm * params.conc_M)
    
    elif mode == CalculationMode.PATH_LENGTH:
        if any(x is None for x in [params.absorbance, params.epsilon_Minv_cm, params.conc_M]):
            raise ValueError("Absorbance, epsilon, and concentration are required to calculate path length")
        if params.epsilon_Minv_cm <= 0 or params.conc_M <= 0:
            raise ValueError("Epsilon and concentration must be positive")
        if params.absorbance < 0:
            raise ValueError("Absorbance cannot be negative")
        return params.absorbance / (params.epsilon_Minv_cm * params.conc_M)
    
    else:
        raise ValueError(f"Unknown calculation mode: {mode}")

def linear_regression(data_points: List[DataPoint], path_length: Optional[float] = None) -> LinearRegressionResult:
    """
    Perform linear regression on concentration vs absorbance data.
    
    Fits the line: A = m*c + b
    Where slope m = ε * l (if path length is known, ε can be calculated)
    
    Args:
        data_points: List of (concentration, absorbance) points
        path_length: Optional path length in cm to calculate epsilon
        
    Returns:
        LinearRegressionResult with regression statistics
        
    Raises:
        ValueError: If insufficient data points or invalid data
    """
    if len(data_points) < 2:
        raise ValueError("At least 2 data points are required for linear regression")
    
    # Extract x (concentration) and y (absorbance) values
    x = np.array([point.concentration for point in data_points])
    y = np.array([point.absorbance for point in data_points])
    
    # Validate data
    if np.any(x < 0) or np.any(y < 0):
        raise ValueError("Concentrations and absorbances must be non-negative")
    
    if len(np.unique(x)) < 2:
        raise ValueError("Need at least 2 different concentration values")
    
    # Perform linear regression
    n = len(x)
    
    # Calculate slope and intercept
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    
    numerator = np.sum((x - x_mean) * (y - y_mean))
    denominator = np.sum((x - x_mean) ** 2)
    
    if denominator == 0:
        raise ValueError("Cannot perform regression: all x values are identical")
    
    slope = numerator / denominator
    intercept = y_mean - slope * x_mean
    
    # Calculate R-squared
    y_pred = slope * x + intercept
    ss_res = np.sum((y - y_pred) ** 2)  # Sum of squares of residuals
    ss_tot = np.sum((y - y_mean) ** 2)  # Total sum of squares
    
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    # Calculate standard error of the slope
    if n > 2:
        mse = ss_res / (n - 2)  # Mean squared error
        std_error = np.sqrt(mse / denominator)
    else:
        std_error = 0
    
    # Calculate epsilon if path length is provided
    epsilon = slope / path_length if path_length and path_length > 0 else None
    
    return LinearRegressionResult(
        slope=slope,
        intercept=intercept,
        r_squared=r_squared,
        std_error=std_error,
        epsilon=epsilon
    )

def generate_standard_curve_points(epsilon: float, path_length: float, 
                                 max_concentration: float, num_points: int = 20) -> List[DataPoint]:
    """
    Generate theoretical standard curve points for visualization.
    
    Args:
        epsilon: Molar absorptivity (M^-1 cm^-1)
        path_length: Path length (cm)
        max_concentration: Maximum concentration for the curve (M)
        num_points: Number of points to generate
        
    Returns:
        List of DataPoint objects representing the theoretical curve
    """
    concentrations = np.linspace(0, max_concentration, num_points)
    data_points = []
    
    for conc in concentrations:
        abs_val = epsilon * path_length * conc
        data_points.append(DataPoint(concentration=conc, absorbance=abs_val))
    
    return data_points

# Backward compatibility functions
def absorbance(x: BeerLambertInput) -> float:
    """Legacy function for backward compatibility"""
    if x.epsilon_Minv_cm is None or x.path_cm is None or x.conc_M is None:
        raise ValueError("Missing required parameters for absorbance calculation")
    return calculate_beer_lambert(x, CalculationMode.ABSORBANCE)
