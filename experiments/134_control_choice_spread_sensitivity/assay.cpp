// Experiment134: exact 104 three-phase physics, monotone spread event only.
// Eligible control initial states were constructed before any injected outcome assay.
#include <array>
#include <unordered_map>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <cassert>
using State=std::array<uint8_t,60>;
struct Key{State s;uint8_t phase;bool operator==(const Key& o)const{return phase==o.phase&&s==o.s;}};
struct Hash{size_t operator()(const Key& k)const noexcept{uint64_t h=1469598103934665603ull;for(auto v:k.s){h^=v;h*=1099511628211ull;}h^=k.phase;h*=1099511628211ull;return size_t(h);}};
inline uint8_t rot(uint8_t x){return uint8_t(((x<<1)&15)|(x>>3));}
inline State step(const State&s,int p){State o=s;for(int j=0;j<20;j++){
 int a=(p+3*j)%60,b=(a+1)%60,c=(a+2)%60;uint8_t x=s[a],y=s[b],z=s[c];
 o[a]=x^rot(y&z);o[b]=y^rot(x&z);o[c]=z^rot(x&y);
}return o;}
struct Outcome{int first10=-1,first60=-1,recurrence=-1;};
Outcome trial(State s,int horizon){
 Outcome r;std::array<bool,60> visited{};int coverage=0;
 for(int i=0;i<60;i++)if(s[i]){visited[i]=true;coverage++;}
 if(coverage>=10)r.first10=0;
 if(coverage>=60){r.first60=0;return r;}
 std::unordered_map<Key,int,Hash> seen;seen.reserve(128);seen.emplace(Key{s,0},0);
 for(int tick=1;tick<=horizon;tick++){
  s=step(s,(tick-1)%3);
  for(int i=0;i<60;i++)if(s[i]&&!visited[i]){visited[i]=true;coverage++;}
  if(r.first10<0&&coverage>=10)r.first10=tick;
  if(coverage==60){r.first60=tick;return r;}
  Key k{s,uint8_t(tick%3)};if(seen.find(k)!=seen.end()){r.recurrence=tick;return r;}
  seen.emplace(std::move(k),tick);
 }
 return r;
}
int fromhex(char a,char b){auto f=[](char c)->int{if(c>='0'&&c<='9')return c-'0';if(c>='a'&&c<='f')return c-'a'+10;assert(false);return 0;};return 16*f(a)+f(b);}
int main(int argc,char**argv){if(argc!=4){std::cerr<<"usage: assay alternatives.csv result.csv horizon\n";return 2;}
 int H=std::stoi(argv[3]);if(H<1||H>50000)return 2;
 std::ifstream in(argv[1]);std::string line;std::getline(in,line);std::ofstream out(argv[2]);
 out<<"parent_id,attempt,rank,side,raw,first10,first60,recurrence\n";
 int nstates=0,probes=0,cert10=0,cert60=0,censored=0;
 while(std::getline(in,line)){
  if(line.empty())continue;std::stringstream ss(line);std::vector<std::string> fields;std::string s;
  while(std::getline(ss,s,','))fields.push_back(s);
  assert(fields.size()==7);
  int pid=std::stoi(fields[0]),attempt=std::stoi(fields[1]),rank=std::stoi(fields[2]);
  int left=std::stoi(fields[3]),right=std::stoi(fields[4]);
  assert(left>=0&&left<60&&right>=0&&right<60&&left!=right);
  const std::string &hex=fields[5];assert(hex.size()==120);
  State base;for(int i=0;i<60;i++){base[i]=uint8_t(fromhex(hex[2*i],hex[2*i+1]));assert(base[i]<16);}
  nstates++;
  for(int side=0;side<2;side++)for(int raw=1;raw<=15;raw++){
   State state=base;int position=side?right:left;assert(state[position]==0);state[position]=uint8_t(raw);
   auto r=trial(state,H);out<<pid<<','<<attempt<<','<<rank<<','<<side<<','<<raw<<','<<r.first10<<','<<r.first60<<','<<r.recurrence<<'\n';
   probes++;cert10+=r.first10>=0;cert60+=r.first60>=0;censored+=r.recurrence<0&&r.first60<0;
  }
 }
 assert(nstates==32&&probes==960);
 std::cerr<<"alternative_control_states="<<nstates<<" probes="<<probes<<" ever10="<<cert10<<" ever60="<<cert60<<" unknown60="<<censored<<"\n";
}
