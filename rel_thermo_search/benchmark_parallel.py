import time
import os
from find_thermo_materials import search_materials
from parallel_search import parallel_search

def run_benchmark(iterations=5000):
    print(f"--- BENCHMARKING THERMOELECTRIC SEARCH ({iterations} iterations) ---")

    # Sequential
    print("Running Sequential Search...")
    start_seq = time.time()
    search_materials(iterations=iterations)
    end_seq = time.time()
    seq_duration = end_seq - start_seq

    # Parallel
    print("\nRunning Parallel Search...")
    start_par = time.time()
    parallel_search(total_iterations=iterations)
    end_par = time.time()
    par_duration = end_par - start_par

    print("\n--- RESULTS ---")
    print(f"Sequential Duration: {seq_duration:.4f}s")
    print(f"Parallel Duration:   {par_duration:.4f}s")
    print(f"Speedup Factor:      {seq_duration / par_duration:.2f}x")
    print("-" * 45)

if __name__ == "__main__":
    run_benchmark()
