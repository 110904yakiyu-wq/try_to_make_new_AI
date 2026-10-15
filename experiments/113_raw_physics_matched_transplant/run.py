#!/usr/bin/env python3
"""Experiment 113: exact physical-feature-matched replacement nulls.

Frozen 112/111 reference cohort and response panel; no kernel modification.
All physical-null values are enumerated before response probing, excluding
both recipient values and the exact original G0 patch to avoid identity nulls.
"""
import argparse
import importlib.util
import itertools
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
SOURCE = PARENT / '112_probe_discrimination_audit' / 'transplant.py'
spec = importlib.util.spec_from_file_location('exp112_transplant', SOURCE)
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
r, e, m = t.r, t.e, t.m

FEATURES = ('popcount', 'neighbor_and', 'first_tick_flips')
TIERS = ('mask', 'popcount', 'pop_and', 'pop_and_flips')


def physical_features(frame):
    nxt = m.step(frame, 0, 'left')
    n = len(frame)
    return (sum(value.bit_count() for value in frame),
            sum((frame[i] & frame[(i + 1) % n]).bit_count() for i in range(n)),
            sum((a ^ b).bit_count() for a, b in zip(frame, nxt)))


def unique_mask_pool(recipient, donor, patch, mask):
    """Exhaustive legal value assignments at changed sites, excluding G0 patch."""
    choices = [tuple(value for value in range(1, 16) if value != recipient[i])
               for i in patch]
    for vals in itertools.product(*choices):
        buf = bytearray(recipient)
        for pos, val in zip(patch, vals):
            buf[pos] = val
        candidate = bytes(buf)
        # Always exclude EXACT transplanted patch, even if rest of donor differs.
        if all(candidate[pos] == donor[pos] for pos in patch):
            continue
        if e.first_mask(candidate) == mask:
            yield candidate


def conditions(pool, donor_features):
    tiers = {key: [] for key in TIERS}
    for state, f in pool:
        tiers['mask'].append(state)
        if f[0] == donor_features[0]:
            tiers['popcount'].append(state)
            if f[1] == donor_features[1]:
                tiers['pop_and'].append(state)
                if f[2] == donor_features[2]:
                    tiers['pop_and_flips'].append(state)
    return tiers


def analyze(records):
    """Aggregate over patches within parent, then over informative parents.

    The full mask-only null is also restricted to the SAME eligible patches
    within each stronger tier, separating eligibility shifts from matching.
    """
    summary = {}
    for width in (1, 2, 3):
        rwidth = [a for a in records if a['width'] == width]
        rows = {}
        for tier in TIERS:
            rsel = [rec for rec in rwidth if rec['eligible'][tier]]
            pmap = defaultdict(list)
            for rec in rsel:
                if rec['informative_probes']:
                    pmap[rec['parent_id']].append(rec)
            details = []
            for pid, items in sorted(pmap.items()):
                donor = statistics.mean(x['donor_confirmed'] / x['informative_probes'] for x in items)
                null = statistics.mean(x['null_expected_confirmed'][tier] / x['informative_probes'] for x in items)
                common_mask = statistics.mean(x['null_expected_confirmed']['mask'] / x['informative_probes'] for x in items)
                details.append({'parent_id': pid, 'patches': len(items),
                                'donor': donor, 'mask_null_same_patches': common_mask,
                                'feature_null': null, 'difference': donor-null,
                                'mask_difference_same_patches': donor-common_mask})
            differences = [x['difference'] for x in details]
            def sign(v):
                return 0 if abs(v) < 1e-12 else (1 if v > 0 else -1)
            rows[tier] = {
                'eligible_patches': len(rsel),
                'eligible_parents_all': len({a['parent_id'] for a in rsel}),
                'eligible_informative_parents': len(details),
                'eligible_informative_patches': sum(len(x) for x in pmap.values()),
                'total_eligible_null_microstates': sum(rec['pool_sizes'][tier] for rec in rsel),
                'null_microstate_probe_applications': sum(rec['pool_sizes'][tier] * rec['informative_probes'] for rec in rsel),
                'parent_mean_donor': statistics.mean(x['donor'] for x in details) if details else None,
                'parent_mean_mask_null_same_patches': statistics.mean(x['mask_null_same_patches'] for x in details) if details else None,
                'parent_mean_feature_null': statistics.mean(x['feature_null'] for x in details) if details else None,
                'parent_mean_donor_minus_feature_null': statistics.mean(differences) if differences else None,
                'parent_mean_donor_minus_mask_null_same_patches': statistics.mean(x['mask_difference_same_patches'] for x in details) if details else None,
                'parent_mean_mask_null_minus_feature_null': statistics.mean(x['mask_null_same_patches']-x['feature_null'] for x in details) if details else None,
                'parent_wins': sum(sign(x)>0 for x in differences),
                'parent_losses': sum(sign(x)<0 for x in differences),
                'parent_ties': sum(sign(x)==0 for x in differences),
                'donor_censored_probe_applications': sum(x['donor_censored'] for x in rsel),
                'null_censored_probe_applications': sum(x['null_censored_microstates'][tier] for x in rsel),
                'parent_details': details,
            }
        summary[str(width)] = rows
    return summary


def assay(reference_file, cohort_limit=None, census_only=False):
    raw = json.loads(Path(reference_file).read_text(encoding='utf-8'))
    refs = r.decode_archive(raw)
    if refs['parameters']['ticks'] != 500 or refs['parameters']['attempts'] != 100:
        raise ValueError('Requires 112 500-tick 100-attempt frozen reference')
    if refs['inventory']['equal_first_mask_pairs'] != 20 or refs['inventory']['G0_checked'] != 130:
        raise ValueError('112 reference cohort mismatch')
    ids = {p['parent_id']: p for p in refs['parent_records']}
    original_orbit = m.orbit
    def bounded(*args, **kw):
        kw.setdefault('max_ticks', 500)
        return original_orbit(*args, **kw)
    m.orbit = bounded
    records = []
    inventory = Counter()
    try:
        for pid, (seed, donor, parent) in enumerate(m.parents('left')):
            if pid not in ids:
                continue
            if cohort_limit is not None and inventory['matched_parents'] >= cohort_limit:
                break
            match = e.v.matched_control(pid, donor, parent, 100)
            if match is None: raise AssertionError('Frozen 112 parent not matched')
            recipient, _, attempt = match
            rec = ids[pid]
            assert rec['seed'] == list(seed) and rec['control_match_attempt'] == attempt
            assert rec['union_support'] == sorted(parent['support'])
            mask = e.first_mask(donor)
            assert mask == e.first_mask(recipient) and rec['first_mask'] == sorted(mask)
            sites = e.probe_sites(parent['support'])
            informative = tuple((p['side'], p['raw']) for p in rec['probes'] if p['class_disagreement'])
            refmap = {(p['side'], p['raw']): p for p in rec['probes']}
            inventory['matched_parents'] += 1
            inventory['informative_parents'] += bool(informative)
            for width in (1, 2, 3):
                for rank, patch in enumerate(e.changed_patches(donor, recipient, parent['support'], width)):
                    transplant = e.replace(recipient, donor, patch)
                    if e.first_mask(transplant) != mask: continue
                    inventory[f'width{width}_g0_mask_eligible'] += 1
                    donor_f = physical_features(transplant)
                    pool = [(cand, physical_features(cand)) for cand in unique_mask_pool(recipient, donor, patch, mask)]
                    eligible = conditions(pool, donor_f)
                    for tier in TIERS:
                        if eligible[tier]:inventory[f'width{width}_{tier}_eligible'] += 1
                    record = {'parent_id': pid, 'width': width, 'patch': list(patch),
                              'informative_probes': len(informative),
                              'donor_features': dict(zip(FEATURES, donor_f)),
                              'pool_sizes': {k: len(v) for k,v in eligible.items()},
                              'eligible': {k: bool(v) for k,v in eligible.items()},
                              'donor_confirmed': None, 'donor_censored': None,
                              'null_expected_confirmed': {}, 'null_censored_microstates': {}}
                    if not census_only:
                        record['donor_confirmed'], record['donor_censored'] = t.score(transplant, sites, informative, refmap)
                        # Enumerate each distinct mask-qualified alternative exactly once.
                        # Nested feature conditions reuse its result, no RNG sampling.
                        outcome = {state: t.score(state, sites, informative, refmap)
                                   for state, _ in pool} if informative else {}
                        for tier in TIERS:
                            if not eligible[tier]: continue
                            if informative:
                                vals = [outcome[state] for state in eligible[tier]]
                                record['null_expected_confirmed'][tier] = statistics.mean(x[0] for x in vals)
                                record['null_censored_microstates'][tier] = sum(x[1] for x in vals)
                            else:
                                record['null_expected_confirmed'][tier] = None
                                record['null_censored_microstates'][tier] = 0
                    records.append(record)
    finally:
        m.orbit = original_orbit
    return {'experiment': 113, 'design': 'exact nonidentical raw-bit alternatives under nested post-transplant physical-feature constraints',
            'parameters': {'reference': '112 results/default.json', 'horizon': 500,
                'mask': 'exact first autonomous changed-site set, phase 0',
                'tiers': list(TIERS), 'features': list(FEATURES), 'widths': [1,2,3],
                'null_repeats_per_eligible_patch': 'ALL (exact enumeration)',
                'null_pool': 'exhaustive nonzero assignments differing at every edited site; exclude donor patch identity; filter exact features before response assays',
                'cohort_limit': cohort_limit, 'census_only': census_only},
            'inventory': dict(sorted(inventory.items())),
            'summary': {} if census_only else analyze(records),
            'patch_records': records}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reference', type=Path, default=PARENT / '112_probe_discrimination_audit' / 'results/default.json')
    ap.add_argument('--output', type=Path, default=None)
    ap.add_argument('--cohort-limit', type=int, default=None)
    ap.add_argument('--census-only', action='store_true')
    args = ap.parse_args()
    if args.cohort_limit is not None and args.cohort_limit < 1:
        ap.error('positive cohort-limit expected')
    result = assay(args.reference, args.cohort_limit, args.census_only)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    brief = {k: result[k] for k in ('parameters','inventory')}
    brief['summary'] = {width: {tier: {k:v for k,v in rows.items() if k!='parent_details'}
                                for tier, rows in data.items()}
                        for width, data in result['summary'].items()}
    print(json.dumps(brief, indent=2, sort_keys=True))

if __name__ == '__main__': main()
