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

        # Euler-Heisenberg Correction (Vacuum Polarization)
        # L_eff = L_Maxwell + alpha^2/m^4 * (4(F_munu F^munu)^2 + 7(F_munu *F^munu)^2)
        # We simplify this as a non-linear term in the stress-energy tensor.
        F_up = np.matmul(F, ETA)
        F_inv = np.sum(F * np.matmul(ETA, F_up))
        # Simplified non-linear contribution
        alpha_corr = 1e-6 * (F_inv**2)

        T = stress_energy_em(F)

        # Energy flux components
        flux = np.sqrt(T[0,1]**2 + T[0,2]**2 + T[0,3]**2)

        # Stability check: Trace of T should be zero for pure EM field (conformally invariant)
        trace = np.trace(np.matmul(T, ETA))

        # Topological stability bonus:
        # Certain vorticities are more stable (quantum numbers)
        v_norm = np.linalg.norm(self.vorticity)
        stability_bonus = 1.0 + 0.5 * np.sin(v_norm * np.pi / 10.0) # Oscillation of stability

        # Field Dissipation term (QED-scale)
        dissipation = 0.005 * (self.energy_density**2 + v_norm**2) + alpha_corr

        # Figure of Merit R-ZT = (Coupling * Flux * Stability) / (1 + abs(trace) + dissipation)
        efficiency = (self.coupling_constant * flux * stability_bonus) / (1.0 + abs(trace) + dissipation)
        return efficiency

if __name__ == "__main__":
    mat = RelMaterial(energy_density=10.0, vorticity=[0, 0, 5.0], coupling_constant=0.5)
    print(f"Material Efficiency: {mat.calculate_efficiency()}")
