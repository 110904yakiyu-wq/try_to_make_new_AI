#!/usr/bin/env python3
"""Secondary Experiment-111 audit: censor-aware response-distance metric.

Donor=G0; recipient=Experiment-108 exact-geometry on-cycle control.
Condition BEFORE any material-response query on equal unperturbed first-tick
changed-site sets. Then allow only site swaps preserving this same set.
Compare the G0-directed one-window swap against a pre-response fixed-seed sample of admissible other
nonzero values at that site, using the identical immediate execution mask.
The stricter null also matches the number of changed bits in that window.
Six post-material probes are measured ONLY after fixing the intervention pool.
Parent, not probe/replacement, is the inferential sampling unit.
"""
import argparse
import csv
import importlib.util
import json
import random
import statistics
from functools import lru_cache
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / '108_cycle_union_geometry_match' / 'run.py'
spec = importlib.util.spec_from_file_location('exp108', BASE)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
m = v.m

PROBES = (1, 7, 15)
MASK_BUDGET = 500


def initial_mask(s):
    updated = m.step(s, 0, 'left')
    return frozenset(i for i, (a, b) in enumerate(zip(s, updated)) if a != b)


def inject_sites(union):
    # Historical nonwrapping localized support, identical to Experiment 109.
    indices = sorted(union)
    assert indices and indices[0] > 0 and indices[-1] < m.SIZE - 1
    return (indices[0] - 1, indices[-1] + 1)


@lru_cache(maxsize=30000)
def signature(frame, sites):
    response = []
    for pos in sites:
        assert frame[pos] == 0
        for raw in PROBES:
            s = bytearray(frame)
            s[pos] = raw
            res = m.orbit(bytes(s), phase=0, direction='left')
            if res['status'] != 'cycle':
                response.append('censored')
            elif res['active'] and len(m.components(res['support'], m.SIZE)) == 1:
                response.append('connected_active')
            else:
                response.append('other_cycle')
    return tuple(response)


def distance(x, y):
    assert len(x) == len(y) == 2 * len(PROBES)
    return sum(a != b for a, b in zip(x, y))


@lru_cache(maxsize=30000)
def probe_mask_profile(frame, sites):
    profiles = []
    for pos in sites:
        for raw in PROBES:
            s = bytearray(frame)
            s[pos] = raw
            profiles.append(initial_mask(bytes(s)))
    return tuple(profiles)


def transplant(recipient, pos, value):
    result = bytearray(recipient)
    result[pos] = value
    return bytes(result)


def evaluate_pair(index, pair, donor, recipient, union, rows, null_per_site, require_probe_mask):
    expected = initial_mask(donor)
    if expected != initial_mask(recipient):
        return False

    sites = inject_sites(union)
    original_profile = probe_mask_profile(recipient, sites)
    donor_profile = probe_mask_profile(donor, sites)
    if require_probe_mask and original_profile != donor_profile:
        return True
    recipient_sig = signature(recipient, sites)
    donor_sig = signature(donor, sites)
    gap = distance(recipient_sig, donor_sig)
    parent_changed = [i for i in range(m.SIZE) if donor[i] != recipient[i]]

    for pos in parent_changed:
        assert donor[pos] != 0 and recipient[pos] != 0
        actual = transplant(recipient, pos, donor[pos])
        if initial_mask(actual) != expected:
            continue
        if require_probe_mask and probe_mask_profile(actual, sites) != original_profile:
            continue

        # Construct the whole null set using only physical, pre-outcome facts.
        all_nulls = [other for other in range(1, 16)
                 if other not in (recipient[pos], donor[pos])
                 and initial_mask(transplant(recipient, pos, other)) == expected
                 and (not require_probe_mask or
                      probe_mask_profile(transplant(recipient, pos, other), sites) == original_profile)]
        if not all_nulls:
            continue

        wanted_flip = (recipient[pos] ^ donor[pos]).bit_count()
        all_strict_nulls = [x for x in all_nulls
                        if (recipient[pos] ^ x).bit_count() == wanted_flip]
        # Pre-register random samples independently of every outcome.
        rng1 = random.Random(111_000_000 + index * 1000 + pos * 2)
        rng2 = random.Random(111_000_001 + index * 1000 + pos * 2)
        nulls = rng1.sample(all_nulls, min(null_per_site, len(all_nulls)))
        strict_nulls = rng2.sample(all_strict_nulls, min(null_per_site, len(all_strict_nulls)))
        actual_sig = signature(actual, sites)
        actual_gain = gap - distance(actual_sig, donor_sig)
        all_gains = [gap - distance(signature(transplant(recipient, pos, x), sites), donor_sig)
                     for x in nulls]
        strict_gains = [gap - distance(signature(transplant(recipient, pos, x), sites), donor_sig)
                        for x in strict_nulls]

        # A separate diagnostic, NOT conditioned on to select interventions.
        probe_mask_agree = 0
        for probe_pos in sites:
            for raw in PROBES:
                def changed_after_probe(frame):
                    s = bytearray(frame)
                    s[probe_pos] = raw
                    return initial_mask(bytes(s))
                if (changed_after_probe(donor) == changed_after_probe(recipient)
                        == changed_after_probe(actual)):
                    probe_mask_agree += 1

        rows.append(dict(parent_index=index, seed_a=pair[0], seed_b=pair[1],
                         site=pos, donor_raw=donor[pos], recipient_raw=recipient[pos],
                         donor_recipient_gap=gap, actual_gain=actual_gain,
                         actual_exact_transfer=int(actual_sig == donor_sig),
                         mask_null_pool=len(all_nulls), mask_null_count=len(nulls), mask_null_mean_gain=statistics.mean(all_gains),
                         bitflip_null_pool=len(all_strict_nulls), bitflip_null_count=len(strict_nulls),
                         bitflip_null_mean_gain=(statistics.mean(strict_gains) if strict_gains else ''),
                         probe_mask_agree=probe_mask_agree))
    return True


def direction(vals, eps=1e-9):
    return (sum(x > eps for x in vals), sum(x < -eps for x in vals),
            sum(abs(x) <= eps for x in vals))


def report(name, parent_summary):
    if not parent_summary:
        print(f'{name}: informative_parents=0')
        return
    actual = [x[0] for x in parent_summary]
    null = [x[1] for x in parent_summary]
    excess = [a-b for a, b in parent_summary]
    p, n, t = direction(excess)
    print(f'{name}: informative_parents={len(parent_summary)} '
          f'parent_mean_actual_gain={statistics.mean(actual):.6f} '
          f'parent_mean_null_gain={statistics.mean(null):.6f} '
          f'parent_mean_excess={statistics.mean(excess):.6f} '
          f'excess_positive={p} excess_negative={n} excess_tie={t}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--attempts', type=int, default=100)
    ap.add_argument('--max-ticks', type=int, default=MASK_BUDGET)
    ap.add_argument('--null-per-site', type=int, default=2,
                    help='fixed pre-response sample budget per null stratum')
    ap.add_argument('--require-probe-mask', action='store_true',
                    help='secondary: also preserve first-tick changed-site masks for all six material probes')
    ap.add_argument('--limit-parents', type=int, default=0,
                    help='debugging only; 0 evaluates all 130 parents')
    ap.add_argument('--output-csv', type=Path, default=Path(__file__).with_name('results')/'site_trials.csv')
    args = ap.parse_args()
    if args.attempts < 1 or args.max_ticks < 1 or args.limit_parents < 0 or args.null_per_site < 1:
        ap.error('invalid positive budget')
    original = m.orbit
    def bounded(*a, **kw):
        kw.setdefault('max_ticks', args.max_ticks)
        return original(*a, **kw)
    m.orbit = bounded

    rows = []
    matched = 0
    eligible = 0
    total = 0
    equal_mask_indices = []
    for index, (pair, frame, parent) in enumerate(m.parents('left')):
        if args.limit_parents and total >= args.limit_parents:
            break
        total += 1
        control = v.matched_control(index, frame, parent, args.attempts)
        if control is None:
            continue
        matched += 1
        recipient, control_orbit, _ = control
        assert parent['period'] == control_orbit['period']
        assert parent['support'] == control_orbit['support']
        assert all(bool(a) == bool(b) for a, b in zip(frame, recipient))
        if evaluate_pair(index, pair, frame, recipient, parent['support'], rows, args.null_per_site, args.require_probe_mask):
            eligible += 1
            equal_mask_indices.append(index)

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    fields = ['parent_index','seed_a','seed_b','site','donor_raw','recipient_raw',
              'donor_recipient_gap','actual_gain','actual_exact_transfer',
              'mask_null_pool','mask_null_count','mask_null_mean_gain',
              'bitflip_null_pool','bitflip_null_count','bitflip_null_mean_gain','probe_mask_agree']
    with args.output_csv.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    informative = [r for r in rows if r['donor_recipient_gap'] > 0]
    parents = sorted({r['parent_index'] for r in rows})
    inform_parents = sorted({r['parent_index'] for r in informative})
    print(f'assay=111_secondary_censor_aware experiment=111 parents_examined={total} exact_geometry_matched={matched} '
          f'equal_initial_mask={eligible} eligible_sites={len(rows)} '
          f'parents_with_eligible_site={len(parents)}')
    print('physics=exp093/104 fixed 60x4-bit ring; left rotate; scheduler phase0')
    print('matching=period+cycle_union_sites+phase0_occupancy+phase0_changed_sites')
    print('intervention=single_nonzero_4bit_window; pre-material_changed_mask_preserved')
    print('probe_changed_mask_strict='+str(args.require_probe_mask).lower())
    print('probe=left/right external boundary x raw_1,7,15; horizon='+str(args.max_ticks))
    print('signature_labels=connected_active,other_cycle,censored')
    print(f'control=preoutcome_fixed_seed_sample_from_same_site_same_changed_mask; per_site={args.null_per_site}')
    print('strict_control=add_equal_4bit_flip_distance_from_recipient')
    print(f'informative_sites={len(informative)} informative_parents={len(inform_parents)} '
          f'no_gap_sites={len(rows)-len(informative)} '
          f'actual_exact_signature_transfers={sum(r["actual_exact_transfer"] for r in informative)}')
    print('equal_mask_parent_indices='+json.dumps(equal_mask_indices))
    print('probe_changed_mask_preserved_on_all_six='+str(sum(r['probe_mask_agree']==6 for r in rows))
          +'/'+str(len(rows)))
    for label, f in [('mask_only', 'mask_null_mean_gain'),
                     ('mask_plus_equal_bitflip', 'bitflip_null_mean_gain')]:
        summaries = []
        for ix in inform_parents:
            eligible_rows = [r for r in informative if r['parent_index']==ix and r[f]!='']
            if eligible_rows:
                summaries.append((statistics.mean(r['actual_gain'] for r in eligible_rows),
                                  statistics.mean(r[f] for r in eligible_rows)))
        report(label, summaries)
    try:
        portable_csv = args.output_csv.resolve().relative_to(Path(__file__).resolve().parents[2])
    except ValueError:
        portable_csv = args.output_csv
    print('csv='+str(portable_csv))
    print('NOTE no conditional causal mechanism proven; non-oncycle hybrids; censored != failure')
    if args.limit_parents:
        print('DEBUG_PARTIAL_RUN not for published scientific conclusions')

if __name__ == '__main__':
    main()
