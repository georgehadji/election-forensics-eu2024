import sys
from pathlib import Path
import yaml

REGISTRY_PATH = Path("literature/literature_registry.yaml")

def main():
    print("Literature ingestion semantic check")

    if not REGISTRY_PATH.exists():
        print("Registry file missing")
        return 1

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        entries = yaml.safe_load(f) or []

    for idx, entry in enumerate(entries):
        if entry.get("method_category") is None:
            print(f"Entry {idx} missing method_category")
            return 1

    print("Literature registry schema check passed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
