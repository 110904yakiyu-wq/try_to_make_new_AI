// Experiment 139: exact deterministic reproduction of original 104/108 orbit
// on pre-generated CPython Random candidates. All eligibility decisions are
// autonomous and do not inspect injected material or its outcomes.
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <unordered_map>
#include <vector>
using Frame = std::array<unsigned char,60>;
struct State { Frame f; uint8_t phase; bool operator==(const State&b) const {return phase==b.phase&&f==b.f;} };
struct Hasher {
 size_t operator()(const State&s) const {
   uint64_t h=1469598103934665603ULL;
   for(auto z:s.f){h^=z;h*=1099511628211ULL;}
   h^=s.phase;h*=1099511628211ULL;return size_t(h);
 }
};
static inline uint8_t rot(uint8_t z){return uint8_t(((z<<1)&15)|(z>>3));}
static inline Frame step(const Frame&x,int phase){
 Frame out=x;
 for(int j=0;j<20;j++){
  int i=(phase+3*j)%60, k=(i+1)%60, l=(i+2)%60;
  const uint8_t a=x[i],b=x[k],c=x[l];
  out[i]=a^rot(b&c);out[k]=b^rot(a&c);out[l]=c^rot(a&b);
 }
 return out;
}
struct Result {int gate; Frame control; int period;};
Result orbit_match(Frame x,const Frame&donor,int period,const Frame&supportMask){
 std::vector<Frame> frames;frames.reserve(501);frames.push_back(x);
 std::unordered_map<State,int,Hasher> seen;seen.reserve(650);seen.emplace(State{x,0},0);
 for(int tick=1;tick<=500;tick++){
  x=step(x,(tick-1)%3);
  State state{x,static_cast<uint8_t>(tick%3)};
  auto itr=seen.find(state);
  if(itr!=seen.end()){
    int begin=itr->second,per=tick-begin;
    Frame mask{};bool active=false;
    for(int j=begin;j<tick;j++){
      for(int k=0;k<60;k++)if(frames[j][k])mask[k]=1;
      if(frames[j]!=frames[begin])active=true;
    }
    if(!active)return {1,{},per};
    if(per!=period)return {2,{},per};
    if(mask!=supportMask)return {3,{},per};
    // Exact historical phase-zero maximum occupancy tie-break: first in orbit order.
    Frame best{};int count=-1;
    for(int j=begin;j<tick;j++){
       if(j%3!=0)continue;
       int score=0;for(auto z:frames[j])score+=bool(z);
       if(score>count){count=score;best=frames[j];}
    }
    if(count<0)return {4,{},per};
    for(int k=0;k<60;k++)if(bool(best[k])!=bool(donor[k]))return {4,{},per};
    return {5,best,per};
  }
  seen.emplace(std::move(state),tick);frames.push_back(x);
 }
 return {0,{},0};
}
int main(int argc,char**argv){
 if(argc!=3){std::cerr<<"usage: sweep proposal.bin accepted.csv\n";return 2;}
 std::ifstream in(argv[1],std::ios::binary);std::ofstream out(argv[2]);
 if(!in||!out)return 2;
 out<<"parent_id,attempt,gate\n";
 int entries=0,accepted=0;
 while(true){
  uint8_t h[4];in.read(reinterpret_cast<char*>(h),4);
  if(!in){if(in.eof())break;return 3;}
  int pid=h[0], attempt=int(h[1])|(int(h[2])<<8), period=h[3];
  // The period for historical G0 set is <= 168.
  Frame donor{},sup{},candidate{};
  in.read(reinterpret_cast<char*>(donor.data()),60);
  in.read(reinterpret_cast<char*>(sup.data()),60);
  in.read(reinterpret_cast<char*>(candidate.data()),60);
  if(!in)return 3;
  auto a=orbit_match(candidate,donor,period,sup);entries++;
  if(a.gate==5)accepted++;
  out<<pid<<","<<attempt<<","<<a.gate<<"\n";
 }
 std::cerr<<"proposals="<<entries<<" accepted="<<accepted<<"\n";
 if(entries!=130000||accepted!=970)return 4;
}
