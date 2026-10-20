"""Exp140 censor-aware physical spread, frozen first acceptable controls by 1000.
Validation includes exact legacy Exp130 row-level replication, not a new dataset.
"""
import argparse,csv,json,statistics,sys
from collections import Counter,defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'139_extended_control_budget'))
import core
REF=HERE.parent/'130_spread_threshold_robustness/results/probes.csv'

def read(path):
    with open(path,newline='',encoding='utf-8') as f:
        return [{k:int(v) for k,v in r.items()} for r in csv.DictReader(f)]

def status(row,k):
    if row[f'first{k}']>=0:return 'yes'
    if row['recurrence']>=0:return 'certified_no'
    return 'unknown'

def counter(rows,k,arm):return Counter(status(r,k) for r in rows if r['arm']==arm)
def calc(rows,k):
    a,b=counter(rows,k,0),counter(rows,k,1);n=sum(a.values());assert n==sum(b.values())
    return {'n_per_arm':n,'G0':dict(a),'control':dict(b),
            'lower_delta':a['yes']-b['yes']-b['unknown'],
            'upper_delta':a['yes']+a['unknown']-b['yes'],
            'lower_rate':(a['yes']-b['yes']-b['unknown'])/n,
            'upper_rate':(a['yes']+a['unknown']-b['yes'])/n}

def assay(probes,reference):
    rows=read(probes); ref=read(reference)
    assert len(rows)==6780 and len(ref)==3300
    ix={(r['parent_id'],r['arm'],r['side'],r['raw']):r for r in rows}
    assert len(ix)==6780
    oldids={r['parent_id'] for r in ref}
    for r in ref:
        k=(r['parent_id'],r['arm'],r['side'],r['raw']);q=ix[k]
        for key in ('first10','first60'):
            assert r[key]==q[key],('historical mismatch',k,key)
        if r['first60']<0:assert r['recurrence']==q['recurrence'],('historical recurrence mismatch',k)
    parents={r['parent_id'] for r in rows}
    assert len(oldids)==55 and len(parents)==113 and len(parents-oldids)==58
    strata={'old55':oldids,'new58':parents-oldids,'all113':parents}
    result={'experiment':140,'contract':{'kernel':'unchanged Exp104/108/134 three-phase mutual modulation',
       'control':'first autonomous candidate satisfying matching within 1000, prior to injected outcome',
       'probe':'left/right support boundary * 15 raw values, 30 per parent',
       'horizon':50000,'event':'ever reaches 10 or 60 distinct window positions; recurrence certifies non-reaching',
       'uncertainty':'no recurrence and no event by horizon -> right censored',
       'independence':'113 parent clusters, 30 dependent probe measurements each'},
       'reference_integrity':{'old55_probe_rows_reproduced':3300,'exact_first10_first60':True,
           'exact_recurrence_on_60_nonhits':True},'summary':{},'parent_records':[]}
    parent_list=list(core.parents())
    for name,ids in strata.items():
        selected=[r for r in rows if r['parent_id'] in ids]
        assert len(selected)==60*len(ids)
        result['summary'][name]={'parents':len(ids),'spread10':calc(selected,10),'spread60':calc(selected,60)}
        for th in (10,60):
            signs=Counter()
            for pid in ids:
                r=calc([x for x in selected if x['parent_id']==pid],th)
                signs['G0_less_guaranteed']+=r['upper_delta']<0
                signs['G0_greater_guaranteed']+=r['lower_delta']>0
                signs['sign_undecided_or_tied']+=not(r['upper_delta']<0 or r['lower_delta']>0)
            result['summary'][name][f'parent_signs_{th}']=dict(signs)
    for pid in sorted(parents):
        sub=[r for r in rows if r['parent_id']==pid]
        result['parent_records'].append({'parent_id':pid,'seed':list(parent_list[pid][0]),
           'period':parent_list[pid][2]['period'],'subset':'old55' if pid in oldids else 'new58',
           'selected_attempt':sub[0]['attempt'],'spread10':calc(sub,10),'spread60':calc(sub,60)})
    assert result['summary']['old55']['spread10']['G0']['yes']==173
    assert result['summary']['old55']['spread10']['control']['yes']==453
    assert result['summary']['new58']['spread10']['G0']['yes']==153
    assert result['summary']['new58']['spread10']['control']['yes']==312
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--reference',type=Path,default=REF)
    p.add_argument('--probes',type=Path,default=HERE/'results/probes.csv');z=p.parse_args()
    d=assay(z.probes,z.reference)
    (HERE/'results/default.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    (HERE/'results/default.txt').write_text(json.dumps(d['summary'],indent=2,sort_keys=True)+'\n')
    print(json.dumps(d['summary'],indent=2,sort_keys=True))
