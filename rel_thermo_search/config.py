import numpy as np

# Physical Constants
ETA = np.diag([1, -1, -1, -1]) # Minkowski Metric
CRITICAL_FIELD = 500.0 # Schwinger limit units
ALPHA_EH = 1e-6 # Euler-Heisenberg coefficient
DISSIPATION_FACTOR = 0.005 # Base field dissipation

# Discovery Search Defaults
DEFAULT_SAMPLES = 1000
DEFAULT_GENERATIONS = 30
POP_SIZE = 40
MUTATION_RATE = 0.1

# Parameter Bounds
ENERGY_MIN, ENERGY_MAX = 0.1, 200.0
VORTICITY_MIN, VORTICITY_MAX = -100.0, 100.0
COUPLING_MIN, COUPLING_MAX = 0.01, 3.0

# Transport Coefficients
BTE_CARRIER_CONST = 1.0
BTE_RELAX_CONST = 0.05
CHI_QED_CONST = 1e-5

# Chemical Mapping
MIN_EN_DIFFERENCE = 0.5 # Heuristic for ionic character
ENERGY_DENSITY_SCALE = 100.0
VORTICITY_SCALE = 50.0
COUPLING_SCALE = 2.0
