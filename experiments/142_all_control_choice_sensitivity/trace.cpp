// Exp140: fixed first accepted 1000-candidate control, no outcome-aware selection.
// Reuses the deterministic 104/134 60-window physical kernel unchanged.
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
struct Key{State s;uint8_t phase;bool operator==(const Key&o)const{return phase==o.phase&&s==o.s;}};
struct Hash{size_t operator()(const Key& k)const noexcept{uint64_t h=1469598103934665603ull;for(auto v:k.s){h^=v;h*=1099511628211ull;}h^=k.phase;h*=1099511628211ull;return size_t(h);}};
inline uint8_t rot(uint8_t x){return uint8_t(((x<<1)&15)|(x>>3));}
inline State step(const State&s,int p){State o=s;for(int j=0;j<20;j++){int a=(p+3*j)%60,b=(a+1)%60,c=(a+2)%60;uint8_t x=s[a],y=s[b],z=s[c];o[a]=x^rot(y&z);o[b]=y^rot(x&z);o[c]=z^rot(x&y);}return o;}
struct Outcome{int first10=-1,first60=-1,recurrence=-1;};
Outcome trial(State s,int horizon){
 Outcome r;std::array<bool,60> visited{};int n=0;
 for(int i=0;i<60;i++)if(s[i]){visited[i]=true;n++;}
 if(n>=10)r.first10=0;
 if(n>=60){r.first60=0;return r;}
 std::unordered_map<Key,int,Hash> seen;seen.reserve(128);seen.emplace(Key{s,0},0);
 for(int t=1;t<=horizon;t++){
   s=step(s,(t-1)%3);
   for(int i=0;i<60;i++)if(s[i]&&!visited[i]){visited[i]=true;n++;}
   if(r.first10<0&&n>=10)r.first10=t;
   if(n==60){r.first60=t;return r;}
   Key k{s,uint8_t(t%3)};if(seen.find(k)!=seen.end()){r.recurrence=t;return r;}
   seen.emplace(std::move(k),t);
 }
 return r;
}
int fromhex(char a,char b){auto f=[](char c)->int{if(c>='0'&&c<='9')return c-'0';if(c>='a'&&c<='f')return c-'a'+10;assert(false);return 0;};return 16*f(a)+f(b);}
int main(int argc,char**argv){
 if(argc!=4){std::cerr<<"usage trace selected_states.csv results.csv horizon\n";return 2;}
 int H=std::stoi(argv[3]);if(H<1||H>50000)return 2;
 std::ifstream in(argv[1]);std::string line;std::getline(in,line);std::ofstream out(argv[2]);
 out<<"parent_id,attempt,arm,side,raw,first10,first60,recurrence\n";
 int frames=0,probes=0;
 std::unordered_map<Key,Outcome,Hash> cache;
 while(std::getline(in,line)){
  if(line.empty())continue;std::stringstream ss(line);std::vector<std::string> a;std::string q;
  while(std::getline(ss,q,','))a.push_back(q);
  if(a.size()!=6)return 3;
  int pid=std::stoi(a[0]),att=std::stoi(a[1]),arm=std::stoi(a[2]),left=std::stoi(a[3]),right=std::stoi(a[4]);
  assert(left>=0&&right<60&&left!=right&&a[5].size()==120);
  State base;for(int i=0;i<60;i++){base[i]=fromhex(a[5][2*i],a[5][2*i+1]);assert(base[i]<16);}
  frames++;
  for(int side=0;side<2;side++)for(int raw=1;raw<=15;raw++){
    State s=base;int pos=side?right:left;assert(s[pos]==0);s[pos]=uint8_t(raw);
    Key key{s,0};Outcome o;
    auto it=cache.find(key);
    if(it==cache.end()){o=trial(s,H);cache.emplace(key,o);}else{o=it->second;}
    out<<pid<<','<<att<<','<<arm<<','<<side<<','<<raw<<','<<o.first10<<','<<o.first60<<','<<o.recurrence<<'\n';probes++;
  }
 }
 std::cerr<<"selected_frames="<<frames<<" probes="<<probes<<" cached_distinct="<<cache.size()<<"\n";
 return frames==970&&probes==29100?0:4;
}
