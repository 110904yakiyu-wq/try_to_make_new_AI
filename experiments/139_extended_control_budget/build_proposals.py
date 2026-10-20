"""Generate original exact CPython random candidate states, one per attempt.
Binary record: parent_id:uint8, attempt:uint16 little endian, period:uint8,
frame[60], cycle_support_mask[60], candidate[60]. No response probes.
"""
import argparse,struct
from pathlib import Path
import core
HERE=Path(__file__).resolve().parent

def generate(limit=1000, output=HERE/'results/proposals.bin'):
    ps=list(core.parents());assert len(ps)==130
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    with open(output,'wb') as f:
        for pid,(_,frame,parent) in enumerate(ps):
            mask=bytes(int(i in parent['support']) for i in range(60))
            assert parent['period']<256
            for i in range(limit):
                candidate=core.proposal(pid,frame,i)
                f.write(struct.pack('<BHB',pid,i+1,parent['period'])+frame+mask+candidate)
    return len(ps)*limit
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--attempts',type=int,default=1000)
    p.add_argument('--output',type=Path,default=HERE/'results/proposals.bin');a=p.parse_args()
    print('generated=',generate(a.attempts,a.output))
