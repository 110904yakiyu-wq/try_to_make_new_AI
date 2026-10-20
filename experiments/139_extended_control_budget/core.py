"""Exact frozen 104/108 local kernel, exposed for independent regression audits."""
import random
from functools import lru_cache
SIZE=60
CENTER=30
@lru_cache(None)
def blocks(n,p):
    return tuple(tuple((p+3*j+k)%n for k in range(3)) for j in range(n//3))
def rotate(x):return ((x<<1)&15)|(x>>3)
def step(s,p):
    o=bytearray(s)
    for i,j,k in blocks(len(s),p):
        x,y,z=s[i],s[j],s[k]
        o[i]=x^rotate(y&z);o[j]=y^rotate(x&z);o[k]=z^rotate(x&y)
    return bytes(o)
def orbit(s,phase=0,max_ticks=500):
    s=bytes(s);seen={(s,phase):0};frames=[s]
    for t in range(1,max_ticks+1):
        s=step(s,(phase+t-1)%3);key=(s,(phase+t)%3)
        if key in seen:
            begin=seen[key];cycle=frames[begin:t]
            sup={i for fr in cycle for i,x in enumerate(fr) if x}
            return {'status':'cycle','cycle':cycle,'phase':(phase+begin)%3,
                    'period':t-begin,'support':sup,'active':len(set(cycle))>1,
                    'first_recurrence':t}
        seen[key]=t;frames.append(s)
    return {'status':'timeout'}
def parents():
    for a in range(1,16):
        for b in range(1,16):
            s=bytearray(SIZE);s[CENTER]=a;s[CENTER+1]=b
            r=orbit(s,max_ticks=2500)
            if r['status']!='cycle' or not r['active'] or len(r['support'])>13: continue
            ph0=[f for j,f in enumerate(r['cycle']) if (r['phase']+j)%3==0]
            yield (a,b),max(ph0,key=lambda f:sum(bool(x) for x in f)),r

def proposal(pid,frame,zero_based_attempt):
    rng=random.Random(3_000_000+pid*300_000+zero_based_attempt)
    return bytes(rng.randrange(1,16) if x else 0 for x in frame)

def qualifying_control(pid,frame,parent,attempt0,horizon=500):
    o=orbit(proposal(pid,frame,attempt0),max_ticks=horizon)
    if o['status']!='cycle' or not o['active'] or o['period']!=parent['period'] or o['support']!=parent['support']:return None
    ph0=[fr for j,fr in enumerate(o['cycle']) if (o['phase']+j)%3==0]
    ctrl=max(ph0,key=lambda x:sum(bool(z) for z in x))
    if any(bool(a)!=bool(b) for a,b in zip(ctrl,frame)):return None
    return ctrl
