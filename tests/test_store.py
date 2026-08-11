from memsieve.core import Store

def test_duplicate_suppression():
    s=Store(); assert s.add('alpha beta gamma'); assert not s.add('alpha beta gamma')

def test_retrieval():
    s=Store(); s.add('invoice 17 is due friday',.9,1); s.add('weather is sunny',.2,2)
    assert 'invoice' in s.search('when is invoice due',1,3)[0].text


def test_budget_is_hard_limit():
    s=Store(max_items=3)
    for i in range(10):s.add(f'unique note {i}',importance=i/10,timestamp=i)
    assert len(s.items)==3

def test_roundtrip(tmp_path):
    s=Store(); s.add('remember alpha',.8,10); f=tmp_path/'m.json'; s.dump(str(f))
    restored=Store.load(str(f)); assert restored.items[0].text=='remember alpha'
