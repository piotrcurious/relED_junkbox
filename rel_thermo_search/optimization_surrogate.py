import numpy as np
import os
from material_engine import RelMaterial
from material_db import load_db, save_to_db
from config import ENERGY_MIN, ENERGY_MAX, VORTICITY_MIN, VORTICITY_MAX, COUPLING_MIN, COUPLING_MAX

class SurrogateSearch:
    def __init__(self):
        self.points = []
        self.scores = []
        # Seed from DB
        db = load_db()
        for m in db:
            p = [m['energy_density'], np.linalg.norm(m['vorticity']), m['coupling']]
            self.points.append(p)
            self.scores.append(m['efficiency'])

    def _heuristic_surrogate(self, p):
        """
        A simple RBF-like surrogate: efficiency is high near known high-performers.
        """
        if not self.points: return np.random.rand()

        pts = np.array(self.points)
        scs = np.array(self.scores)

        # Euclidean distances
        dists = np.linalg.norm(pts - np.array(p), axis=1)
        # Inverse distance weighting
        weights = 1.0 / (dists + 0.1)
        score = np.sum(weights * scs) / np.sum(weights)
        return score

    def search(self, num_samples=1000):
        print(f"Starting Surrogate-Guided Discovery ({num_samples} iterations)...")
        best_p = None
        best_score = -1

        # Randomly sample, but rank by surrogate
        candidates = []
        for _ in range(num_samples * 2):
            p = [
                np.random.uniform(ENERGY_MIN, ENERGY_MAX),
                np.random.uniform(0, VORTICITY_MAX), # mag
                np.random.uniform(COUPLING_MIN, COUPLING_MAX)
            ]
            candidates.append((p, self._heuristic_surrogate(p)))

        # Select top candidates to evaluate for real
        candidates.sort(key=lambda x: x[1], reverse=True)

        for p_cand, s_surr in candidates[:num_samples]:
            # Convert back to vector vorticity (simplified: random direction)
            vec_v = np.random.uniform(-1, 1, 3)
            vec_v = vec_v / np.linalg.norm(vec_v) * p_cand[1]

            mat = RelMaterial(p_cand[0], vec_v, p_cand[2])
            eff = mat.calculate_efficiency()

            if eff > best_score:
                best_score = eff
                best_p = {'energy_density': p_cand[0], 'vorticity': vec_v.tolist(), 'coupling': p_cand[2], 'efficiency': eff}

        if best_p:
            best_p['method'] = 'surrogate_search'
            save_to_db(best_p)
            print(f"Surrogate Discovery: Best R-ZT = {best_score:.4f}")
        return best_p

if __name__ == "__main__":
    searcher = SurrogateSearch()
    searcher.search(100)
