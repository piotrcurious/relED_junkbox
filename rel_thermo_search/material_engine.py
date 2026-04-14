import numpy as np
from rel_tensor_util import ETA, faraday_tensor, stress_energy_em

class RelMaterial:
    def __init__(self, energy_density, vorticity, coupling_constant, meb_coupling=1.0):
        self.energy_density = energy_density
        self.vorticity = vorticity # Vector representing the internal EM vortex strength
        self.coupling_constant = coupling_constant
        self.meb_coupling = meb_coupling # Mass-Energy-Bond coupling

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

    def calculate_stability(self):
        """
        Calculates a stability score (0 to 1).
        1 is perfectly stable, 0 is unstable (Schwinger decay).
        """
        E, _ = self.simulate_fields()
        e_mag = np.linalg.norm(E)
        CRITICAL_FIELD = 500.0

        if e_mag <= CRITICAL_FIELD:
            return 1.0
        else:
            # Decay score
            return np.exp(-(e_mag - CRITICAL_FIELD) / 200.0)

    def calculate_efficiency(self):
        """
        Calculates the Relativistic Figure of Merit (R-ZT).
        In the junkbox theory, efficiency is high when the energy flux (T_0i)
        is strongly coupled to the potential gradient.
        """
        E, B = self.simulate_fields()
        F = faraday_tensor(E, B)

        # Euler-Heisenberg Correction (Vacuum Polarization)
        F_up = np.matmul(F, ETA)
        # Invariants: I1 = 1/2 F_munu F^munu, I2 = 1/4 F_munu *F^munu
        # We use a simplified invariant for correction
        F_inv = np.sum(F * np.matmul(ETA, F_up))
        alpha_corr = 1e-6 * (F_inv**2)

        T = stress_energy_em(F)

        # Rigorous Seebeck Gradient Dynamic:
        # F^i0 = S_rel * grad(T00). We assume grad(T00) ~ EnergyDensity / Scale
        # This is already captured in simulate_fields where E ~ energy_density * coupling

        # Energy flux components (Poynting-like vector)
        flux = np.sqrt(T[0,1]**2 + T[0,2]**2 + T[0,3]**2)

        # Stability check: Trace of T
        trace = np.trace(np.matmul(T, ETA))

        # QED Pair Production (Schwinger Effect) Limit
        # When E field exceeds a critical value, vacuum decays.
        e_mag = np.linalg.norm(E)
        CRITICAL_FIELD = 500.0
        schwinger_dissipation = 0.0
        if e_mag > CRITICAL_FIELD:
            # Exponentially increasing dissipation
            schwinger_dissipation = np.exp((e_mag - CRITICAL_FIELD) / 100.0)

        # Topological stability bonus:
        v_norm = np.linalg.norm(self.vorticity)
        stability_bonus = 1.0 + 0.5 * np.sin(v_norm * np.pi / 10.0)

        # Field Dissipation term
        dissipation = 0.005 * (self.energy_density**2 + v_norm**2) + alpha_corr + schwinger_dissipation

        # Figure of Merit R-ZT
        efficiency = (self.coupling_constant * flux * stability_bonus * self.meb_coupling) / (1.0 + abs(trace) + dissipation)
        return efficiency

if __name__ == "__main__":
    mat = RelMaterial(energy_density=10.0, vorticity=[0, 0, 5.0], coupling_constant=0.5)
    print(f"Material Efficiency: {mat.calculate_efficiency()}")
