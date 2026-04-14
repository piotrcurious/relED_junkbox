import numpy as np
from rel_tensor_util import ETA, faraday_tensor, stress_energy_em

class RelMaterial:
    def __init__(self, energy_density, vorticity, coupling_constant):
        self.energy_density = energy_density
        self.vorticity = vorticity # Vector representing the internal EM vortex strength
        self.coupling_constant = coupling_constant

    def simulate_fields(self):
        """
        Generates the internal E and B fields of the material 'vortex'.
        For a simple model, B is the vorticity, and E is induced by the
        energy density gradient (simplified).
        """
        B = np.array(self.vorticity)
        # In this theory, E field components are coupled to energy density
        # For a stable stationary vortex, we assume a radial E field proportional to density
        E = self.coupling_constant * np.array([self.energy_density, self.energy_density, self.energy_density])
        return E, B

    def calculate_efficiency(self):
        """
        Calculates the Relativistic Figure of Merit (R-ZT).
        In the junkbox theory, efficiency is high when the energy flux (T_0i)
        is strongly coupled to the potential gradient.
        """
        E, B = self.simulate_fields()
        F = faraday_tensor(E, B)
        T = stress_energy_em(F)

        # Energy flux components
        flux = np.sqrt(T[0,1]**2 + T[0,2]**2 + T[0,3]**2)

        # Stability check: Trace of T should be zero for pure EM field (conformally invariant)
        # For matter-field, there might be a non-zero trace (mass), but we want low dissipation.
        trace = np.trace(np.matmul(T, ETA))

        # Field Dissipation term (based on non-linearity/vorticity energy)
        # In a real QED framework, high field gradients lead to pair production or dissipation.
        dissipation = 0.01 * (self.energy_density**2 + np.sum(np.array(self.vorticity)**2))

        # Figure of Merit R-ZT = (Coupling * Flux) / (1 + abs(trace) + dissipation)
        # High flux + low dissipation = high efficiency.
        efficiency = (self.coupling_constant * flux) / (1.0 + abs(trace) + dissipation)
        return efficiency

if __name__ == "__main__":
    mat = RelMaterial(energy_density=10.0, vorticity=[0, 0, 5.0], coupling_constant=0.5)
    print(f"Material Efficiency: {mat.calculate_efficiency()}")
