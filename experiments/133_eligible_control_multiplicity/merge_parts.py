#!/usr/bin/env python3
"""Merge disjoint exact-geometry candidate enumerations, no scientific postselection."""
from pathlib import Path
from collections import Counter
import json, argparse
HERE=Path(__file__).resolve().parent

def merge(parts):
    sources=[json.loads(Path(p).read_text()) for p in parts]
    ranges=[(x['contract']['catalog_start'],x['contract']['catalog_stop']) for x in sources]
    assert ranges==[(0,30),(30,60),(60,90),(90,130)]
    records=sum((x['parent_records'] for x in sources),[])
    assert [p['parent_id'] for p in records]==list(range(130))
    n=Counter(x['num_eligible_candidates'] for x in records)
    u=Counter(x['num_unique_phase0_microstates'] for x in records)
    assert sum(n.values())==130 and sum(x['num_eligible_candidates'] for x in records)==87
    summary={'parents_inspected':len(records), 'eligible_parents':sum(x['num_eligible_candidates']>0 for x in records),
        'parents_with_multiple_eligible':sum(x['num_eligible_candidates']>1 for x in records),
        'parents_with_multiple_distinct_controls':sum(x['num_unique_phase0_microstates']>1 for x in records),
        'total_accepted_candidates':sum(x['num_eligible_candidates'] for x in records),
        'accepted_histogram':dict(sorted(n.items())),'unique_state_histogram':dict(sorted(u.items()))}
    assert summary['eligible_parents']==55 and summary['parents_with_multiple_eligible']==22
    return {'experiment':133,'contract':{'parents':130,'attempts':100,
      'kernel':'frozen phase0 60-window left-rotation 104/108',
      'eligibility':'same period, exact cycle-union support positions, phase-zero occupancy and scheduler phase',
      'selection':'100 autonomous candidate attempts per G0; no future injected response used; original frozen first-choice verified'},
      'summary':summary,'parent_records':records}

def main():
    z=argparse.ArgumentParser();z.add_argument('--output',type=Path,default=HERE/'results/default.json');a=z.parse_args()
    p=[HERE/'results'/f'part{i}.json' for i in range(4)]
    out=merge(p);a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps(out['summary'],sort_keys=True,indent=2))
if __name__=='__main__':main()
