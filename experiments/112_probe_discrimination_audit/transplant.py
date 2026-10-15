#!/usr/bin/env python3
"""Experiment 112 secondary: fixed 30-probe local patch/null response transfer.

Patch/null eligibility is wholly independent of perturbation responses;
reference informative probes are taken only from the frozen 112 reference file.
Use the same first-mask constraint, 1..3 contiguous windows and 4 synthetic
matched nulls as Experiment 111. Nulls are drawn with replacement.
"""
import argparse
import importlib.util
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("exp112", HERE / "run.py")
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
e, m = r.e, r.m
WIDTHS=(1,2,3)


def score(frame, sites, keys, reference):
    confirmed = censored = 0
    for (side,raw) in keys:
        site=sites[0] if side=="left" else sites[1]
        label=r.observe(frame,site,raw)["class"]
        # Reference G0 is resolved on informative inputs by definition.
        target=reference[(side,raw)]["a"]["class"]
        confirmed += label==target
        censored += label=="censored"
    return confirmed, censored


def assay(reference, repeats=4, budget=256, attempts=100):
    if reference["parameters"]["attempts"]!=attempts or reference["parameters"]["ticks"]!=500:
        raise ValueError("Frozen references must be the 100-attempt, 500-tick default")
    if reference["inventory"]["G0_checked"]!=130:
        raise ValueError("Frozen reference must cover all G0 parents")
    ids={entry["parent_id"]:entry for entry in reference["parent_records"]}
    if len(ids)!=20:raise AssertionError("Reference first-mask cohort changed")
    orig=m.orbit
    def finite(*a,**kw):
        kw.setdefault("max_ticks",500)
        return orig(*a,**kw)
    m.orbit=finite
    inventory=Counter()
    patch_records=[]
    parent_records=[]
    try:
        for pid,(pair,donor,parent) in enumerate(m.parents("left")):
            match=e.v.matched_control(pid,donor,parent,attempts)
            if match is None:continue
            ctrl=match[0]
            mask=e.first_mask(donor)
            if e.first_mask(ctrl)!=mask:continue
            inventory["same_first_mask_pairs"]+=1
            pref=ids[pid]
            assert pref["seed"]==list(pair)
            assert pref["union_support"]==sorted(parent["support"])
            assert pref["control_match_attempt"]==match[2]
            assert pref["first_mask"]==sorted(mask)
            refmap={(p["side"],p["raw"]):p for p in pref["probes"]}
            informative=tuple(k for k,v in refmap.items() if v["class_disagreement"])
            sites=e.probe_sites(parent["support"])
            parent_records.append({"parent_id":pid,"seed":list(pair),
                                   "informative_probes":len(informative)})
            inventory["informative_parents"]+=bool(informative)
            for width in WIDTHS:
                candidates=e.changed_patches(donor,ctrl,parent["support"],width)
                inventory[f"width{width}_candidates"]+=len(candidates)
                for rank,patch in enumerate(candidates):
                    trans=e.replace(ctrl,donor,patch)
                    if e.first_mask(trans)!=mask:continue
                    inventory[f"width{width}_donor_mask_pass"]+=1
                    nulls,tried=e.null_replacements(ctrl,patch,mask,pid,rank,width,repeats,budget)
                    inventory[f"width{width}_null_proposals"]+=tried
                    if len(nulls)!=repeats:
                        inventory[f"width{width}_null_shortages"]+=1
                        continue
                    inventory[f"width{width}_matched_patches"]+=1
                    # All eligibility checks precede use of the injected response.
                    donor_counts=score(trans,sites,informative,refmap)
                    null_counts=[score(fake,sites,informative,refmap) for fake in nulls]
                    patch_records.append({"parent_id":pid,"width":width,
                        "patch":list(patch),"informative_probes":len(informative),
                        "donor_confirmed":donor_counts[0],"donor_censored":donor_counts[1],
                        "null_confirmed":[x[0] for x in null_counts],
                        "null_censored":[x[1] for x in null_counts]})
    finally:
        m.orbit=orig
    summaries={}
    for width in WIDTHS:
        rows=[p for p in patch_records if p["width"]==width]
        group=defaultdict(list)
        for p in rows:group[p["parent_id"]].append(p)
        eligible={pid:items for pid,items in group.items() if items[0]["informative_probes"]>0}
        diff=[];av=[];bv=[]
        for pid,items in eligible.items():
            a=statistics.mean(item["donor_confirmed"]/item["informative_probes"] for item in items)
            b=statistics.mean(statistics.mean(item["null_confirmed"])/item["informative_probes"] for item in items)
            av.append(a);bv.append(b);diff.append(a-b)
        summaries[str(width)]={
            "matched_patches":len(rows),"parents_with_matched_patches":len(group),
            "informative_parents_with_matched_patches":len(eligible),
            "reference_informative_probe_total_in_evaluable_parents":sum(items[0]["informative_probes"] for items in eligible.values()),
            "donor_parent_mean_confirmed_fraction":statistics.mean(av) if av else None,
            "null_parent_mean_confirmed_fraction":statistics.mean(bv) if bv else None,
            "parent_mean_difference":statistics.mean(diff) if diff else None,
            "parent_wins":sum(x>0 for x in diff),"parent_losses":sum(x<0 for x in diff),
            "parent_ties":sum(x==0 for x in diff),
            "donor_censored_probes":sum(p["donor_censored"] for p in rows),
            "null_censored_probes":sum(sum(p["null_censored"]) for p in rows),
        }
    return {"experiment":112,"part":"exploratory 30-probe response transfer",
            "parameters":{"null_repeats":repeats,"null_proposal_budget":budget,
                "matching_attempts":attempts,"ticks":500,"widths":list(WIDTHS),
                "panel":"predeclared all 15 nonzero values x two boundaries",
                "null":"same sites and first-tick changed mask (with replacement)"},
            "inventory":dict(sorted(inventory.items())),"summary":summaries,
            "parent_records":parent_records,"patch_records":patch_records}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--reference",type=Path,default=HERE/"results"/"default.json")
    ap.add_argument("--output",type=Path,default=None)
    ap.add_argument("--null-repeats",type=int,default=4)
    ap.add_argument("--null-budget",type=int,default=256)
    args=ap.parse_args()
    if args.null_repeats<1 or args.null_budget<1:ap.error("positive null repeats and budget required")
    frozen=r.decode_archive(json.loads(args.reference.read_text(encoding="utf-8")))
    result=assay(frozen,args.null_repeats,args.null_budget)
    if args.output is not None:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ("parameters","inventory","summary")},indent=2,sort_keys=True))

if __name__=="__main__":main()
