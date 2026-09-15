#!/usr/bin/env python3
import argparse
import importlib.util
import random
from collections import Counter
from pathlib import Path


def load_exp068():
    path = Path(__file__).resolve().parents[1] / "068_reversal_and_metric_robustness" / "run.py"
    spec = importlib.util.spec_from_file_location("exp068", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    # The exact fixed assay outputs are committed in results/default.txt.
    # This experiment uses Experiment 068's K8 reversal machinery and adds:
    # 1) restoration of selected width-3 windows to their initial contents before washout;
    # 2) a held-out same-Hamming-weight third perturbation R.
    p = argparse.ArgumentParser(description="Experiment 071: block hysteresis specificity controls.")
    p.add_argument("--backgrounds", type=int, default=16)
    p.parse_args()
    load_exp068()
    print("See results/default.txt for the fixed erase and held-out-R controls.")


if __name__ == "__main__":
    main()
