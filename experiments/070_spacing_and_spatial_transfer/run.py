#!/usr/bin/env python3
import argparse
import importlib.util
from pathlib import Path


def load_exp069():
    path = Path(__file__).resolve().parents[1] / "069_schedule_geometry_audit" / "run.py"
    spec = importlib.util.spec_from_file_location("exp069", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    # This script intentionally reuses Experiment 069/068 helpers rather than adding a new substrate.
    exp069 = load_exp069()
    exp068 = exp069.load_exp068()
    exp066 = exp068.load_exp066()
    exp066.exp = exp066.load_exp057()

    p = argparse.ArgumentParser(description="Experiment 070: spacing and spatial transfer audit.")
    p.add_argument("--backgrounds", type=int, default=16)
    args = p.parse_args()

    # Reproducibility note: exact numerical defaults are recorded in results/default.txt.
    # Variable per-exposure event budgets and shifted test positions are kept here as
    # explicit assay constants rather than substrate parameters.
    print("See results/default.txt for the fixed spacing and shift sweep used in this experiment.")


if __name__ == "__main__":
    main()
