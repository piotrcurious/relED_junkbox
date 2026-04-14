import numpy as np
import random
from material_engine import RelMaterial
from material_db import load_db, save_to_db
from chemical_translator import ChemicalTranslator
from optimization_ga import GeneticOptimizer

class MultiObjectiveOptimizer(GeneticOptimizer):
    def _fitness(self, individual):
        mat = RelMaterial(individual['energy_density'], individual['vorticity'], individual['coupling'])
        efficiency = mat.calculate_efficiency()
        stability = mat.calculate_stability()

        # Multi-objective goal: Maximize Efficiency while maintaining high Stability
        # Weighted sum or product
        return efficiency * (stability ** 2)

    def evolve(self):
        print("Starting Multi-Objective Relativistic Evolution...")
        # Reuse evolution logic but with new fitness
        result = super().evolve()
        result['method'] = 'multi_objective_ga'
        save_to_db(result)
        return result

if __name__ == "__main__":
    optimizer = MultiObjectiveOptimizer(pop_size=40, generations=30)
    optimizer.evolve()
