import numpy as np
import matplotlib.pyplot as plt
from material_engine import RelMaterial

def sensitivity_analysis():
    # Base parameters
    e_dens = 50.0
    vort = np.array([0, 0, 20.0])
    coupling = 1.0

    # Ranges
    e_range = np.linspace(0.1, 200, 100)
    v_range = np.linspace(0, 100, 100)
    c_range = np.linspace(0.01, 5.0, 100)

    eff_e = [RelMaterial(e, vort, coupling).calculate_efficiency() for e in e_range]
    eff_v = [RelMaterial(e_dens, np.array([0,0,v]), coupling).calculate_efficiency() for v in v_range]
    eff_c = [RelMaterial(e_dens, vort, c).calculate_efficiency() for c in c_range]

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    axs[0].plot(e_range, eff_e)
    axs[0].set_title('Sensitivity to Energy Density')
    axs[0].set_xlabel('Energy Density')
    axs[0].set_ylabel('R-ZT')

    axs[1].plot(v_range, eff_v)
    axs[1].set_title('Sensitivity to Vorticity Magnitude')
    axs[1].set_xlabel('Vorticity')

    axs[2].plot(c_range, eff_c)
    axs[2].set_title('Sensitivity to Coupling Constant')
    axs[2].set_xlabel('Coupling')

    plt.tight_layout()
    import os
    output_path = os.path.join(os.path.dirname(__file__), 'sensitivity_analysis.png')
    plt.savefig(output_path)
    print(f"Sensitivity analysis saved to {output_path}")

if __name__ == "__main__":
    sensitivity_analysis()
