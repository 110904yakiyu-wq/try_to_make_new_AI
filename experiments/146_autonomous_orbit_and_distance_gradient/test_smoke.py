#!/usr/bin/env python3
"""Regenerate orbit identity and within-distance response variation invariants."""
import json
from pathlib import Path
import run
HERE=Path(__file__).resolve().parent

def main():
 x=run.assay()
 assert x==json.loads((HERE/'results/default.json').read_text())
 s=x['summary']
 assert (s['parents'],s['eligible_controls'],s['exact_microstate_controls'],s['same_autonomous_orbit_controls'])==(113,970,1,1)
 assert s['parents_with_multiple_raw_distances']==111
 assert s['within_parent_same_distance_groups']==231
 assert s['within_parent_same_distance_differing_yes10']==198
 assert s['within_parent_same_distance_differing_yes60']==199
 assert (s['near_tie_break_changes_control'],s['far_tie_break_changes_control'])==(6,2)
 assert (s['spread10']['near_control_yes'],s['spread10']['near_with_window_tie_yes'])==(663,615)
 assert (s['spread60']['near_control_yes'],s['spread60']['near_with_window_tie_yes'])==(518,476)
 assert {p['parent_id'] for p in x['parent_records'] if p['identical_G0_controls']}=={22}
 assert sum(p['controls'] for p in x['parent_records'])==970
 print('exp146 smoke PASS (autonomous cycle identity, same-distance outcome variation)')
if __name__=='__main__':main()
