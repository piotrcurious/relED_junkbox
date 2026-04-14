import numpy as np
import random
from material_engine import RelMaterial
from material_db import load_db, save_to_db

class GeneticOptimizer:
    def __init__(self, pop_size=50, mutation_rate=0.1, generations=20):
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
                'energy_density': np.random.uniform(0.1, 100.0),
                'vorticity': np.random.uniform(-50.0, 50.0, size=3),
                'coupling': np.random.uniform(0.01, 2.0)
            })
        return population

    def _fitness(self, individual):
        mat = RelMaterial(individual['energy_density'], individual['vorticity'], individual['coupling'])
        return mat.calculate_efficiency()

    def _mutate(self, individual):
        if random.random() < self.mutation_rate:
            individual['energy_density'] *= np.random.uniform(0.8, 1.2)
        if random.random() < self.mutation_rate:
            individual['vorticity'] += np.random.uniform(-5.0, 5.0, size=3)
        if random.random() < self.mutation_rate:
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

            # Selection (Top 50%)
            next_gen = [ind for score, ind in scored_pop[:self.pop_size // 2]]

            # Crossover and Mutation to fill the rest
            while len(next_gen) < self.pop_size:
                p1 = random.choice(next_gen)
                p2 = random.choice(next_gen)
                child = self._crossover(p1, p2)
                child = self._mutate(child)
                next_gen.append(child)

            self.population = next_gen

        # Return best
        final_scored = [(self._fitness(ind), ind) for ind in self.population]
        final_scored.sort(key=lambda x: x[0], reverse=True)
        best_score, best_ind = final_scored[0]

        result = {
            'energy_density': float(best_ind['energy_density']),
            'vorticity': best_ind['vorticity'].tolist(),
            'coupling': float(best_ind['coupling']),
            'efficiency': float(best_score),
            'method': 'genetic_algorithm'
        }
        save_to_db(result)
        return result

if __name__ == "__main__":
    optimizer = GeneticOptimizer(pop_size=40, generations=30)
    optimizer.evolve()
