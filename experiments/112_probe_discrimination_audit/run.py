#!/usr/bin/env python3
"""Experiment 112: predeclared 30-probe identification audit.

Pure measurement extension of Experiment 111, using its frozen 108 matching,
local kernel and first-tick changed-position-mask eligibility. No outcome-based
candidate selection; raw probes are all 1..15 at each of two support boundaries.
"""
import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "111_conditional_local_bit_swap" / "run.py"
spec = importlib.util.spec_from_file_location("exp111", SOURCE)
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)
m = e.m
RAW_VALUES = tuple(range(1,16))
LEGACY = (1,7,15)


def observe(frame, pos, raw):
    assert frame[pos] == 0
    perturbed = bytearray(frame)
    perturbed[pos] = raw
    orbit = m.orbit(bytes(perturbed), phase=0, direction="left")
    if orbit["status"] != "cycle":
        return {"class": "censored", "period": None, "support": None}
    if not orbit["active"]:
        label = "static"
    elif len(e.components(orbit["support"])) == 1:
        label = "connected"
    else:
        label = "fragmented"
    return {"class": label, "period": orbit["period"],
            "support": sorted(orbit["support"])}


def summarize_pair(actual, control, positions):
    rows = []
    for side, pos in zip(("left", "right"), positions):
        for raw in RAW_VALUES:
            a, b = actual[(side, raw)], control[(side, raw)]
            resolved = a["class"] != "censored" and b["class"] != "censored"
            different = resolved and a["class"] != b["class"]
            rows.append({"side": side, "raw": raw, "a": a, "b": b,
                         "both_resolved": resolved, "class_disagreement": different,
                         "resolved_period_disagreement": resolved and a["period"] != b["period"],
                         "resolved_support_disagreement": resolved and a["support"] != b["support"]})
    assert len(rows)==30
    return rows


def analyze_records(records):
    out = {}
    for name, f in (("six", lambda x:x["raw"] in LEGACY),
                    ("all30", lambda x:True)):
        agg = Counter()
        parents_with_any = Counter()
        for parent in records:
            sub = [r for r in parent["probes"] if f(r)]
            assert len(sub) == (6 if name=="six" else 30)
            cs = Counter()
            for r in sub:
                a,b = r["a"], r["b"]
                cs["both_resolved"] += r["both_resolved"]
                cs["class_disagreement"] += r["class_disagreement"]
                cs["resolved_period_disagreement"] += r["resolved_period_disagreement"]
                cs["resolved_support_disagreement"] += r["resolved_support_disagreement"]
                cs["at_least_one_censored"] += not r["both_resolved"]
                cs["both_censored"] += a["class"]=="censored" and b["class"]=="censored"
                cs["actual_connected"] += a["class"]=="connected"
                cs["control_connected"] += b["class"]=="connected"
                cs["actual_censored"] += a["class"]=="censored"
                cs["control_censored"] += b["class"]=="censored"
                cs["both_connected"] += a["class"]=="connected" and b["class"]=="connected"
            agg.update(cs)
            for key in ("class_disagreement", "resolved_period_disagreement",
                        "resolved_support_disagreement", "both_resolved"):
                parents_with_any[key] += cs[key]>0
        out[name] = {"probe_pair_rows":len(records)*(6 if name=="six" else 30),
                     "aggregate":dict(sorted(agg.items())),
                     "parents_with_any":dict(sorted(parents_with_any.items()))}
    out["comparison"]={"additional_class_informative_parents":
                       out["all30"]["parents_with_any"].get("class_disagreement",0)-
                       out["six"]["parents_with_any"].get("class_disagreement",0)}
    return out


def assay(attempts=100, ticks=500, max_parents=None):
    original = m.orbit
    def bounded(*args, **kw):
        kw.setdefault("max_ticks",ticks)
        return original(*args, **kw)
    m.orbit=bounded
    recs=[]
    inventory=Counter()
    try:
        for idx,(pair,donor,parent) in enumerate(m.parents("left")):
            if max_parents is not None and idx>=max_parents:break
            inventory["G0_checked"] += 1
            match=e.v.matched_control(idx,donor,parent,attempts)
            if match is None:continue
            inventory["exact108_pairs"] += 1
            ctrl,control_orbit,nth=match
            if e.first_mask(donor) != e.first_mask(ctrl):continue
            inventory["equal_first_mask_pairs"] += 1
            sites=e.probe_sites(parent["support"])
            obs=[]
            for frame in (donor,ctrl):
                item={}
                for side, pos in zip(("left","right"),sites):
                    for raw in RAW_VALUES:
                        item[(side,raw)]=observe(frame,pos,raw)
                obs.append(item)
            probes=summarize_pair(*obs,sites)
            recs.append({"parent_id":idx,"seed":list(pair),"control_match_attempt":nth,
                         "union_support":sorted(parent["support"]),
                         "first_mask":sorted(e.first_mask(donor)),"probes":probes})
    finally:
        m.orbit=original
    summary=analyze_records(recs)
    inventory["nonmatching108_pairs"]=inventory["G0_checked"]-inventory["exact108_pairs"]
    inventory["mask_different108_pairs"]=inventory["exact108_pairs"]-inventory["equal_first_mask_pairs"]
    return {"experiment":112,"purpose":"predeclared probe discrimination (not causal transfer)",
            "parameters":{"attempts":attempts,"ticks":ticks,"max_parents":max_parents,
                          "scheduler_phase":0,"direction":"left","center":m.CENTER,
                          "probes_per_side":list(RAW_VALUES),"legacy_probes_per_side":list(LEGACY),
                          "selection":"preintervention 108 exact match + same unperturbed first-tick mask"},
            "inventory":dict(sorted(inventory.items())),"summary":summary,"parent_records":recs}


def encode_archive(result):
    """Losslessly pack per-probe observable labels, periods, support sets.

    Ordering is left raw=1..15, then right raw=1..15.
    Each entry contains [G0 class, G0 period, G0 union-support bitset hex,
                         control class, control period, control support hex].
    All absent period/support values are JSON null (censored trajectory).
    """
    out={k:v for k,v in result.items() if k!="parent_records"}
    out["encoding"]="30 probes ordered left 1..15 then right 1..15; 6 fields per probe: G0 class,period,support_hex,control class,period,support_hex"
    out["parent_records"]=[]
    for parent in result["parent_records"]:
        rec={k:v for k,v in parent.items() if k!="probes"}
        rec["probes"]=[]
        for q in parent["probes"]:
            vals=[]
            for side in ("a","b"):
                a=q[side]
                sup=None if a["support"] is None else format(sum(1<<i for i in a["support"]), "x")
                vals.extend([a["class"],a["period"],sup])
            rec["probes"].append(vals)
        out["parent_records"].append(rec)
    return out


def decode_archive(packed):
    if packed.get("experiment")!=112 or "encoding" not in packed:
        raise ValueError("Not a compressed Exp112 reference archive")
    out={k:v for k,v in packed.items() if k not in ("parent_records","encoding")}
    out["parent_records"]=[]
    for parent in packed["parent_records"]:
        rec={k:v for k,v in parent.items() if k!="probes"}
        rows=[]
        if len(parent["probes"])!=30:raise AssertionError("30 expected probes")
        for idx,entry in enumerate(parent["probes"]):
            if len(entry)!=6:raise AssertionError("6 fields expected")
            decoded=[]
            for j in (0,3):
                label,period,hex_support=entry[j:j+3]
                support=None if hex_support is None else [k for k in range(m.SIZE) if int(hex_support,16)>>k & 1]
                decoded.append({"class":label,"period":period,"support":support})
            a,b=decoded
            resolved=a["class"]!="censored" and b["class"]!="censored"
            rows.append({"side":"left" if idx<15 else "right", "raw":idx%15+1,
                         "a":a,"b":b,"both_resolved":resolved,
                         "class_disagreement":resolved and a["class"]!=b["class"],
                         "resolved_period_disagreement":resolved and a["period"]!=b["period"],
                         "resolved_support_disagreement":resolved and a["support"]!=b["support"]})
        rec["probes"]=rows
        out["parent_records"].append(rec)
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--attempts",type=int,default=100)
    p.add_argument("--max-ticks",type=int,default=500)
    p.add_argument("--max-parents",type=int,default=None)
    p.add_argument("--output",type=Path,default=None)
    args=p.parse_args()
    if args.attempts<1 or args.max_ticks<1 or args.max_parents is not None and args.max_parents<1:
        p.error("all numerical controls must be positive")
    result=assay(args.attempts,args.max_ticks,args.max_parents)
    if args.output is not None:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(encode_archive(result),ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ("parameters","inventory","summary")},indent=2,sort_keys=True))

if __name__=="__main__":main()
