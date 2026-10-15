#!/usr/bin/env python3
"""Experiment 111: local value transplants conditioned on first-tick mask.

Only on-cycle 108 pairs with a common first-tick changed-site mask are
eligible. Patches and mask-conditioned nulls are chosen without any material
response test. The six-probe assay is deliberately resource bounded.
"""
import argparse
import importlib.util
import json
import random
import statistics
from collections import Counter
from functools import lru_cache
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "108_cycle_union_geometry_match" / "run.py"
spec = importlib.util.spec_from_file_location("exp108", BASE)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
m = v.m
PROBES = (1, 7, 15)
SIZES = (1, 2, 3)


def first_mask(frame):
    after = m.step(frame, 0, "left")
    return frozenset(i for i, (before, nxt) in enumerate(zip(frame, after)) if before != nxt)


def changed_patches(donor, recipient, support, width):
    """All contiguous width-window sites, entirely changed donor vs recipient."""
    altered = {i for i, (a, b) in enumerate(zip(donor, recipient)) if a != b}
    return sorted({tuple((start + j) % m.SIZE for j in range(width))
                   for start in support
                   if all((start + j) % m.SIZE in altered for j in range(width))})


def replace(recipient, source, patch):
    copied = bytearray(recipient)
    for i in patch:
        copied[i] = source[i]
    return bytes(copied)


def null_replacements(recipient, patch, expected_mask, parent_id, patch_rank,
                      width, repeats, budget):
    rng = random.Random(111_000_001 + 1_000_003 * parent_id
                        + 10_007 * width + 101 * patch_rank)
    accepted = []
    attempts = 0
    while attempts < budget and len(accepted) < repeats:
        attempts += 1
        frame = bytearray(recipient)
        for site in patch:
            # Control and donor use the same changed-site count and occupancy.
            frame[site] = rng.choice([b for b in range(1, 16)
                                      if b != recipient[site]])
        out = bytes(frame)
        if first_mask(out) == expected_mask:
            accepted.append(out)
    return accepted, attempts


def probe_sites(parent_union):
    positions = sorted(parent_union)
    return ((positions[0] - 1) % m.SIZE, (positions[-1] + 1) % m.SIZE)


@lru_cache(maxsize=None)
def response(frame, left, right):
    result = []
    for site in (left, right):
        assert frame[site] == 0
        for raw in PROBES:
            s = bytearray(frame)
            s[site] = raw
            r = m.orbit(bytes(s), phase=0, direction="left")
            if r["status"] != "cycle":
                result.append("censored")
            elif not r["active"]:
                result.append("static")
            elif len(components(r["support"])) == 1:
                result.append("connected")
            else:
                result.append("fragmented")
    return tuple(result)


def components(support):
    """Count ring-connected components, independent of daughter viability."""
    remaining = set(support)
    count = 0
    while remaining:
        count += 1
        todo = [remaining.pop()]
        while todo:
            x = todo.pop()
            for y in ((x - 1) % m.SIZE, (x + 1) % m.SIZE):
                if y in remaining:
                    remaining.remove(y)
                    todo.append(y)
    return [None] * count


def score(sig, target, baseline):
    # Denominator fixed across actual/null arms; timeouts cannot confirm transfer.
    informative = [i for i in range(len(target))
                   if target[i] != "censored" and baseline[i] != "censored"
                   and target[i] != baseline[i]]
    confirmed = sum(sig[i] == target[i] and sig[i] != "censored"
                    for i in informative)
    censored = sum(sig[i] == "censored" for i in informative)
    return confirmed, censored, len(informative)


def assay(attempts, ticks, repeats, budget, max_parents):
    original_orbit = m.orbit
    def finite(*args, **kwargs):
        kwargs.setdefault("max_ticks", ticks)
        return original_orbit(*args, **kwargs)
    m.orbit = finite
    records = []
    inventory = Counter()
    parent_records = []
    try:
        for parent_id, (pair, donor, parent) in enumerate(m.parents("left")):
            if max_parents is not None and parent_id >= max_parents:
                break
            inventory["G0_parents_checked"] += 1
            matched = v.matched_control(parent_id, donor, parent, attempts)
            if matched is None:
                continue
            inventory["108_pairs"] += 1
            recipient = matched[0]
            mask = first_mask(recipient)
            if first_mask(donor) != mask:
                continue
            inventory["same_first_mask_pairs"] += 1
            sites = probe_sites(parent["support"])
            target = response(donor, *sites)
            baseline = response(recipient, *sites)
            informative = sum(a != "censored" and b != "censored" and a != b
                              for a, b in zip(target, baseline))
            pdata = {"parent_id": parent_id, "seed": list(pair),
                     "informative_probes": informative, "patches": {}}
            for width in SIZES:
                candidates = changed_patches(donor, recipient, parent["support"], width)
                inventory[f"width{width}_candidates"] += len(candidates)
                eligible = []
                for rank, patch in enumerate(candidates):
                    transplant = replace(recipient, donor, patch)
                    if first_mask(transplant) != mask:
                        continue
                    inventory[f"width{width}_donor_mask_pass"] += 1
                    nulls, tried = null_replacements(recipient, patch, mask,
                                                     parent_id, rank, width, repeats, budget)
                    inventory[f"width{width}_null_attempts"] += tried
                    if len(nulls) < repeats:
                        inventory[f"width{width}_null_shortage"] += 1
                        continue
                    inventory[f"width{width}_matched_patches"] += 1
                    # No test response is used above this point to pick a patch or null.
                    ds = response(transplant, *sites)
                    actual = score(ds, target, baseline)
                    ns = [score(response(fake, *sites), target, baseline) for fake in nulls]
                    assert all(x[2] == actual[2] for x in ns)
                    record = {"parent_id": parent_id, "width": width, "patch": list(patch),
                              "baseline_discordant_resolved": informative,
                              "donor_confirmed": actual[0], "donor_censored": actual[1],
                              "null_confirmed": [x[0] for x in ns],
                              "null_censored": [x[1] for x in ns]}
                    eligible.append(record)
                    records.append(record)
                pdata["patches"][str(width)] = len(eligible)
            parent_records.append(pdata)
    finally:
        m.orbit = original_orbit
        response.cache_clear()
    summary = {}
    for width in SIZES:
        rows = [r for r in records if r["width"] == width]
        group = {}
        for r in rows:
            group.setdefault(r["parent_id"], []).append(r)
        evaluable = {p: rr for p, rr in group.items() if rr[0]["baseline_discordant_resolved"] > 0}
        diffs = []
        g0_rate = []
        null_rate = []
        for parent, rr in evaluable.items():
            donor = statistics.mean(r["donor_confirmed"] / r["baseline_discordant_resolved"] for r in rr)
            null = statistics.mean(statistics.mean(r["null_confirmed"]) /
                                   r["baseline_discordant_resolved"] for r in rr)
            g0_rate.append(donor)
            null_rate.append(null)
            diffs.append(donor - null)
        summary[str(width)] = {
            "mask_matched_patches": len(rows), "parents_with_matched_patches": len(group),
            "parents_with_informative_resolved_probes": len(evaluable),
            "mean_donor_confirmed_fraction": statistics.mean(g0_rate) if g0_rate else None,
            "mean_null_confirmed_fraction": statistics.mean(null_rate) if null_rate else None,
            "parent_mean_donor_minus_null": statistics.mean(diffs) if diffs else None,
            "parents_donor_higher": sum(x > 0 for x in diffs),
            "parents_null_higher": sum(x < 0 for x in diffs),
            "parents_tied": sum(x == 0 for x in diffs),
            "donor_censored_on_informative_probes": sum(r["donor_censored"] for r in rows),
            "null_censored_on_informative_probes": sum(sum(r["null_censored"]) for r in rows),
        }
    return {"experiment": 111, "parameters": {"attempts": attempts, "ticks": ticks,
            "null_repeats": repeats, "null_proposal_budget": budget,
            "max_parents": max_parents, "probes_per_side": list(PROBES),
            "patch_widths": list(SIZES), "direction": "left", "phase": 0,
            "selection": "same first-tick mask in G0/control pair; transplant retains it",
            "null": "fixed changed sites and occupancy, first-tick mask retained"},
            "inventory": dict(sorted(inventory.items())), "summary": summary,
            "parent_records": parent_records, "patch_records": records}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--attempts", type=int, default=100)
    ap.add_argument("--max-ticks", type=int, default=500)
    ap.add_argument("--null-repeats", type=int, default=4)
    ap.add_argument("--null-budget", type=int, default=256)
    ap.add_argument("--max-parents", type=int, default=None)
    ap.add_argument("--output", type=Path, default=None)
    args = ap.parse_args()
    if args.attempts < 1 or args.max_ticks < 1 or args.null_repeats < 1 or args.null_budget < 1:
        ap.error("attempts, max-ticks, null-repeats and null-budget must be positive")
    if args.max_parents is not None and args.max_parents < 1:
        ap.error("max-parents must be positive")
    result = assay(args.attempts, args.max_ticks, args.null_repeats,
                   args.null_budget, args.max_parents)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("parameters", "inventory", "summary")},
                     indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
