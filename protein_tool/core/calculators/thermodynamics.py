from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np
from enum import Enum
import math

class ThermodynamicsMode(Enum):
    """Different calculation modes for thermodynamics"""
    GIBBS_FREE_ENERGY = "gibbs_free_energy"     # ΔG = ΔH - TΔS
    ENTHALPY = "enthalpy"                       # ΔH = ΔG + TΔS
    ENTROPY = "entropy"                         # ΔS = (ΔH - ΔG) / T
    TEMPERATURE = "temperature"                 # T = (ΔH - ΔG) / ΔS
    EQUILIBRIUM_CONSTANT = "equilibrium_constant" # K = exp(-ΔG/RT)
    GIBBS_FROM_KEQR = "gibbs_from_keq"         # ΔG = -RT ln(K)

@dataclass
class ThermodynamicsInput:
    """Input parameters for thermodynamics calculations"""
    delta_G_kJ_mol: Optional[float] = None      # Gibbs free energy change (kJ/mol)
    delta_H_kJ_mol: Optional[float] = None      # Enthalpy change (kJ/mol)
    delta_S_J_mol_K: Optional[float] = None     # Entropy change (J/mol·K)
    temperature_K: Optional[float] = None       # Temperature (K)
    temperature_C: Optional[float] = None       # Temperature (°C) - will convert to K
    equilibrium_constant: Optional[float] = None # Equilibrium constant K
    
    def __post_init__(self):
        """Convert Celsius to Kelvin if provided"""
        if self.temperature_C is not None and self.temperature_K is None:
            self.temperature_K = self.temperature_C + 273.15

@dataclass
class ThermodynamicsResult:
    """Results from thermodynamics calculations"""
    calculated_value: float
    calculation_mode: ThermodynamicsMode
    input_parameters: dict
    units: str
    equation_used: str

# Physical constants
R_GAS_CONSTANT = 8.314  # J/(mol·K) - Universal gas constant

def calculate_thermodynamics(params: ThermodynamicsInput, mode: ThermodynamicsMode) -> ThermodynamicsResult:
    """
    Calculate thermodynamic parameters using fundamental relationships.
    
    Key equations:
    - Gibbs-Helmholtz: ΔG = ΔH - TΔS
    - Equilibrium: ΔG = -RT ln(K)
    
    Args:
        params: ThermodynamicsInput with known parameters
        mode: Which parameter to calculate
        
    Returns:
        ThermodynamicsResult with calculated value and metadata
        
    Raises:
        ValueError: If insufficient parameters provided or invalid values
    """
    
    # Validate inputs
    _validate_thermodynamics_input(params, mode)
    
    # Perform calculation based on mode
    if mode == ThermodynamicsMode.GIBBS_FREE_ENERGY:
        return _calculate_gibbs_free_energy(params)
    elif mode == ThermodynamicsMode.ENTHALPY:
        return _calculate_enthalpy(params)
    elif mode == ThermodynamicsMode.ENTROPY:
        return _calculate_entropy(params)
    elif mode == ThermodynamicsMode.TEMPERATURE:
        return _calculate_temperature(params)
    elif mode == ThermodynamicsMode.EQUILIBRIUM_CONSTANT:
        return _calculate_equilibrium_constant(params)
    elif mode == ThermodynamicsMode.GIBBS_FROM_KEQR:
        return _calculate_gibbs_from_keq(params)
    else:
        raise ValueError(f"Unsupported calculation mode: {mode}")

def _validate_thermodynamics_input(params: ThermodynamicsInput, mode: ThermodynamicsMode):
    """Validate that sufficient parameters are provided for the calculation"""
    
    if mode == ThermodynamicsMode.GIBBS_FREE_ENERGY:
        if params.delta_H_kJ_mol is None or params.delta_S_J_mol_K is None or params.temperature_K is None:
            raise ValueError("ΔG calculation requires ΔH, ΔS, and T")
    
    elif mode == ThermodynamicsMode.ENTHALPY:
        if params.delta_G_kJ_mol is None or params.delta_S_J_mol_K is None or params.temperature_K is None:
            raise ValueError("ΔH calculation requires ΔG, ΔS, and T")
    
    elif mode == ThermodynamicsMode.ENTROPY:
        if params.delta_G_kJ_mol is None or params.delta_H_kJ_mol is None or params.temperature_K is None:
            raise ValueError("ΔS calculation requires ΔG, ΔH, and T")
    
    elif mode == ThermodynamicsMode.TEMPERATURE:
        if params.delta_G_kJ_mol is None or params.delta_H_kJ_mol is None or params.delta_S_J_mol_K is None:
            raise ValueError("T calculation requires ΔG, ΔH, and ΔS")
    
    elif mode == ThermodynamicsMode.EQUILIBRIUM_CONSTANT:
        if params.delta_G_kJ_mol is None or params.temperature_K is None:
            raise ValueError("K calculation requires ΔG and T")
    
    elif mode == ThermodynamicsMode.GIBBS_FROM_KEQR:
        if params.equilibrium_constant is None or params.temperature_K is None:
            raise ValueError("ΔG from K calculation requires K and T")
    
    # Validate positive temperature
    if params.temperature_K is not None and params.temperature_K <= 0:
        raise ValueError("Temperature must be positive (> 0 K)")
    
    # Validate positive equilibrium constant
    if params.equilibrium_constant is not None and params.equilibrium_constant <= 0:
        raise ValueError("Equilibrium constant must be positive")

def _calculate_gibbs_free_energy(params: ThermodynamicsInput) -> ThermodynamicsResult:
    """Calculate ΔG = ΔH - TΔS"""
    delta_S_kJ_mol_K = params.delta_S_J_mol_K / 1000  # Convert J to kJ
    delta_G = params.delta_H_kJ_mol - params.temperature_K * delta_S_kJ_mol_K
    
    return ThermodynamicsResult(
        calculated_value=delta_G,
        calculation_mode=ThermodynamicsMode.GIBBS_FREE_ENERGY,
        input_parameters={
            'ΔH': f"{params.delta_H_kJ_mol} kJ/mol",
            'ΔS': f"{params.delta_S_J_mol_K} J/mol·K",
            'T': f"{params.temperature_K} K"
        },
        units="kJ/mol",
        equation_used="ΔG = ΔH - TΔS"
    )

def _calculate_enthalpy(params: ThermodynamicsInput) -> ThermodynamicsResult:
    """Calculate ΔH = ΔG + TΔS"""
    delta_S_kJ_mol_K = params.delta_S_J_mol_K / 1000  # Convert J to kJ
    delta_H = params.delta_G_kJ_mol + params.temperature_K * delta_S_kJ_mol_K
    
    return ThermodynamicsResult(
        calculated_value=delta_H,
        calculation_mode=ThermodynamicsMode.ENTHALPY,
        input_parameters={
            'ΔG': f"{params.delta_G_kJ_mol} kJ/mol",
            'ΔS': f"{params.delta_S_J_mol_K} J/mol·K",
            'T': f"{params.temperature_K} K"
        },
        units="kJ/mol",
        equation_used="ΔH = ΔG + TΔS"
    )

def _calculate_entropy(params: ThermodynamicsInput) -> ThermodynamicsResult:
    """Calculate ΔS = (ΔH - ΔG) / T"""
    delta_S_kJ_mol_K = (params.delta_H_kJ_mol - params.delta_G_kJ_mol) / params.temperature_K
    delta_S_J_mol_K = delta_S_kJ_mol_K * 1000  # Convert kJ to J
    
    return ThermodynamicsResult(
        calculated_value=delta_S_J_mol_K,
        calculation_mode=ThermodynamicsMode.ENTROPY,
        input_parameters={
            'ΔG': f"{params.delta_G_kJ_mol} kJ/mol",
            'ΔH': f"{params.delta_H_kJ_mol} kJ/mol",
            'T': f"{params.temperature_K} K"
        },
        units="J/mol·K",
        equation_used="ΔS = (ΔH - ΔG) / T"
    )

def _calculate_temperature(params: ThermodynamicsInput) -> ThermodynamicsResult:
    """Calculate T = (ΔH - ΔG) / ΔS"""
    if params.delta_S_J_mol_K == 0:
        raise ValueError("Cannot calculate temperature when ΔS = 0")
    
    delta_S_kJ_mol_K = params.delta_S_J_mol_K / 1000  # Convert J to kJ
    temperature = (params.delta_H_kJ_mol - params.delta_G_kJ_mol) / delta_S_kJ_mol_K
    
    if temperature <= 0:
        raise ValueError("Calculated temperature is not physically meaningful (≤ 0 K)")
    
    return ThermodynamicsResult(
        calculated_value=temperature,
        calculation_mode=ThermodynamicsMode.TEMPERATURE,
        input_parameters={
            'ΔG': f"{params.delta_G_kJ_mol} kJ/mol",
            'ΔH': f"{params.delta_H_kJ_mol} kJ/mol",
            'ΔS': f"{params.delta_S_J_mol_K} J/mol·K"
        },
        units="K",
        equation_used="T = (ΔH - ΔG) / ΔS"
    )

def _calculate_equilibrium_constant(params: ThermodynamicsInput) -> ThermodynamicsResult:
    """Calculate K = exp(-ΔG/RT)"""
    # Convert ΔG from kJ/mol to J/mol
    delta_G_J_mol = params.delta_G_kJ_mol * 1000
    
    # K = exp(-ΔG/RT)
    exponent = -delta_G_J_mol / (R_GAS_CONSTANT * params.temperature_K)
    K = math.exp(exponent)
    
    return ThermodynamicsResult(
        calculated_value=K,
        calculation_mode=ThermodynamicsMode.EQUILIBRIUM_CONSTANT,
        input_parameters={
            'ΔG': f"{params.delta_G_kJ_mol} kJ/mol",
            'T': f"{params.temperature_K} K"
        },
        units="dimensionless",
        equation_used="K = exp(-ΔG/RT)"
    )

def _calculate_gibbs_from_keq(params: ThermodynamicsInput) -> ThermodynamicsResult:
    """Calculate ΔG = -RT ln(K)"""
    # ΔG = -RT ln(K)
    delta_G_J_mol = -R_GAS_CONSTANT * params.temperature_K * math.log(params.equilibrium_constant)
    delta_G_kJ_mol = delta_G_J_mol / 1000  # Convert J to kJ
    
    return ThermodynamicsResult(
        calculated_value=delta_G_kJ_mol,
        calculation_mode=ThermodynamicsMode.GIBBS_FROM_KEQR,
        input_parameters={
            'K': f"{params.equilibrium_constant}",
            'T': f"{params.temperature_K} K"
        },
        units="kJ/mol",
        equation_used="ΔG = -RT ln(K)"
    )

def get_thermodynamics_info() -> dict:
    """Return information about thermodynamics calculations"""
    return {
        'title': 'Thermodynamics Calculator',
        'description': 'Calculate thermodynamic parameters using fundamental relationships',
        'equations': {
            'Gibbs-Helmholtz': 'ΔG = ΔH - TΔS',
            'Equilibrium': 'ΔG = -RT ln(K)',
            'Gas Constant': 'R = 8.314 J/(mol·K)'
        },
        'parameters': {
            'ΔG': {'name': 'Gibbs Free Energy', 'units': 'kJ/mol', 'typical_range': '(-100, 100)'},
            'ΔH': {'name': 'Enthalpy', 'units': 'kJ/mol', 'typical_range': '(-200, 200)'},
            'ΔS': {'name': 'Entropy', 'units': 'J/mol·K', 'typical_range': '(-500, 500)'},
            'T': {'name': 'Temperature', 'units': 'K', 'typical_range': '(200, 400)'},
            'K': {'name': 'Equilibrium Constant', 'units': 'dimensionless', 'typical_range': '(1e-10, 1e10)'}
        },
        'applications': [
            'Chemical reaction thermodynamics',
            'Protein folding energetics',
            'Enzyme kinetics and binding',
            'Phase transitions',
            'Electrochemical processes'
        ]
    }
