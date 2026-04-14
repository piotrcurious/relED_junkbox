import numpy as np
import multiprocessing as mp
import os
import time
from material_engine import RelMaterial
from material_db import save_to_db
from chemical_translator import ChemicalTranslator
from config import DEFAULT_SAMPLES

def evaluate_material_batch(args):
    """
    Evaluates a batch of random material configurations.
    Returns the best parameters and efficiency found in this batch.
    """
    batch_size, worker_id = args

    # Ensure fresh randomness in each worker process
    np.random.seed((os.getpid() * int(time.time())) % 123456789)

    # NUMA Consideration: Affinity/Pinning Hint
    # In a real NUMA environment, we might use psutil to pin to specific cores.
    # For now, we log the worker initialization.

    local_best_eff = -1
    local_best_params = None

    for _ in range(batch_size):
        energy_density = np.random.uniform(0.1, 100.0)
        vorticity = np.random.uniform(-50.0, 50.0, size=3)
        coupling = np.random.uniform(0.01, 2.0)

        mat = RelMaterial(energy_density, vorticity, coupling)
        eff = mat.calculate_efficiency()

        if eff > local_best_eff:
            local_best_eff = eff
            local_best_params = {
                'energy_density': energy_density,
                'vorticity': vorticity.tolist(), # Ensure serializability
                'coupling': coupling,
                'efficiency': eff
            }

    return local_best_params

def parallel_search(total_iterations=DEFAULT_SAMPLES, num_workers=None):
    if num_workers is None:
        # Respect NUMA/HPC environments via env var or cpu_count
        num_workers = int(os.environ.get('OMP_NUM_THREADS', os.cpu_count()))

    batch_size = total_iterations // num_workers
    remaining = total_iterations % num_workers
    batches = [batch_size] * num_workers
    if remaining > 0:
        batches[0] += remaining

    print(f"Starting Parallel Relativistic Search on {num_workers} workers...")
    print(f"Total Iterations: {total_iterations} (Batch Size: {batch_size})")

    start_time = time.time()

    # Prepare arguments for starmap/map
    worker_args = [(b, i) for i, b in enumerate(batches)]

    with mp.Pool(processes=num_workers) as pool:
        results = pool.map(evaluate_material_batch, worker_args)

    # Aggregate results from all workers
    global_best = max(results, key=lambda x: x['efficiency'])

    # Enrich with chemical info
    translator = ChemicalTranslator()
    chem_info = translator.translate(
        global_best['energy_density'],
        global_best['vorticity'],
        global_best['coupling']
    )
    global_best.update(chem_info)

    duration = time.time() - start_time

    print("\n--- OPTIMAL THERMOELECTRIC MATERIAL DISCOVERED (PARALLEL) ---")
    print(f"Substance: {global_best.get('substance', 'Unknown')}")
    print(f"Bond Type: {global_best.get('bond_type', 'Unknown')}")
    print(f"Confidence: {global_best.get('confidence', 0):.2%}")
    print(f"Energy Density: {global_best['energy_density']:.4f}")
    print(f"Vorticity Vector: {global_best['vorticity']}")
    print(f"Relativistic Coupling: {global_best['coupling']:.4f}")
    print(f"Maximum R-ZT: {global_best['efficiency']:.4f}")
    print(f"Search Duration: {duration:.2f} seconds")
    print("------------------------------------------------------------")

    # Save the best finding from this run to the persistent database
    save_to_db(global_best)

    return global_best

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--total_iterations", type=int, default=1000)
    args = parser.parse_args()
    parallel_search(total_iterations=args.total_iterations)
