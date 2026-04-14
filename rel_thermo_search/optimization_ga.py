import numpy as np
import random
from material_engine import RelMaterial
from material_db import load_db, save_to_db
from chemical_translator import ChemicalTranslator
from config import POP_SIZE, MUTATION_RATE, DEFAULT_GENERATIONS, ENERGY_MIN, ENERGY_MAX, VORTICITY_MIN, VORTICITY_MAX, COUPLING_MIN, COUPLING_MAX

class GeneticOptimizer:
    def __init__(self, pop_size=POP_SIZE, mutation_rate=MUTATION_RATE, generations=DEFAULT_GENERATIONS):
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = self._initialize_population()

    def _initialize_population(self):
        population = []
        db = load_db()
        # Seed from DB if available
        if db:
            seeds = sorted(db, key=lambda x: x.get('efficiency', 0), reverse=True)[:self.pop_size // 2]
            for s in seeds:
                population.append({
                    'energy_density': s['energy_density'],
                    'vorticity': np.array(s['vorticity']),
                    'coupling': s['coupling']
                })

        # Fill the rest with random materials
        while len(population) < self.pop_size:
            population.append({
                'energy_density': np.random.uniform(ENERGY_MIN, ENERGY_MAX),
                'vorticity': np.random.uniform(VORTICITY_MIN, VORTICITY_MAX, size=3),
                'coupling': np.random.uniform(COUPLING_MIN, COUPLING_MAX)
            })
        return population

    def _fitness(self, individual):
        mat = RelMaterial(individual['energy_density'], individual['vorticity'], individual['coupling'])
        return mat.calculate_efficiency()

    def _mutate(self, individual, rate):
        if random.random() < rate:
            individual['energy_density'] *= np.random.uniform(0.8, 1.2)
        if random.random() < rate:
            individual['vorticity'] += np.random.uniform(-5.0, 5.0, size=3)
        if random.random() < rate:
            individual['coupling'] *= np.random.uniform(0.8, 1.2)
        return individual

    def _crossover(self, parent1, parent2):
        child = {}
        for key in ['energy_density', 'coupling']:
            child[key] = random.choice([parent1[key], parent2[key]])
        child['vorticity'] = random.choice([parent1['vorticity'], parent2['vorticity']]).copy()
        return child

    def evolve(self):
        for gen in range(self.generations):
            # Calculate fitness for all
            scored_pop = [(self._fitness(ind), ind) for ind in self.population]
            scored_pop.sort(key=lambda x: x[0], reverse=True)

            best_eff, best_ind = scored_pop[0]
            print(f"Generation {gen+1}: Best R-ZT = {best_eff:.4f}")

            # Selection with Elitism (Keep top 2)
            next_gen = [ind for score, ind in scored_pop[:2]]

            # Selection (Top 50%) for the rest of parents
            parents = [ind for score, ind in scored_pop[:self.pop_size // 2]]

            # Adaptive Mutation Rate
            current_mutation_rate = self.mutation_rate * (1.0 - gen / self.generations)

            # Crossover and Mutation to fill the rest
            while len(next_gen) < self.pop_size:
                p1 = random.choice(parents)
                p2 = random.choice(next_gen)
                child = self._crossover(p1, p2)
                child = self._mutate(child, current_mutation_rate)
                next_gen.append(child)

            self.population = next_gen

        # Return best
        final_scored = [(self._fitness(ind), ind) for ind in self.population]
        final_scored.sort(key=lambda x: x[0], reverse=True)
        best_score, best_ind = final_scored[0]

        translator = ChemicalTranslator()
        chem_info = translator.translate(
            best_ind['energy_density'],
            best_ind['vorticity'],
            best_ind['coupling']
        )

        result = {
            'energy_density': float(best_ind['energy_density']),
            'vorticity': best_ind['vorticity'].tolist(),
            'coupling': float(best_ind['coupling']),
            'efficiency': float(best_score),
            'method': 'genetic_algorithm'
        }
        result.update(chem_info)
        save_to_db(result)
        return result

if __name__ == "__main__":
    optimizer = GeneticOptimizer(pop_size=40, generations=30)
    optimizer.evolve()
