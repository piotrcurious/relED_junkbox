import numpy as np
import os
import re
from material_mapping import KNOWN_MATERIALS

# Heuristic Element Properties for Synthesis
ELEMENTS = {
    "Bi": {"mass": 208.9, "en": 2.02, "type": "p-block", "valency": 3},
    "Te": {"mass": 127.6, "en": 2.1, "type": "chalcogen", "valency": 2},
    "Sb": {"mass": 121.7, "en": 2.05, "type": "p-block", "valency": 3},
    "Pb": {"mass": 207.2, "en": 2.33, "type": "p-block", "valency": 2},
    "Si": {"mass": 28.1, "en": 1.9, "type": "metalloid", "valency": 4},
    "Ge": {"mass": 72.6, "en": 2.01, "type": "metalloid", "valency": 4},
    "Co": {"mass": 58.9, "en": 1.88, "type": "transition", "valency": 3},
    "Zn": {"mass": 65.4, "en": 1.65, "type": "transition", "valency": 2},
    "Cu": {"mass": 63.5, "en": 1.9, "type": "transition", "valency": 1},
    "Se": {"mass": 78.9, "en": 2.55, "type": "chalcogen", "valency": 2},
    "Ag": {"mass": 107.8, "en": 1.93, "type": "transition", "valency": 1},
    "Sn": {"mass": 118.7, "en": 1.96, "type": "p-block", "valency": 2},
    "Au": {"mass": 197.0, "en": 2.54, "type": "transition", "valency": 1},
    "Hg": {"mass": 200.6, "en": 2.0, "type": "transition", "valency": 2},
    "Tl": {"mass": 204.4, "en": 2.04, "type": "p-block", "valency": 1},
    "In": {"mass": 114.8, "en": 1.78, "type": "p-block", "valency": 3},
    "Ga": {"mass": 69.7, "en": 1.81, "type": "p-block", "valency": 3},
    "As": {"mass": 74.9, "en": 2.18, "type": "metalloid", "valency": 3},
    "S": {"mass": 32.1, "en": 2.58, "type": "chalcogen", "valency": 2},
}

class ChemicalTranslator:
    def __init__(self):
        self.anchors = KNOWN_MATERIALS

    def _calculate_distance(self, p1, p2):
        """
        Normalized Euclidean distance in Relativistic Parameter Space.
        p = [energy_density, vorticity_magnitude, coupling]
        """
        norms = np.array([100.0, 50.0, 2.0])
        return np.linalg.norm((np.array(p1) - np.array(p2)) / norms)

    def calculate_chemical_stability(self, el_names):
        """
        Calculates a heuristic stability score based on element compatibility.
        """
        if not el_names:
            return 0.0

        types = [ELEMENTS.get(el, {}).get('type', 'unknown') for el in el_names]
        if 'p-block' in types and ('chalcogen' in types or 'transition' in types):
            return 0.9
        if 'metalloid' in types:
            return 0.8
        return 0.5

    def translate(self, energy_density, vorticity, coupling):
        v_mag = np.linalg.norm(vorticity)
        current_p = [energy_density, v_mag, coupling]

        distances = []
        for name, props in self.anchors.items():
            anchor_p = [props['energy_density'], np.linalg.norm(props['vorticity']), props['coupling']]
            dist = self._calculate_distance(current_p, anchor_p)
            distances.append((dist, name))

        distances.sort()
        best_match_dist, best_match_name = distances[0]

        if coupling < 0.1:
            bond_type = "Metallic (Delocalized Soliton)"
        elif coupling > 1.5:
            bond_type = "Complex Covalent-Ionic (Topological Vortex)"
        else:
            bond_type = "Semiconducting Covalent (Stable Soliton)"

        if best_match_dist < 0.1:
            predicted_substance = best_match_name
            found_els = re.findall(r'([A-Z][a-z]*)', best_match_name)
            el1 = found_els[0] if len(found_els) > 0 else "Bi"
            el2 = found_els[1] if len(found_els) > 1 else "Te"
        else:
            candidates = []
            if energy_density > 80:
                candidates = ["Pb", "Bi", "Tl", "Hg", "Au"]
            elif energy_density > 40:
                candidates = ["Sb", "Te", "Se", "Ag", "Sn", "In"]
            else:
                candidates = ["Si", "Ge", "Co", "Zn", "Ga", "As", "S"]

            el1 = candidates[0]
            el2 = candidates[min(1, len(candidates)-1)]
            v1 = ELEMENTS.get(el1, {}).get('valency', 1)
            v2 = ELEMENTS.get(el2, {}).get('valency', 1)

            if v_mag > 40 and len(candidates) > 2:
                el3 = candidates[2]
                v3 = ELEMENTS.get(el3, {}).get('valency', 1)
                formula = f"{el1}{el2}{el3}{abs(v1+v2-v3)+1} (Relativistic Ternary)"
            elif v_mag > 20:
                formula = f"{el1}{v2}{el2}{v1} (Topological Phase)"
            else:
                formula = f"{el1}{el2} Solid Solution"

            predicted_substance = f"Theoretical {formula} [Ref: {best_match_name}]"

        chem_stability = self.calculate_chemical_stability([el1, el2])

        return {
            "substance": predicted_substance,
            "bond_type": bond_type,
            "nearest_anchor": best_match_name,
            "confidence": float(max(0, 1.0 - best_match_dist)),
            "chemical_stability": chem_stability
        }

    def reverse_lookup(self, formula):
        """
        Heuristically map a chemical formula to relativistic parameters.
        """
        for name, props in self.anchors.items():
            if formula.lower() in name.lower():
                return props

        parts = re.findall(r'([A-Z][a-z]*)(\d*)', formula)

        total_mass = 0
        element_count = 0
        for el, count in parts:
            c = int(count) if count else 1
            if el in ELEMENTS:
                total_mass += ELEMENTS[el]['mass'] * c
                element_count += c

        if total_mass > 0:
            energy_density = min(100.0, total_mass / (5.0 * element_count + 1))
            v_mag = 10.0 * len(parts)
            return {
                "energy_density": energy_density,
                "vorticity": [0, 0, v_mag],
                "coupling": 1.0 + 0.1 * len(parts)
            }

        return {
            "energy_density": 50.0,
            "vorticity": [0, 0, 10.0],
            "coupling": 1.0
        }

if __name__ == "__main__":
    translator = ChemicalTranslator()
    print(f"Reverse Lookup (Bi2Te3): {translator.reverse_lookup('Bi2Te3')}")
    result = translator.translate(7.5, [0, 0, 9.5], 1.4)
    print(f"Result: {result}")
    result2 = translator.translate(55.0, [20, 20, 20], 1.8)
    print(f"Discovery: {result2}")
