import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from material_engine import RelMaterial

def plot_vortex_structure(energy_density=50, vorticity=[0,0,10], coupling=1.0):
    # Create a 3D grid
    x = np.linspace(-5, 5, 10)
    y = np.linspace(-5, 5, 10)
    z = np.linspace(-5, 5, 10)
    X, Y, Z = np.meshgrid(x, y, z)

    # Internal fields from the theory
    # For a solitonic vortex, the field lines circulate
    # We'll use a simple toroidal/vortex model for visualization
    u = -Y * vorticity[2] / 10.0
    v = X * vorticity[2] / 10.0
    w = np.full_like(Z, vorticity[2] / 2.0)

    # E field is radial (proportional to energy density)
    ex = X * energy_density * coupling / 100.0
    ey = Y * energy_density * coupling / 100.0
    ez = Z * energy_density * coupling / 100.0

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Plot B-field (Vorticity) as streamlines-like arrows
    ax.quiver(X, Y, Z, u, v, w, length=0.8, color='blue', alpha=0.6, label='Vorticity (B)')

    # Plot E-field as radial arrows
    ax.quiver(X, Y, Z, ex, ey, ez, length=0.5, color='red', alpha=0.4, label='Energy Gradient (E)')

    ax.set_title(f'Relativistic Solitonic Vortex Structure\nE={energy_density}, V={vorticity}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    output_path = os.path.join(os.path.dirname(__file__), 'vortex_structure.png')
    plt.savefig(output_path)
    print(f"Vortex structure visualization saved to {output_path}")

if __name__ == "__main__":
    plot_vortex_structure()
