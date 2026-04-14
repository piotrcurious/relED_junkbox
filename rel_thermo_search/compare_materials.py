import sys
import numpy as np
from material_engine import RelMaterial
from chemical_translator import ChemicalTranslator

def compare(formula1, formula2):
    translator = ChemicalTranslator()

    mats = []
    for f in [formula1, formula2]:
        p = translator.reverse_lookup(f)
        mat = RelMaterial(p['energy_density'], p['vorticity'], p['coupling'])
        mats.append((f, mat))

    print(f"{'Metric':<25} | {formula1:<30} | {formula2:<30}")
    print("-" * 90)

    eff1 = mats[0][1].calculate_efficiency()
    eff2 = mats[1][1].calculate_efficiency()
    print(f"{'Rel Figure of Merit':<25} | {eff1:<30.4f} | {eff2:<30.4f}")

    stab1 = mats[0][1].calculate_stability()
    stab2 = mats[1][1].calculate_stability()
    print(f"{'Field Stability':<25} | {stab1:<30.4f} | {stab2:<30.4f}")

    E1, _ = mats[0][1].simulate_fields()
    E2, _ = mats[1][1].simulate_fields()
    print(f"{'Electric Field':<25} | {np.linalg.norm(E1):<30.2f} | {np.linalg.norm(E2):<30.2f}")

    print("-" * 90)
    winner = formula1 if eff1 > eff2 else formula2
    print(f"CONCLUSION: {winner} is theoretically superior in this relativistic framework.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        compare(sys.argv[1], sys.argv[2])
    else:
        compare("Bi2Te3", "PbTe")
