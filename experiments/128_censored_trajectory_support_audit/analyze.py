#!/usr/bin/env python3
"""Descriptive support geometry for still-right-censored Experiment127 traces."""
import csv,json,collections,statistics,argparse
from pathlib import Path
R=Path(__file__).parent

def summarize(rows):
 result={}
 for arm,label in [(0,'G0'),(1,'control')]:
  data=[r for r in rows if r['arm']==arm]
  result[label]={
   'records':len(data),
   'full_ring_union_500':sum(x['union_500']==60 for x in data),
   'full_ring_union_2000':sum(x['union_2000']==60 for x in data),
   'full_ring_union_10000':sum(x['union_10000']==60 for x in data),
   'full_ring_union_50000':sum(x['union_50000']==60 for x in data),
   'ever_30_simultaneously_active':sum(x['max_simultaneous_active']>=30 for x in data),
   'mean_occupied_windows_over_50000':statistics.mean(x['total_active_site_ticks']/50000 for x in data),
   'median_first_full_union_tick':statistics.median(x['first_union60'] for x in data if x['first_union60']>=0),
   'nonfull_cases':[{'parent_id':x['parent_id'],'side':x['side'],'raw':x['raw'],'union_50000':x['union_50000'],'first_union60':x['first_union60']} for x in data if x['union_50000']!=60],
   'parents_with_censored_cases':len(set(x['parent_id'] for x in data)),
  }
 result['overall']={'records':len(rows),'full_ring_union_500':sum(x['union_500']==60 for x in rows),
        'full_ring_union_50000':sum(x['union_50000']==60 for x in rows),
        'parents_with_censored_cases':len(set(x['parent_id'] for x in rows)),
        'censored_unique_physical_states':528}
 assert result['G0']['records']==143 and result['control']['records']==394
 assert result['G0']['full_ring_union_50000']==143 and result['control']['full_ring_union_50000']==393
 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--csv',type=Path,default=R/'results/censored_trace.csv');ap.add_argument('--output',type=Path,default=R/'results/default.json');z=ap.parse_args()
 with open(z.csv,newline='')as f:rows=[{k:int(v)for k,v in r.items()}for r in csv.DictReader(f)]
 assert len(rows)==537
 summary=summarize(rows)
 payload={'experiment':128,'reference':'Exp127 55 matched parents, 50k right-censored subset only',
 'protocol':{'horizon':50000,'physical_step':'identical 104 three-phase local kernel',
 'geometric_observer':'historical nonzero 4-bit window union (does not imply simultaneous occupancy)',
 'eligibility':'only Exp127 exact phase-key recurrent status censored at 50000',
 'independence':'parent clusters; repeated probes not independent',
 'interpretation':'full-ring visit within finite horizon, not proof of eventual stationary behavior'},
 'summary':summary,'probe_records':rows}
 z.output.write_text(json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=='__main__':main()
