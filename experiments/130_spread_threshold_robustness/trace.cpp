// Experiment 130: predeclared spread-threshold robustness audit.
// All full-state phase-aware recurrence times are frozen in Experiment127.
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
inline State step(const State&s,int p){State o=s;for(int j=0;j<20;j++){
 int a=(p+3*j)%60,b=(a+1)%60,c=(a+2)%60;uint8_t x=s[a],y=s[b],z=s[c];
 o[a]=x^rot(y&z);o[b]=y^rot(x&z);o[c]=z^rot(x&y);
}return o;}
struct Key{State s;bool operator==(const Key&o)const{return s==o.s;}};
struct Hash{size_t operator()(const Key&k)const noexcept{uint64_t h=1469598103934665603ull;
 for(auto v:k.s){h^=v;h*=1099511628211ull;}return size_t(h);}};
const int TH[6]={10,20,30,40,50,60};
struct Desc{std::array<int,6> first;int certificate_tick;int max_union;};
Desc observe(State initial,int recurrence){
 const int horizon=recurrence==-1?50000:recurrence;
 assert(horizon>0 && horizon<=50000);
 Desc d;d.first.fill(-1);d.certificate_tick=recurrence;
 std::array<bool,60> seen{};int n=0;
 for(int i=0;i<60;i++)if(initial[i]){seen[i]=true;n++;}
 for(int j=0;j<6;j++)if(n>=TH[j])d.first[j]=0;
 for(int tick=1;tick<=horizon && d.first[5]==-1;tick++){
  initial=step(initial,(tick-1)%3);
  for(int i=0;i<60;i++)if(initial[i]&&!seen[i]){seen[i]=true;n++;}
  for(int j=0;j<6;j++)if(n>=TH[j]&&d.first[j]==-1)d.first[j]=tick;
 }
 d.max_union=n;
 return d;
}
int main(int argc,char**argv){if(argc!=4){std::cerr<<"usage trace states.bin exp127_probes.csv out.csv\n";return 2;}
 std::ifstream bin(argv[1],std::ios::binary);std::unordered_map<int,std::array<State,2>> states;std::unordered_map<int,std::array<int,2>> sites;
 while(true){uint8_t meta[4];bin.read(reinterpret_cast<char*>(meta),4);if(bin.gcount()==0)break;assert(bin.gcount()==4);
  std::array<State,2> s;for(auto &x:s){bin.read(reinterpret_cast<char*>(x.data()),60);assert(bin.gcount()==60);}
  states[meta[0]]=s;sites[meta[0]]={meta[2],meta[3]};}
 assert(states.size()==55);
 std::ifstream csv(argv[2]);std::string line;std::getline(csv,line);
 std::ofstream out(argv[3]);out<<"parent_id,arm,side,raw,recurrence,class,first10,first20,first30,first40,first50,first60,max_union\n";
 std::unordered_map<Key,Desc,Hash> cache;int n=0;
 while(std::getline(csv,line)){
  if(line.empty())continue;
  std::stringstream in(line);std::string part;std::vector<int> v;
  while(std::getline(in,part,','))v.push_back(std::stoi(part));
  assert(v.size()==8);
  int pid=v[0],arm=v[1],side=v[2],raw=v[3],recurrence=v[4],cls=v[6];
  State s=states.at(pid)[arm];int pos=sites.at(pid)[side];assert(s[pos]==0);s[pos]=raw;
  Key key{s};auto it=cache.find(key);Desc d;
  if(it==cache.end()){d=observe(s,recurrence);cache.emplace(key,d);}else d=it->second;
  out<<pid<<','<<arm<<','<<side<<','<<raw<<','<<recurrence<<','<<cls;
  for(int first:d.first)out<<','<<first;
  out<<','<<d.max_union<<'\n';n++;
 }
 assert(n==3300);std::cerr<<"probes="<<n<<" distinct="<<cache.size()<<"\n";
}
