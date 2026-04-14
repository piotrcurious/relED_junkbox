import json
import os
import matplotlib.pyplot as plt
import numpy as np

def plot_top_candidates():
    db_file = os.path.join(os.path.dirname(__file__), "discovered_materials.json")
    if not os.path.exists(db_file):
        print("No database found to plot.")
        return

    with open(db_file, 'r') as f:
        db = json.load(f)

    if not db:
        print("Database is empty.")
        return

    # Sort and pick top 10
    db.sort(key=lambda x: x.get('efficiency', 0), reverse=True)
    top_db = db[:10]

    names = [m.get('substance', 'Theoretical') for m in top_db]
    effs = [m['efficiency'] for m in top_db]
    stabs = [m.get('chemical_stability', 0.5) for m in top_db]

    fig, ax1 = plt.subplots(figsize=(12, 7))

    color = 'tab:blue'
    ax1.set_xlabel('Material')
    ax1.set_ylabel('Efficiency (R-ZT)', color=color)
    bars = ax1.bar(names, effs, color=color, alpha=0.6)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.xticks(rotation=45, ha='right')

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Chemical Stability', color=color)
    ax2.plot(names, stabs, color=color, marker='o', linestyle='--')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(0, 1.1)

    plt.title('Top 10 Relativistic Thermoelectric Candidates')
    plt.tight_layout()

    output_path = os.path.join(os.path.dirname(__file__), 'top_candidates.png')
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    plot_top_candidates()
