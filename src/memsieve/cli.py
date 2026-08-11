import argparse
from .core import Store

def main():
    p=argparse.ArgumentParser(description='Rank memories under a fixed budget.')
    p.add_argument('query'); p.add_argument('memories',nargs='+')
    a=p.parse_args(); s=Store(max_items=len(a.memories))
    for x in a.memories:s.add(x)
    for m in s.search(a.query):print(m.text)
if __name__=='__main__':main()
