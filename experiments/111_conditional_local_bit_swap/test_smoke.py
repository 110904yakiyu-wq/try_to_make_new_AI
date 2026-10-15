#!/usr/bin/env python3
"""Lightweight integrity checks without running the full 111 assay."""
import importlib.util
from pathlib import Path

path = Path(__file__).with_name("run.py")
spec = importlib.util.spec_from_file_location("exp111", path)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
m = v.m

def main():
    blank = bytes(m.SIZE)
    assert m.SIZE == 60 and m.CENTER == 30 and m.CENTER % 3 == 0
    assert m.step(blank, 0, "left") == blank
    assert v.first_mask(blank) == frozenset()
    assert len(v.response(blank, 29, 32)) == 6  # probe cardinality invariant
    recipient = bytearray(blank)
    recipient[30] = 1
    donor = bytearray(recipient)
    donor[30] = 3
    recipient, donor = bytes(recipient), bytes(donor)
    assert v.changed_patches(donor, recipient, {30}, 1) == [(30,)]
    assert v.replace(recipient, donor, (30,)) == donor
    x, attempts = v.null_replacements(recipient, (30,), v.first_mask(recipient),
                                      5, 0, 1, 4, 64)
    assert attempts <= 64
    assert all(candidate[30] != 1 and candidate[30] > 0 for candidate in x)
    assert all(v.first_mask(candidate) == v.first_mask(recipient) for candidate in x)
    assert v.score(("censored", "static"), ("connected", "static"),
                   ("static", "connected")) == (1, 1, 2)
    print("smoke: PASS")

if __name__ == "__main__":
    main()
