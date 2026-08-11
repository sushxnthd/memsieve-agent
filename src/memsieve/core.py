from __future__ import annotations
from dataclasses import dataclass
from math import log1p
import re, time

_WORD=re.compile(r"[a-z0-9]+")
def tokens(s:str)->set[str]: return set(_WORD.findall(s.lower()))

def jaccard(a:set[str],b:set[str])->float:
    return len(a&b)/max(1,len(a|b))

@dataclass
class Memory:
    text: str
    timestamp: float
    importance: float = .5
    hits: int = 0

class Store:
    def __init__(self, max_items:int=128): self.max_items=max_items; self.items:list[Memory]=[]
    def add(self,text:str,importance:float=.5,timestamp:float|None=None):
        now=time.time() if timestamp is None else timestamp
        t=tokens(text)
        if any(jaccard(t,tokens(m.text))>.88 for m in self.items): return False
        self.items.append(Memory(text,now,min(max(importance,0),1)))
        self._trim(now); return True
    def _trim(self,now:float):
        if len(self.items)<=self.max_items:return
        ranked=sorted(self.items,key=lambda m:self._base(m,now),reverse=True)
        self.items=ranked[:self.max_items]
    def _base(self,m:Memory,now:float)->float:
        age=max(0,now-m.timestamp)
        recency=1/(1+age/86400)
        usage=min(1,log1p(m.hits)/3)
        return .5*m.importance+.3*recency+.2*usage
    def search(self,query:str,k:int=5,now:float|None=None)->list[Memory]:
        now=time.time() if now is None else now; q=tokens(query)
        scored=[]
        for m in self.items:
            relevance=jaccard(q,tokens(m.text)); score=.68*relevance+.32*self._base(m,now)
            scored.append((score,m))
        top=[m for _,m in sorted(scored,key=lambda x:x[0],reverse=True)[:k]]
        for m in top:m.hits+=1
        return top


    def stats(self) -> dict[str,float]:
        if not self.items:return {'items':0,'mean_importance':0.0,'hit_memories':0}
        return {'items':len(self.items),'mean_importance':sum(m.importance for m in self.items)/len(self.items),'hit_memories':sum(m.hits>0 for m in self.items)}

    def dump(self,path:str)->None:
        import json
        from dataclasses import asdict
        from pathlib import Path
        Path(path).write_text(json.dumps([asdict(m) for m in self.items],indent=2))

    @classmethod
    def load(cls,path:str,max_items:int=128)->'Store':
        import json
        from pathlib import Path
        s=cls(max_items=max_items)
        for row in json.loads(Path(path).read_text()):s.items.append(Memory(**row))
        s._trim(time.time()); return s
