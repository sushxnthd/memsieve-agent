import json, random, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'src'))
from memsieve.core import Store
random.seed(5); trials=200; hits=0
for i in range(trials):
    topic=f'project-{i}'
    s=Store(max_items=24)
    s.add(f'{topic} deployment password rotation schedule friday',importance=.9,timestamp=1000)
    for j in range(80):s.add(f'noise item {j} random note {random.randrange(9999)}',importance=.1,timestamp=1000+j)
    hits += topic in s.search(f'when is {topic} password rotation',k=1,now=2000)[0].text
result={'trials':trials,'top1_recall':hits/trials,'memory_budget':24,'stream_length':81}
Path(__file__).with_name('results.json').write_text(json.dumps(result,indent=2));print(result)
