import json
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "discovered_materials.json")

def load_db():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_to_db(new_materials):
    """
    Appends new findings to the existing database and saves.
    """
    db = load_db()
    # If new_materials is a single dict, wrap in list
    if isinstance(new_materials, dict):
        new_materials = [new_materials]

    db.extend(new_materials)

    # Optional: Deduplicate or sort by efficiency
    db.sort(key=lambda x: x.get('efficiency', 0), reverse=True)

    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)

    print(f"Database updated. Total materials in vault: {len(db)}")

if __name__ == "__main__":
    # Test DB
    save_to_db({"name": "Test Vortex", "efficiency": 123.45})
    print(load_db())
