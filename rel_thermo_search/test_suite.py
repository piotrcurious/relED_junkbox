import unittest
import numpy as np
from rel_tensor_util import faraday_tensor, stress_energy_em, ETA
from material_engine import RelMaterial

class TestRelThermo(unittest.TestCase):
    def test_tensor_trace(self):
        # Pure EM field T should be traceless (eta_mu_nu T^mu_nu = 0)
        E = [1, 0, 0]
        B = [0, 1, 0]
        F = faraday_tensor(E, B)
        T = stress_energy_em(F)
        # Raising index to get T^mu_nu
        T_up = np.matmul(ETA, np.matmul(T, ETA))
        trace = np.sum(ETA * T_up) # This is equivalent to eta_mu_nu T^mu_nu
        # Note: My stress_energy_em returns T_mu_nu.
        # Trace is g^mu_nu T_mu_nu
        trace_direct = np.trace(np.matmul(T, ETA))
        self.assertAlmostEqual(trace_direct, 0.0, places=7)

    def test_energy_density_positive(self):
        E = np.random.rand(3)
        B = np.random.rand(3)
        F = faraday_tensor(E, B)
        T = stress_energy_em(F)
        self.assertGreaterEqual(T[0,0], 0.0)

    def test_material_efficiency(self):
        mat = RelMaterial(10, [0,0,1], 1.0)
        eff = mat.calculate_efficiency()
        self.assertIsInstance(eff, float)
        self.assertGreater(eff, 0)

if __name__ == "__main__":
    unittest.main()
