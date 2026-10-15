// Experiment 128: physical-support trajectories for Exp127 50k-censored states.
// No new observer of recurrence, only descriptive physical activity diagnostics.
#include <array>
#include <vector>
#include <cstdint>
#include <cassert>
#include <fstream>
#include <sstream>
#include <iostream>
#include <unordered_map>
#include <algorithm>
#include <string>
using State=std::array<uint8_t,60>;
inline uint8_t rot(uint8_t x){return uint8_t(((x<<1)&15)|(x>>3));}
inline State step(const State& s,int p){State o=s;for(int j=0;j<20;j++){
 int a=(p+3*j)%60,b=(a+1)%60,c=(a+2)%60;uint8_t x=s[a],y=s[b],z=s[c];
 o[a]=x^rot(y&z);o[b]=y^rot(x&z);o[c]=z^rot(x&y);
}return o;}
struct Key{State s;bool operator==(const Key&o)const{return s==o.s;}};
struct Hash{size_t operator()(Key const& k)const noexcept{uint64_t h=1469598103934665603ull;
 for(auto v:k.s){h^=v;h*=1099511628211ull;}return size_t(h);}};
struct Metrics{int union_500=0,union_2000=0,union_10000=0,union_50000=0;
 int max_active=0,final_active=0,first_union30=-1,first_union60=-1,first_active30=-1;
 long long total_occupied=0,total_popcount=0;};
Metrics analyze(const State& initial){Metrics m;State s=initial;std::array<bool,60> seen{};int seen_n=0;
 for(int tick=0;tick<=50000;tick++){
  int occupied=0;
  for(int i=0;i<60;i++){
   if(s[i]){occupied++;if(!seen[i]){seen[i]=true;seen_n++;}}
  }
  if(tick>0){m.total_occupied+=occupied;
    for(int i=0;i<60;i++)m.total_popcount+=__builtin_popcount((unsigned int)s[i]);}
  m.max_active=std::max(m.max_active,occupied);
  if(m.first_active30==-1&&occupied>=30)m.first_active30=tick;
  if(m.first_union30==-1&&seen_n>=30)m.first_union30=tick;
  if(m.first_union60==-1&&seen_n==60)m.first_union60=tick;
  if(tick==500)m.union_500=seen_n;
  if(tick==2000)m.union_2000=seen_n;
  if(tick==10000)m.union_10000=seen_n;
  if(tick==50000){m.union_50000=seen_n;m.final_active=occupied;break;}
  s=step(s,tick%3);
 }
 return m;
}
int main(int argc,char**argv){if(argc!=4){std::cerr<<"usage: trace <Exp127 states.bin> <Exp127 probes.csv> <output.csv>\n";return 2;}
 std::ifstream bin(argv[1],std::ios::binary);if(!bin) return 2;
 std::unordered_map<int,std::array<State,2>> states;std::unordered_map<int,std::array<int,2>> sites;
 while(true){uint8_t meta[4];bin.read(reinterpret_cast<char*>(meta),4);if(bin.gcount()==0)break;
  assert(bin.gcount()==4);std::array<State,2> s;for(auto &x:s){bin.read(reinterpret_cast<char*>(x.data()),60);assert(bin.gcount()==60);}
  states[meta[0]]=s;sites[meta[0]]={meta[2],meta[3]};
 }
 assert(states.size()==55);
 std::ifstream csv(argv[2]);std::string line;std::getline(csv,line);
 std::ofstream out(argv[3]);out<<"parent_id,arm,side,raw,union_500,union_2000,union_10000,union_50000,max_simultaneous_active,final_active,first_union30,first_union60,first_active30,total_active_site_ticks,total_set_bit_ticks\n";
 std::unordered_map<Key,Metrics,Hash> cached;int records=0;
 while(std::getline(csv,line)){
  if(line.empty())continue;
  std::vector<int> v;std::stringstream s(line);std::string token;
  while(std::getline(s,token,','))v.push_back(std::stoi(token));
  assert(v.size()==8);if(v[4]!=-1)continue;
  int pid=v[0],arm=v[1],side=v[2],raw=v[3];assert(raw>=1&&raw<=15);
  State state=states.at(pid)[arm];int pos=sites.at(pid)[side];assert(!state[pos]);state[pos]=raw;
  Key k{state};auto it=cached.find(k);
  Metrics m;
  if(it==cached.end()){m=analyze(state);cached.emplace(k,m);}else m=it->second;
  out<<pid<<','<<arm<<','<<side<<','<<raw<<','<<m.union_500<<','<<m.union_2000<<','<<m.union_10000<<','<<m.union_50000<<','<<m.max_active<<','<<m.final_active<<','<<m.first_union30<<','<<m.first_union60<<','<<m.first_active30<<','<<m.total_occupied<<','<<m.total_popcount<<'\n';records++;
 }
 std::cerr<<"censored_probe_records="<<records<<" unique_censored_states="<<cached.size()<<"\n";
 assert(records==537);
}
