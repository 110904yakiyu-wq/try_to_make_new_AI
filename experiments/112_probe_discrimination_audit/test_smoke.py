#!/usr/bin/env python3
"""Fast archival/physics-contract regression checks for Experiment 112."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("exp112", ROOT / "run.py")
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


def main():
    assert r.m.SIZE == 60 and r.m.CENTER == 30 and r.m.CENTER % 3 == 0
    assert r.m.step(bytes(r.m.SIZE), 0, "left") == bytes(r.m.SIZE)
    assert len(r.RAW_VALUES) == 15 and r.LEGACY == (1, 7, 15)
    archive = json.loads((ROOT / "results/default.json").read_text(encoding="utf-8"))
    full = r.decode_archive(archive)
    assert r.encode_archive(full) == archive
    assert r.analyze_records(full["parent_records"]) == archive["summary"]
    assert (archive["inventory"]["G0_checked"], archive["inventory"]["exact108_pairs"],
            archive["inventory"]["equal_first_mask_pairs"]) == (130, 55, 20)
    assert len(full["parent_records"]) == 20
    assert archive["summary"]["six"]["aggregate"]["class_disagreement"] == 2
    assert archive["summary"]["all30"]["aggregate"]["class_disagreement"] == 10
    assert archive["summary"]["six"]["parents_with_any"]["class_disagreement"] == 2
    assert archive["summary"]["all30"]["parents_with_any"]["class_disagreement"] == 8
    assert archive["summary"]["all30"]["aggregate"]["both_resolved"] == 420
    assert archive["summary"]["all30"]["aggregate"]["at_least_one_censored"] == 180
    # Each parent contributes exactly 15 probes at both boundaries.
    for p in full["parent_records"]:
        assert [(x["side"], x["raw"]) for x in p["probes"]] == [
            (side, raw) for side in ("left", "right") for raw in range(1, 16)]
    transplanted = json.loads((ROOT / "results/transplant.json").read_text(encoding="utf-8"))
    assert transplanted["inventory"]["same_first_mask_pairs"] == 20
    assert transplanted["inventory"]["informative_parents"] == 8
    assert len(transplanted["patch_records"]) == 71
    assert [transplanted["summary"][str(w)]["matched_patches"] for w in (1,2,3)] == [35,16,20]
    assert [transplanted["summary"][str(w)]["informative_parents_with_matched_patches"]
            for w in (1,2,3)] == [8,5,6]
    # No confirmation is allowed to exceed the frozen informative denominator.
    for p in transplanted["patch_records"]:
        assert 0 <= p["donor_confirmed"] <= p["informative_probes"]
        assert 0 <= p["donor_censored"] <= p["informative_probes"]
        assert len(p["null_confirmed"]) == 4
        assert all(0 <= n <= p["informative_probes"] for n in p["null_confirmed"])
    print("exp112 smoke: PASS")


if __name__ == "__main__":
    main()
