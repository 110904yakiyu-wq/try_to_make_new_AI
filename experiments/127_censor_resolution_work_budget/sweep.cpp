// Experiment 127: exact finite-state phase-key recurrence, optimized CPU runner.
// Physics copied literally from experiments/104_single_window_fission_audit/run.py.
// This program is a computational backend, not a new physical model.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
#include <cassert>
#include <algorithm>
using State=std::array<uint8_t,60>;
struct Key {State s;uint8_t phase;bool operator==(Key const& o)const{return phase==o.phase&&s==o.s;}};
struct Hash {size_t operator()(Key const& k)const noexcept{
  uint64_t h=1469598103934665603ull;
  for(auto b:k.s){h^=b;h*=1099511628211ull;}
  h^=k.phase;h*=1099511628211ull;return size_t(h);
}};
inline uint8_t rot(uint8_t x){return uint8_t(((x<<1)&15)|(x>>3));}
inline State step(State const& s,int p){
 State o=s;
 for(int j=0;j<20;j++){
   int a=(p+3*j)%60,b=(a+1)%60,c=(a+2)%60;
   uint8_t x=s[a],y=s[b],z=s[c];
   o[a]=x^rot(y&z);o[b]=y^rot(x&z);o[c]=z^rot(x&y);
 }
 return o;
}
struct Result{int recurrence;int period;int cls;}; // -1 censored, 0 static,1 connected,2 fragmented
Result orbit(State const& start,int H){
 std::unordered_map<Key,int,Hash> seen;seen.reserve(H*2+1);
 std::vector<State> frames;frames.reserve(H+1);
 State s=start;seen.emplace(Key{s,0},0);frames.push_back(s);
 for(int tick=1;tick<=H;tick++){
   s=step(s,(tick-1)%3);Key k{s,uint8_t(tick%3)};
   auto it=seen.find(k);
   if(it!=seen.end()){
     int begin=it->second;
     std::array<bool,60> support{};
     bool active=false;
     for(int i=begin;i<tick;i++){
       for(int j=0;j<60;j++)if(frames[i][j])support[j]=true;
       if(frames[i]!=frames[begin])active=true;
     }
     if(!active)return {tick,tick-begin,0};
     int components=0;
     for(int j=0;j<60;j++)if(support[j]&&!support[(j+59)%60])components++;
     if(components==0 && support[0])components=1; // full ring
     assert(components>0);
     return {tick,tick-begin,components==1?1:2};
   }
   seen.emplace(k,tick);frames.push_back(s);
 }
 return {-1,-1,-1};
}
int main(int argc,char** argv){
 if(argc!=4){std::cerr<<"usage sweep states.bin output.csv max_horizon\n";return 2;}
 int H=std::stoi(argv[3]);if(H<2000||H>50000)return 2;
 std::ifstream in(argv[1],std::ios::binary);if(!in){std::cerr<<"no states.bin\n";return 2;}
 std::ofstream out(argv[2]);out<<"pid,arm,side,raw,recurrence,period,class,cache_hit\n";
 std::unordered_map<Key,Result,Hash> memo;
 int nparents=0,total=0;
 while(true){
   uint8_t meta[4];in.read(reinterpret_cast<char*>(meta),4);
   if(in.gcount()==0)break;
   assert(in.gcount()==4);
   State frames[2];for(auto &fr:frames){in.read(reinterpret_cast<char*>(fr.data()),60);assert(in.gcount()==60);}
   int pid=meta[0],lo=meta[2],hi=meta[3];nparents++;
   for(int a=0;a<2;a++)for(int side=0;side<2;side++)for(int raw=1;raw<16;raw++){
     State injected=frames[a];int pos=side==0?lo:hi;assert(injected[pos]==0);
     injected[pos]=uint8_t(raw);
     Key k{injected,0};auto it=memo.find(k);bool cached=it!=memo.end();
     Result res;
     if(cached)res=it->second;
     else{res=orbit(injected,H);memo.emplace(std::move(k),res);}
     out<<pid<<","<<a<<","<<side<<","<<raw<<","<<res.recurrence<<","<<res.period<<","<<res.cls<<","<<(cached?1:0)<<"\n";
     total++;
   }
 }
 assert(nparents==55&&total==3300);
 std::cerr<<"parents="<<nparents<<" probes="<<total<<" unique="<<memo.size()<<" horizon="<<H<<"\n";
 return 0;
}
