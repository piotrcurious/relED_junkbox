# Mapping Real-World Materials to Relativistic Field Parameters

# The 'Theory' (relED_junkbox) suggests:
# - Energy Density (T00) ~ Material Mass Density / Atomic Weight
# - Vorticity ~ Topological index / Lattice Complexity (Solitonic stability)
# - Coupling ~ Electronic Quality Factor / Seebeck potential coupling

KNOWN_MATERIALS = {
    "Bismuth Telluride (Bi2Te3)": {
        "real_zt": 1.0,
        "energy_density": 7.7, # g/cm3
        "vorticity": [0, 0, 10.0], # High due to topological insulator nature
        "coupling": 1.5
    },
    "Silicon Germanium (SiGe)": {
        "real_zt": 0.6,
        "energy_density": 3.0,
        "vorticity": [0, 0, 2.0], # Standard semiconductor
        "coupling": 0.8
    },
    "Lead Telluride (PbTe)": {
        "real_zt": 1.5,
        "energy_density": 8.16,
        "vorticity": [0, 0, 8.0],
        "coupling": 2.0
    },
    "Copper (Cu)": {
        "real_zt": 0.0001,
        "energy_density": 8.96,
        "vorticity": [0, 0, 0.1], # Metal, no stable solitons
        "coupling": 0.01 # Low Seebeck coupling in this framework
    },
    "Cobalt Antimonide (CoSb3)": {
        "real_zt": 0.8,
        "energy_density": 7.6,
        "vorticity": [0, 0, 5.0],
        "coupling": 1.1
    },
    "Zinc Antimonide (Zn4Sb3)": {
        "real_zt": 1.3,
        "energy_density": 6.3,
        "vorticity": [0, 0, 12.0],
        "coupling": 1.8
    }
}
