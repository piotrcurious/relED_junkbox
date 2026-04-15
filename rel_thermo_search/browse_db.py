import json
import os
import sys

def browse_db(min_efficiency=None, search_term=None):
    db_file = os.path.join(os.path.dirname(__file__), "discovered_materials.json")
    if not os.path.exists(db_file):
        print("Database not found.")
        return

    with open(db_file, 'r') as f:
        db = json.load(f)

    filtered = db
    if min_efficiency:
        filtered = [m for m in filtered if m['efficiency'] >= float(min_efficiency)]
    if search_term:
        filtered = [m for m in filtered if search_term.lower() in m.get('substance', '').lower()]

    print(f"{'#':<3} | {'Substance':<40} | {'R-ZT':<10} | {'Stability':<10}")
    print("-" * 75)
    for i, m in enumerate(filtered[:20]): # Show top 20
        print(f"{i+1:<3} | {m.get('substance', 'Theoretical'):<40} | {m['efficiency']:<10.2f} | {m.get('stability', 1.0):<10.2f}")

if __name__ == "__main__":
    eff = sys.argv[1] if len(sys.argv) > 1 else None
    term = sys.argv[2] if len(sys.argv) > 2 else None
    browse_db(eff, term)
