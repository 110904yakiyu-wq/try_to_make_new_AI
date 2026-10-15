#!/usr/bin/env python3
"""Experiment 114: time-to-cycle censoring and phase-consistent response traces.

No change to the finite-speed physical kernel, parent matching, intervention,
or preexisting class definitions. Causal response mask means a perturbed
trajectory minus its OWN no-injection deterministic trajectory, time-aligned.
"""
import argparse
import csv
import importlib.util
import json
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
SOURCE = EXP / '108_cycle_union_geometry_match' / 'run.py'
spec = importlib.util.spec_from_file_location('exp108', SOURCE)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
m = v.m

SAMPLE_TICKS = (1, 3, 6, 12, 24)
HORIZONS = (100, 250, 500, 1000, 2000)
CLASS = ('connected', 'fragmented', 'static', 'censored')


def changed_mask(before, after):
    return sum((1 << i) for i, (a, b) in enumerate(zip(before, after)) if a != b)


def response_trace(base, injected):
    """Perturbed vs its own unperturbed state at equal phase and time."""
    p = bytes(injected)
    b = bytes(base)
    assert len(p) == len(b) == m.SIZE
    out = {}
    for tick in range(1, max(SAMPLE_TICKS) + 1):
        b = m.step(b, (tick - 1) % 3, 'left')
        p = m.step(p, (tick - 1) % 3, 'left')
        if tick in SAMPLE_TICKS:
            mask = changed_mask(b, p)
            bits = sum((x ^ y).bit_count() for x, y in zip(b, p))
            out[tick] = (mask, bits)
    return out


def connected_components(support):
    remainder = set(support)
    n = 0
    while remainder:
        n += 1
        stack = [remainder.pop()]
        while stack:
            x = stack.pop()
            for y in ((x - 1) % m.SIZE, (x + 1) % m.SIZE):
                if y in remainder:
                    remainder.remove(y)
                    stack.append(y)
    return n


def extended_orbit(initial, max_ticks=2000):
    """First exact microstate+next-scheduler-phase recurrence; right censored."""
    state = bytes(initial)
    seen = {(state, 0): 0}
    frames = [state]
    for tick in range(1, max_ticks + 1):
        state = m.step(state, (tick - 1) % 3, 'left')
        key = (state, tick % 3)
        if key in seen:
            entry = seen[key]
            cycle = frames[entry:tick]
            support = {i for frame in cycle for i, x in enumerate(frame) if x}
            active = len(set(cycle)) > 1
            cls = ('static' if not active else
                   'connected' if connected_components(support) == 1 else 'fragmented')
            return dict(first_recurrence=tick, preperiod=entry,
                        period=tick - entry, cls=cls,
                        support=sorted(support))
        seen[key] = tick
        frames.append(state)
    return dict(first_recurrence=None, preperiod=None, period=None,
                cls='censored', support=None)


def snapshot_at(result, horizon):
    return result['cls'] if result['first_recurrence'] is not None and result['first_recurrence'] <= horizon else 'censored'


def reference_control(pid, donor, parent, accepted_attempt):
    # Historical 108 seed is tied to G0 catalog index and attempt, NOT seed pair.
    attempt_index = accepted_attempt - 1
    rng = random.Random(3_000_000 + pid * 300_000 + attempt_index)
    candidate = bytes(rng.randrange(1, 16) if x else 0 for x in donor)
    result = m.orbit(candidate, phase=0, direction='left', max_ticks=500)
    if result['status'] != 'cycle' or not result['active']:
        raise AssertionError('Frozen control is not on-cycle')
    if result['period'] != parent['period'] or result['support'] != parent['support']:
        raise AssertionError('Frozen cycle period or union support mismatch')
    phase0 = [f for j, f in enumerate(result['cycle']) if (result['phase'] + j) % 3 == 0]
    ctrl = max(phase0, key=lambda f: sum(bool(x) for x in f))
    if any(bool(x) != bool(y) for x, y in zip(ctrl, donor)):
        raise AssertionError('Frozen phase0 occupancy mismatch')
    return ctrl


def load_reference(path):
    frozen = json.loads(Path(path).read_text(encoding='utf-8'))
    if frozen.get('experiment') != 112 or frozen['parameters']['attempts'] != 100 or frozen['parameters']['ticks'] != 500:
        raise ValueError('Requires frozen Experiment 112 default 100-attempt 500-tick reference')
    if frozen['inventory']['G0_checked'] != 130 or frozen['inventory']['equal_first_mask_pairs'] != 20:
        raise ValueError('Unexpected historical cohort')
    if len(frozen['parent_records']) != 20:
        raise ValueError('Frozen 20-pair cohort required')
    if frozen['summary']['all30']['aggregate']['both_resolved'] != 420:
        raise ValueError('Reference 112 summary corrupted')
    return frozen


def aggregate(records):
    res = {}
    parents = defaultdict(list)
    for row in records:
        parents[row['parent_id']].append(row)
    for h in HORIZONS:
        row_counts = Counter()
        parent_diffs = []
        for pid, rows in parents.items():
            g = c = 0
            for row in rows:
                a = row['a'][str(h)]
                b = row['b'][str(h)]
                row_counts['actual_connected'] += a == 'connected'
                row_counts['control_connected'] += b == 'connected'
                row_counts['actual_censored'] += a == 'censored'
                row_counts['control_censored'] += b == 'censored'
                row_counts['both_censored'] += a == b == 'censored'
                row_counts['both_resolved'] += a != 'censored' and b != 'censored'
                row_counts['both_connected'] += a == b == 'connected'
                row_counts['resolved_class_disagreement'] += a != b and a != 'censored' and b != 'censored'
                g += a == 'connected'
                c += b == 'connected'
            parent_diffs.append((g - c) / len(rows))
        res[str(h)] = {'probe_pair_rows': len(records),
                       'aggregate': dict(sorted(row_counts.items())),
                       'parent_mean_connected_difference': statistics.mean(parent_diffs),
                       'parent_G0_higher': sum(x > 0 for x in parent_diffs),
                       'parent_control_higher': sum(x < 0 for x in parent_diffs),
                       'parent_ties': sum(x == 0 for x in parent_diffs)}

    early = {}
    for tick in SAMPLE_TICKS:
        parent_equal, parent_jaccard = [], []
        for rows in parents.values():
            parent_equal.append(statistics.mean(x['response_equal'][str(tick)] for x in rows))
            parent_jaccard.append(statistics.mean(x['response_jaccard'][str(tick)] for x in rows))
        early[str(tick)] = {
            'parent_mean_equal_response_position_mask': statistics.mean(parent_equal),
            'parent_mean_mask_jaccard': statistics.mean(parent_jaccard),
            'parent_min_equal_rate': min(parent_equal),
            'parent_max_equal_rate': max(parent_equal),
            'paired_probe_count': len(records),
            'equal_response_mask_count': sum(x['response_equal'][str(tick)] for x in records),
        }
    delayed = Counter()
    for row in records:
        for arm in ('a', 'b'):
            delayed[arm + '_censored_500'] += row[arm]['500'] == 'censored'
            delayed[arm + '_resolved_500_to_2000'] += row[arm]['500'] == 'censored' and row[arm]['2000'] != 'censored'
            delayed[arm + '_still_censored_2000'] += row[arm]['2000'] == 'censored'
        delayed['both_uncertain_500'] += row['a']['500'] == 'censored' or row['b']['500'] == 'censored'
        delayed['both_uncertain_2000'] += row['a']['2000'] == 'censored' or row['b']['2000'] == 'censored'
    class_same = [r for r in records if r['a']['500'] == r['b']['500'] and r['a']['500'] != 'censored']
    early_in_class_same = {}
    for tick in SAMPLE_TICKS:
        early_in_class_same[str(tick)] = {
            'paired_probes': len(class_same),
            'same_mask_count': sum(r['response_equal'][str(tick)] for r in class_same),
            'same_mask_fraction': statistics.mean(r['response_equal'][str(tick)] for r in class_same) if class_same else None}
    return {'horizons':res,'early':early,'delayed':dict(sorted(delayed.items())),
            'equal_500_class_early_response':early_in_class_same}


def assay(reference, max_ticks=2000, max_parents=None):
    if max_ticks != 2000:
        raise ValueError('Horizon 2000 is frozen for Experiment 114')
    historical = load_reference(reference)
    indexes = {x['parent_id']: x for x in historical['parent_records']}
    records = []
    parent_meta = []
    parents = list(m.parents('left'))
    if len(parents) != 130:
        raise AssertionError('Original G0 catalog mismatch')
    for pid, (pair, g0, parent) in enumerate(parents):
        if pid not in indexes:
            continue
        if max_parents is not None and len(parent_meta) >= max_parents:
            break
        p = indexes[pid]
        assert p['seed'] == list(pair)
        assert p['union_support'] == sorted(parent['support'])
        ctrl = reference_control(pid, g0, parent, p['control_match_attempt'])
        assert p['first_mask'] == [i for i in range(m.SIZE) if g0[i] != m.step(g0, 0, 'left')[i]]
        assert p['first_mask'] == [i for i in range(m.SIZE) if ctrl[i] != m.step(ctrl, 0, 'left')[i]]
        parent_meta.append({'parent_id':pid,'seed':list(pair),'attempt':p['control_match_attempt'],
                            'period':parent['period'],'union_support':p['union_support']})
        boundary = (min(parent['support']) - 1, max(parent['support']) + 1)
        for side, site in zip(('left', 'right'), boundary):
            assert g0[site] == ctrl[site] == 0
            for raw in range(1,16):
                arm_data = []
                early_data = []
                for initial in (g0, ctrl):
                    mutated = bytearray(initial)
                    mutated[site] = raw
                    result = extended_orbit(mutated, max_ticks)
                    arm_data.append({str(h):snapshot_at(result,h) for h in HORIZONS})
                    early_data.append(response_trace(initial, mutated))
                    arm_data[-1]['recurrence'] = result['first_recurrence']
                    arm_data[-1]['period'] = result['period']
                    arm_data[-1]['support'] = result['support']
                eq = {}
                jac = {}
                bitdelta = {}
                for tick in SAMPLE_TICKS:
                    a_mask,a_bits = early_data[0][tick]
                    b_mask,b_bits = early_data[1][tick]
                    eq[str(tick)] = a_mask == b_mask
                    union = (a_mask | b_mask).bit_count()
                    jac[str(tick)] = ((a_mask & b_mask).bit_count() / union) if union else 1.0
                    bitdelta[str(tick)] = a_bits - b_bits
                if 'probes' in p:
                    # Full 112 repository archive stores [class, period, support_hex] x2
                    idx = (0 if side == 'left' else 15) + raw - 1
                    expected = p['probes'][idx]
                    for arm, offset in zip(arm_data, (0, 3)):
                        observed_hex = (None if arm['500'] == 'censored' else
                            format(sum(1 << i for i in arm['support']), 'x'))
                        if (arm['500'], arm['period'] if arm['500'] != 'censored' else None,
                            observed_hex) != tuple(expected[offset:offset+3]):
                            raise AssertionError(f'Exp112 full record mismatch pid={pid} {side} raw={raw}')
                records.append({'parent_id':pid,'side':side,'raw':raw,
                                'a':arm_data[0],'b':arm_data[1],
                                'response_equal':eq,'response_jaccard':jac,
                                'response_bitcount_difference':bitdelta})
    summary = aggregate(records)
    # Reproduce the published Experiment 112 500-tick coarse outcome population.
    if max_parents is None:
        a = summary['horizons']['500']['aggregate']
        target = historical['summary']['all30']['aggregate']
        assert a['actual_censored'] == target['actual_censored']
        assert a['control_censored'] == target['control_censored']
        assert a['both_resolved'] == target['both_resolved']
        assert a['resolved_class_disagreement'] == target['class_disagreement']
        assert len(parent_meta) == 20 and len(records) == 600
    return {'experiment':114,'protocol': {
                'physical_kernel':'unchanged 104 phase0 left-rotate mutual modulation; SIZE60 CENTER30',
                'parent_cohort':'frozen 112 first-mask-matched 20 pairs',
                'injections':'same 30 (side,raw) probes per matched parent',
                'horizons':list(HORIZONS),'extended_horizon':max_ticks,
                'trace_times':list(SAMPLE_TICKS),
                'response':'position mask and Hamming bits of injected trajectory relative to its own same-phase noninjected trajectory',
                'recurrent_key':'full microstate + next scheduler phase',
                'censoring':'right censored if no exact recurrent key by horizon',
                'classification':'connected/fragmented/static only after recurrence; no daughter viability inference',
                'independence':'20 matched parent pairs; 600 paired probes are repeated measures',
                'null':'matched on-cycle controls from Experiment108, no new control tuning',
             },
             'reference':{'experiment':112,'matched_parents':len(parent_meta)},
             'parent_metadata':parent_meta,'summary':summary,'records':records}


def export(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, indent=2, sort_keys=True)+'\n', encoding='utf-8')


def write_csv(path, result):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    keys = ['parent_id','side','raw','G0_500','CTRL_500','G0_2000','CTRL_2000','G0_recurrence','CTRL_recurrence','G0_period_500','CTRL_period_500','G0_support_500','CTRL_support_500','G0_period_2000','CTRL_period_2000']
    keys += [f'mask_equal_t{t}' for t in SAMPLE_TICKS]
    keys += [f'jaccard_t{t}' for t in SAMPLE_TICKS]
    keys += [f'bitcount_diff_t{t}' for t in SAMPLE_TICKS]
    with Path(path).open('w', newline='', encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=keys,lineterminator="\n")
        writer.writeheader()
        for x in result['records']:
            row={'parent_id':x['parent_id'],'side':x['side'],'raw':x['raw'],
                 'G0_500':x['a']['500'],'CTRL_500':x['b']['500'],
                 'G0_2000':x['a']['2000'],'CTRL_2000':x['b']['2000'],
                 'G0_recurrence':x['a']['recurrence'],'CTRL_recurrence':x['b']['recurrence'],
                 'G0_period_500':x['a']['period'] if x['a']['500']!='censored' else None,
                 'CTRL_period_500':x['b']['period'] if x['b']['500']!='censored' else None,
                 'G0_support_500':format(sum(1<<i for i in x['a']['support']),'x') if x['a']['500']!='censored' else None,
                 'CTRL_support_500':format(sum(1<<i for i in x['b']['support']),'x') if x['b']['500']!='censored' else None,
                 'G0_period_2000':x['a']['period'],'CTRL_period_2000':x['b']['period']}
            row.update({f'mask_equal_t{t}':int(x['response_equal'][str(t)]) for t in SAMPLE_TICKS})
            row.update({f'jaccard_t{t}':f"{x['response_jaccard'][str(t)]:.8f}" for t in SAMPLE_TICKS})
            row.update({f'bitcount_diff_t{t}':x['response_bitcount_difference'][str(t)] for t in SAMPLE_TICKS})
            writer.writerow(row)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reference',type=Path,default=EXP/'112_probe_discrimination_audit/results/default.json')
    ap.add_argument('--output',type=Path,default=HERE/'results/default.json')
    ap.add_argument('--csv',type=Path,default=HERE/'results/probes.csv')
    ap.add_argument('--max-parents',type=int,default=None)
    args=ap.parse_args()
    if args.max_parents is not None and args.max_parents<1:
        ap.error('positive max-parents required')
    result=assay(args.reference,max_parents=args.max_parents)
    # Audit archive: compact per-probe records are CSV; summary JSON excludes duplicate entries.
    export(args.output,{k:v for k,v in result.items() if k!='records'})
    write_csv(args.csv,result)
    print(json.dumps(result['summary'],sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
