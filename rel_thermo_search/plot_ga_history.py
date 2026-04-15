import json
import os
import matplotlib.pyplot as plt

def plot_history():
    db_file = os.path.join(os.path.dirname(__file__), "discovered_materials.json")
    if not os.path.exists(db_file):
        return

    with open(db_file, 'r') as f:
        db = json.load(f)

    # Find the latest multi_objective_ga run with history
    ga_runs = [m for m in db if m.get('method') == 'multi_objective_ga' and 'history' in m]
    if not ga_runs:
        print("No GA history found to plot.")
        return

    # Use the best run (first one since db is sorted)
    latest = ga_runs[0]
    history = latest['history']

    gens = [h['gen'] for h in history]
    effs = [h['eff'] for h in history]
    stabs = [h['stab'] for h in history]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('Efficiency (R-ZT)', color=color)
    ax1.plot(gens, effs, color=color, linewidth=2, label='Efficiency')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Field Stability', color=color)
    ax2.plot(gens, stabs, color=color, linewidth=2, linestyle='--', label='Stability')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(0, 1.1)

    plt.title(f"GA Convergence: {latest.get('substance', 'Compound')}")
    fig.tight_layout()

    output_path = os.path.join(os.path.dirname(__file__), 'ga_convergence.png')
    plt.savefig(output_path)
    print(f"Convergence plot saved to {output_path}")

if __name__ == "__main__":
    plot_history()
