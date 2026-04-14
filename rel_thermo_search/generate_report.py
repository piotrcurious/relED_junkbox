import json
import os
from datetime import datetime

def generate_report():
    db_file = os.path.join(os.path.dirname(__file__), "discovered_materials.json")
    if not os.path.exists(db_file):
        print("No database found to report.")
        return

    with open(db_file, 'r') as f:
        db = json.load(f)

    if not db:
        print("Database is empty.")
        return

    # Sort by efficiency
    db.sort(key=lambda x: x.get('efficiency', 0), reverse=True)

    report_path = os.path.join(os.path.dirname(__file__), "discovery_report.txt")
    with open(report_path, 'w') as f:
        f.write("RELATIVISTIC THERMOELECTRIC DISCOVERY REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 45 + "\n\n")

        f.write(f"Total Materials Discovered: {len(db)}\n\n")

        f.write("TOP 5 CANDIDATES:\n")
        f.write("-" * 15 + "\n")
        for i, mat in enumerate(db[:5]):
            f.write(f"{i+1}. {mat.get('substance', 'Theoretical Compound')}\n")
            f.write(f"   R-ZT: {mat['efficiency']:.4f}\n")
            f.write(f"   Bond Type: {mat.get('bond_type', 'N/A')}\n")
            f.write(f"   Confidence: {mat.get('confidence', 0):.2%}\n")
            f.write(f"   Parameters: E={mat['energy_density']:.2f}, V={mat['vorticity']}, C={mat['coupling']:.2f}\n\n")

        f.write("\nEnd of Report.\n")

    print(f"Report generated: {report_path}")

if __name__ == "__main__":
    generate_report()
