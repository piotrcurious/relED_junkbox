import sys
import numpy as np
from material_engine import RelMaterial
from chemical_translator import ChemicalTranslator

def compare(formula1, formula2):
    translator = ChemicalTranslator()

    data = []
    for f in [formula1, formula2]:
        p = translator.reverse_lookup(f)
        mat = RelMaterial(p['energy_density'], p['vorticity'], p['coupling'])
        chem = translator.translate(p['energy_density'], p['vorticity'], p['coupling'])
        data.append({'formula': f, 'mat': mat, 'chem': chem})

    print(f"{'Metric':<25} | {formula1:<30} | {formula2:<30}")
    print("-" * 90)

    eff1 = data[0]['mat'].calculate_efficiency()
    eff2 = data[1]['mat'].calculate_efficiency()
    print(f"{'Rel Figure of Merit':<25} | {eff1:<30.4f} | {eff2:<30.4f}")

    stab1 = data[0]['mat'].calculate_stability()
    stab2 = data[1]['mat'].calculate_stability()
    print(f"{'Field Stability':<25} | {stab1:<30.4f} | {stab2:<30.4f}")

    print(f"{'Category':<25} | {data[0]['chem'].get('category', 'N/A'):<30} | {data[1]['chem'].get('category', 'N/A'):<30}")
    print(f"{'Synthesis Path':<25} | {data[0]['chem'].get('synthesis_path', 'N/A')[:28]:<30} | {data[1]['chem'].get('synthesis_path', 'N/A')[:28]:<30}")

    print("-" * 90)
    winner = formula1 if eff1 > eff2 else formula2
    print(f"CONCLUSION: {winner} is theoretically superior in this relativistic framework.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        compare(sys.argv[1], sys.argv[2])
    else:
        compare("Bi2Te3", "PbTe")
