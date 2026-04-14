import numpy as np
import os
from material_mapping import KNOWN_MATERIALS

# Heuristic Element Properties for Synthesis
ELEMENTS = {
    "Bi": {"mass": 208.9, "en": 2.02, "type": "p-block"},
    "Te": {"mass": 127.6, "en": 2.1, "type": "chalcogen"},
    "Sb": {"mass": 121.7, "en": 2.05, "type": "p-block"},
    "Pb": {"mass": 207.2, "en": 2.33, "type": "p-block"},
    "Si": {"mass": 28.1, "en": 1.9, "type": "metalloid"},
    "Ge": {"mass": 72.6, "en": 2.01, "type": "metalloid"},
    "Co": {"mass": 58.9, "en": 1.88, "type": "transition"},
    "Zn": {"mass": 65.4, "en": 1.65, "type": "transition"},
    "Cu": {"mass": 63.5, "en": 1.9, "type": "transition"},
    "Se": {"mass": 78.9, "en": 2.55, "type": "chalcogen"},
    "Ag": {"mass": 107.8, "en": 1.93, "type": "transition"},
    "Sn": {"mass": 118.7, "en": 1.96, "type": "p-block"},
}

class ChemicalTranslator:
    def __init__(self):
        self.anchors = KNOWN_MATERIALS

    def _calculate_distance(self, p1, p2):
        """
        Normalized Euclidean distance in Relativistic Parameter Space.
        p = [energy_density, vorticity_magnitude, coupling]
        """
        # Normalization factors based on typical ranges
        norms = np.array([100.0, 50.0, 2.0])
        return np.linalg.norm((np.array(p1) - np.array(p2)) / norms)

    def translate(self, energy_density, vorticity, coupling):
        v_mag = np.linalg.norm(vorticity)
        current_p = [energy_density, v_mag, coupling]

        # Find nearest known materials
        distances = []
        for name, props in self.anchors.items():
            anchor_p = [props['energy_density'], np.linalg.norm(props['vorticity']), props['coupling']]
            dist = self._calculate_distance(current_p, anchor_p)
            distances.append((dist, name))

        distances.sort()

        # Heuristic Analysis
        best_match_dist, best_match_name = distances[0]

        # Determine Bond Type
        if coupling < 0.1:
            bond_type = "Metallic (Delocalized Soliton)"
        elif coupling > 1.5:
            bond_type = "Complex Covalent-Ionic (Topological Vortex)"
        else:
            bond_type = "Semiconducting Covalent (Stable Soliton)"

        # Synthesize a "Predicted Compound" based on Energy Density (Mass)
        # and Vorticity (Complexity)

        if best_match_dist < 0.1:
            # Very close to a known material
            predicted_substance = best_match_name
        else:
            # Interpolated / Theoretical Material
            # High energy density -> Heavy elements
            # High vorticity -> Complex stoichiometry

            candidates = []
            if energy_density > 80:
                candidates = ["Pb", "Bi", "Sn"]
            elif energy_density > 40:
                candidates = ["Sb", "Te", "Se", "Ag"]
            else:
                candidates = ["Si", "Ge", "Co", "Zn"]

            # Pick two elements based on vorticity
            if v_mag > 30:
                formula = f"{candidates[0]}x{candidates[1]}y (High-Vorticity Alloy)"
            else:
                formula = f"{candidates[0]}-{candidates[1]} Solid Solution"

            predicted_substance = f"Theoretical {formula} [Ref: {best_match_name}]"

        return {
            "substance": predicted_substance,
            "bond_type": bond_type,
            "nearest_anchor": best_match_name,
            "confidence": float(max(0, 1.0 - best_match_dist))
        }

    def reverse_lookup(self, formula):
        """
        Heuristically map a chemical formula to relativistic parameters.
        """
        # Search in known materials first
        for name, props in self.anchors.items():
            if formula.lower() in name.lower():
                return props

        # Generic heuristic for unknown formulas
        # Simplified: uses sum of atomic weights (Energy Density)
        # and complexity (Vorticity)
        return {
            "energy_density": 50.0, # Placeholder for mass density
            "vorticity": [0, 0, 10.0],
            "coupling": 1.0
        }

if __name__ == "__main__":
    translator = ChemicalTranslator()
    # Test reverse lookup
    print(f"Reverse Lookup (Bi2Te3): {translator.reverse_lookup('Bi2Te3')}")
    # Test with Bi2Te3-like parameters
    result = translator.translate(7.5, [0, 0, 9.5], 1.4)
    print(f"Result: {result}")

    # Test with random discovery parameters
    result2 = translator.translate(55.0, [20, 20, 20], 1.8)
    print(f"Discovery: {result2}")
