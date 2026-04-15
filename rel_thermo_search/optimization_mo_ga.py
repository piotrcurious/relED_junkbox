import numpy as np
import random
from material_engine import RelMaterial
from material_db import load_db, save_to_db
from chemical_translator import ChemicalTranslator
from optimization_ga import GeneticOptimizer
from config import ENERGY_MIN, ENERGY_MAX, VORTICITY_MIN, VORTICITY_MAX, COUPLING_MIN, COUPLING_MAX

class MultiObjectiveOptimizer(GeneticOptimizer):
    def _fitness_objectives(self, individual):
        mat = RelMaterial(individual['energy_density'], individual['vorticity'], individual['coupling'])
        return mat.calculate_efficiency(), mat.calculate_stability()

    def _is_dominated(self, obj1, obj2):
        """ Checks if obj1 is dominated by obj2 """
        # obj = (efficiency, stability)
        # obj2 dominates obj1 if all objectives of obj2 >= obj1 AND at least one is >
        better_or_equal = (obj2[0] >= obj1[0] and obj2[1] >= obj1[1])
        strictly_better = (obj2[0] > obj1[0] or obj2[1] > obj1[1])
        return better_or_equal and strictly_better

    def _calculate_crowding_distance(self, ranked_pop_slice):
        """
        Calculates crowding distance to preserve diversity in the Pareto front.
        """
        if not ranked_pop_slice: return []
        n = len(ranked_pop_slice)
        distances = [0.0] * n

        # objectives are at index 1: (eff, stab)
        for obj_idx in [0, 1]:
            # Sort by objective
            indexed_objs = sorted(range(n), key=lambda i: ranked_pop_slice[i][1][obj_idx])

            # Boundary points have infinite distance
            distances[indexed_objs[0]] = float('inf')
            distances[indexed_objs[-1]] = float('inf')

            # Range for normalization
            obj_min = ranked_pop_slice[indexed_objs[0]][1][obj_idx]
            obj_max = ranked_pop_slice[indexed_objs[-1]][1][obj_idx]
            obj_range = obj_max - obj_min if obj_max > obj_min else 1.0

            for i in range(1, n - 1):
                distances[indexed_objs[i]] += (ranked_pop_slice[indexed_objs[i+1]][1][obj_idx] -
                                               ranked_pop_slice[indexed_objs[i-1]][1][obj_idx]) / obj_range
        return distances

    def evolve(self):
        print("Starting Pareto-Optimized Relativistic Evolution (NSGA-II inspired)...")
        history = []
        for gen in range(self.generations):
            # 1. Calculate objectives for all
            population_with_objs = []
            for ind in self.population:
                population_with_objs.append((self._fitness_objectives(ind), ind))

            # 2. Pareto Ranking (Simple approach: non-dominated count)
            ranked_pop = []
            for i, (objs_i, ind_i) in enumerate(population_with_objs):
                domination_count = 0
                for j, (objs_j, ind_j) in enumerate(population_with_objs):
                    if i == j: continue
                    if self._is_dominated(objs_i, objs_j):
                        domination_count += 1
                ranked_pop.append((domination_count, objs_i, ind_i))

            # Sort by domination count (0 is best - non-dominated)
            # Within same rank, sort by crowding distance (need to calculate)
            unique_ranks = sorted(list(set(r[0] for r in ranked_pop)))
            final_sorted_pop = []
            for r in unique_ranks:
                rank_slice = [item for item in ranked_pop if item[0] == r]
                crowd_dists = self._calculate_crowding_distance(rank_slice)
                # Attach distance and sort descending
                slice_with_dist = []
                for i in range(len(rank_slice)):
                    slice_with_dist.append((rank_slice[i], crowd_dists[i]))
                slice_with_dist.sort(key=lambda x: x[1], reverse=True)
                final_sorted_pop.extend([item[0] for item in slice_with_dist])

            best_rank, best_objs, best_ind = final_sorted_pop[0]
            print(f"Generation {gen+1}: Best Rank={best_rank}, Eff={best_objs[0]:.2f}, Stab={best_objs[1]:.2f}")
            history.append({'gen': gen+1, 'eff': best_objs[0], 'stab': best_objs[1]})

            # 3. Selection (Top 50% by Rank + Crowding)
            next_gen = [ind for rank, objs, ind in final_sorted_pop[:self.pop_size // 2]]

            # 4. Fill the rest with crossover/mutation and "Immigrants"
            current_mutation_rate = self.mutation_rate * (1.0 - gen / self.generations)

            # Add 10% fresh blood to prevent stagnation
            num_immigrants = max(1, self.pop_size // 10)
            for _ in range(num_immigrants):
                if len(next_gen) < self.pop_size:
                    next_gen.append({
                        'energy_density': np.random.uniform(ENERGY_MIN, ENERGY_MAX),
                        'vorticity': np.random.uniform(VORTICITY_MIN, VORTICITY_MAX, size=3),
                        'coupling': np.random.uniform(COUPLING_MIN, COUPLING_MAX)
                    })

            while len(next_gen) < self.pop_size:
                p1 = random.choice(next_gen[:max(2, self.pop_size // 4)]) # Prefer parents with better rank
                p2 = random.choice(next_gen)
                child = self._crossover(p1, p2)
                child = self._mutate(child, current_mutation_rate)
                next_gen.append(child)

            self.population = next_gen

        # Return best non-dominated
        final_objs = [(self._fitness_objectives(ind), ind) for ind in self.population]
        # Sort by weighted sum just for final selection
        final_objs.sort(key=lambda x: x[0][0] * x[0][1], reverse=True)
        best_objs, best_ind = final_objs[0]

        translator = ChemicalTranslator()
        chem_info = translator.translate(best_ind['energy_density'], best_ind['vorticity'], best_ind['coupling'])

        result = {
            'energy_density': float(best_ind['energy_density']),
            'vorticity': best_ind['vorticity'].tolist(),
            'coupling': float(best_ind['coupling']),
            'efficiency': float(best_objs[0]),
            'stability': float(best_objs[1]),
            'method': 'multi_objective_ga'
        }
        result.update(chem_info)
        result['history'] = history
        save_to_db(result)
        return result

if __name__ == "__main__":
    optimizer = MultiObjectiveOptimizer(pop_size=40, generations=30)
    optimizer.evolve()
