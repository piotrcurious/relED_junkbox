import os
import subprocess
import argparse
import sys

def run_pipeline(iterations=500, generations=20):
    print("=== STARTING RELATIVISTIC THERMOELECTRIC DISCOVERY PIPELINE ===")

    # 1. Clear previous cache (optional)
    # 2. Run Parallel Search
    print(f"\nStep 1: Parallel Random Search ({iterations} iterations)...")
    subprocess.run([sys.executable, "rel_thermo_search/parallel_search.py", "--total_iterations", str(iterations)], check=True)

    # 3. Run Multi-Objective GA
    print(f"\nStep 2: Multi-Objective Genetic Evolution ({generations} generations)...")
    subprocess.run([sys.executable, "rel_thermo_search/optimization_mo_ga.py"], check=True)

    # 4. Generate Visualizations
    print("\nStep 3: Generating Visualizations...")
    subprocess.run([sys.executable, "rel_thermo_search/visualize_discovery.py"], check=True)
    subprocess.run([sys.executable, "rel_thermo_search/sensitivity_analysis.py"], check=True)
    subprocess.run([sys.executable, "rel_thermo_search/plot_top_candidates.py"], check=True)
    subprocess.run([sys.executable, "rel_thermo_search/plot_phase_diagram.py"], check=True)
    subprocess.run([sys.executable, "rel_thermo_search/validate_real_materials.py"], check=True)

    # 5. Generate Report
    print("\nStep 4: Compiling Final Report...")
    subprocess.run([sys.executable, "rel_thermo_search/generate_report.py"], check=True)

    print("\n=== PIPELINE COMPLETE ===")
    print("Outputs available in rel_thermo_search/:")
    print(" - discovery_map.png")
    print(" - sensitivity_analysis.png")
    print(" - discovery_report.txt")
    print(" - discovered_materials.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=500)
    parser.add_argument("--generations", type=int, default=20)
    args = parser.parse_args()
    run_pipeline(args.iterations, args.generations)
