#!/usr/bin/env python3
"""Reconstruct frozen 125/126 matched parent cohort; write binary microstates.
Uses exact kernel and matching RNG constants from 104/108, with frozen
accepted-attempt manifest from 126. Does NOT select by any probe outcomes.
"""
import json,random,struct,sys
from pathlib import Path
from functools import lru_cache
SIZE=60; CENTER=30
assert CENTER%3==0
@lru_cache(None)
def blocks(n,p):return tuple(tuple((p+3*j+k)%n for k in range(3)) for j in range(n//3))
def rotate(x):return ((x<<1)&15)|(x>>3)
def step(s,p):
 o=bytearray(s)
 for i,j,k in blocks(len(s),p):
  x,y,z=s[i],s[j],s[k]
  o[i]=x^rotate(y&z);o[j]=y^rotate(x&z);o[k]=z^rotate(x&y)
 return bytes(o)
def orbit(s,phase=0,max_ticks=2500):
 s=bytes(s);seen={(s,phase):0};frames=[s]
 for t in range(1,max_ticks+1):
  s=step(s,(phase+t-1)%3);key=(s,(phase+t)%3)
  if key in seen:
   begin=seen[key];cycle=frames[begin:t]
   support={i for f in cycle for i,x in enumerate(f) if x}
   return {'status':'cycle','cycle':cycle,'phase':(phase+begin)%3,'period':t-begin,'support':support,'active':len(set(cycle))>1}
  seen[key]=t;frames.append(s)
 return {'status':'timeout'}
def parents():
 for a in range(1,16):
  for b in range(1,16):
   s=bytearray(SIZE);s[CENTER]=a;s[CENTER+1]=b
   r=orbit(s)
   if r['status']!='cycle' or not r['active'] or len(r['support'])>13:continue
   ph0=[f for j,f in enumerate(r['cycle']) if (r['phase']+j)%3==0]
   yield ((a,b),max(ph0,key=lambda f:sum(bool(x) for x in f)),r)
def control(pid,frame,parent,attempt):
 rng=random.Random(3_000_000+pid*300_000+attempt-1)
 c=bytes(rng.randrange(1,16) if x else 0 for x in frame)
 r=orbit(c)
 assert r['status']=='cycle' and r['active'] and r['period']==parent['period'] and r['support']==parent['support']
 ph0=[f for j,f in enumerate(r['cycle']) if (r['phase']+j)%3==0]
 result=max(ph0,key=lambda f:sum(bool(x) for x in f))
 assert all(bool(a)==bool(b) for a,b in zip(frame,result))
 return result
# Frozen from Exp126 verified parent metadata: (catalog index, seedA, seedB, match accepted attempt)
MANIFEST=[(2,1,5,85),(4,1,9,47),(5,1,11,61),(6,1,13,12),(8,2,2,13),(9,2,3,20),(11,2,7,96),(12,2,10,51),(13,2,11,49),(17,3,2,38),(19,3,6,91),(22,3,10,5),(23,3,13,4),(24,4,4,23),(25,4,5,30),(26,4,6,16),(28,4,12,15),(29,4,13,12),(32,5,1,55),(33,5,3,39),(34,5,4,9),(35,5,5,6),(36,5,6,2),(37,5,7,83),(38,5,9,30),(39,5,11,8),(42,5,14,35),(45,6,3,58),(46,6,4,79),(48,6,10,67),(49,6,11,24),(52,7,1,41),(59,7,12,29),(61,8,8,58),(62,8,9,52),(63,8,10,61),(66,8,13,75),(73,9,10,30),(75,9,12,54),(76,9,14,26),(77,10,2,27),(79,10,6,19),(80,10,7,87),(85,10,12,26),(86,10,13,9),(90,11,2,7),(91,11,5,83),(92,11,6,70),(99,12,5,1),(102,12,8,32),(104,12,10,74),(106,13,1,51),(108,13,4,33),(111,13,10,27),(126,15,4,5)]
def main():
 cat=list(parents());assert len(cat)==130,len(cat)
 out=Path(__file__).with_name('states.bin')
 with out.open('wb') as f:
  for pid,a,b,attempt in MANIFEST:
   seed,fr,p=cat[pid];assert seed==(a,b)
   c=control(pid,fr,p,attempt)
   lo=min(p['support'])-1;hi=max(p['support'])+1
   assert 0<=lo<hi<SIZE and fr[lo]==fr[hi]==c[lo]==c[hi]==0
   f.write(struct.pack('<BBBB',pid,attempt,lo,hi));f.write(fr);f.write(c)
 print(f'G0={len(cat)} matched={len(MANIFEST)} bytes={out.stat().st_size}')
if __name__=='__main__':main()
