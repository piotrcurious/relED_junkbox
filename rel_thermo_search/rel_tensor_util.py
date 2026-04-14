import numpy as np

# Metric tensor (Minkowski +---)
ETA = np.diag([1, -1, -1, -1])

def contract(A, B, indices):
    """
    General tensor contraction.
    'indices' should be a tuple of (axis_A, axis_B)
    """
    return np.tensordot(A, B, axes=indices)

def raise_index(tensor, index_pos):
    """
    Raises the index at index_pos using ETA.
    """
    # Assuming tensor is rank-N
    # result^...mu... = eta^mu_nu tensor^...nu...
    # Since ETA is diagonal and symmetric, it's easy.
    return np.tensordot(ETA, tensor, axes=(1, index_pos))

def lower_index(tensor, index_pos):
    """
    Lowers the index at index_pos using ETA.
    """
    return np.tensordot(ETA, tensor, axes=(1, index_pos))

def faraday_tensor(E, B):
    """
    Constructs the Faraday F^mu nu (or F_mu nu depending on convention)
    Here we construct F_mu_nu with indices (0,1,2,3)
    """
    F = np.zeros((4, 4))
    # Electric field components E_i = F_i0
    F[1, 0] = E[0]
    F[2, 0] = E[1]
    F[3, 0] = E[2]
    F[0, 1] = -E[0]
    F[0, 2] = -E[1]
    F[0, 3] = -E[2]

    # Magnetic field components B_i = -1/2 epsilon_ijk F^jk
    # F_12 = B3, F_23 = B1, F_31 = B2
    F[1, 2] = B[2]
    F[2, 1] = -B[2]
    F[2, 3] = B[0]
    F[3, 2] = -B[0]
    F[3, 1] = B[1]
    F[1, 3] = -B[1]

    return F

def stress_energy_em(F):
    """
    Calculates the Electromagnetic Stress-Energy Tensor T_mu_nu
    T_mu_nu = 1/mu0 * (F_mu_alpha F_nu^alpha - 1/4 eta_mu_nu F_alpha_beta F^alpha_beta)
    """
    # For simplicity, mu0 = 1
    # Raise one index of F: F_nu^alpha = F_nu_beta eta^beta_alpha
    F_up = np.matmul(F, ETA) # F_mu_alpha * eta^alpha_beta = F_mu^beta

    # First term: F_mu_alpha F_nu^alpha = F_mu_alpha F_beta_nu eta^alpha_beta
    # F_up has indices F_mu^alpha
    term1 = np.matmul(F, F_up.T)

    # The sign convention for T00 should be positive for energy density.
    # Let's check T_00 = F_0_alpha F_0^alpha - 1/4 eta_00 (F_ab F^ab)

    # Second term: 1/4 eta_mu_nu F_alpha_beta F^alpha_beta
    # F_inv = F_alpha_beta F^alpha_beta
    F_double_up = np.matmul(ETA, np.matmul(F, ETA))
    F_inv = np.sum(F * F_double_up)

    term2 = 0.25 * ETA * F_inv

    # Adjusted sign for standard convention
    return -(term1 - term2)

if __name__ == "__main__":
    # Test
    E = [1, 0, 0]
    B = [0, 1, 0]
    F = faraday_tensor(E, B)
    T = stress_energy_em(F)
    print("Stress-Energy Tensor T_00 (Energy Density):", T[0,0])
    print("Stress-Energy Tensor T_01 (Energy Flux x):", T[0,1])
