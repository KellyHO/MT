#!/usr/bin/env python
import sys, os
from itertools import product
from collections import defaultdict

STOP = '。 、 ， ！ ？ 「 」 （ ） ( ) ： ； , ( ) '.split()

PREPS = [x.strip() for x in open('prepositions.txt').readlines()]
CPREPS = [x.strip() for x in open('prepositions-ch.txt').readlines()]
GRAMMAR = ['V', 'A', 'n']

def read_tm():
    deps = defaultdict(lambda: defaultdict(lambda: []))
    for line in open('tm.11.large.txt').readlines():
        # 放棄	abandon	0.12	191.0	2582.0	454.0
        cword, eword, dice, cec, cc, ce = line.strip().split('\t')
        deps[eword][cword] = float(dice)
    return deps
    
def prep_in_deps(prep, deps):
    return prep in str(deps)

def read_phrase_tm(tm):
    for line in open('mp.V.deps.tm.txt').readlines():
        # print (line)
        # abandon its non-cooperation operation	放棄 不 合作 政策	1	['V:obj:N']
        ephrase, cphrase, cce, rels = line.strip().split('\t')
        headtag, deptag = eval(rels)[0][0], eval(rels)[0][-1].lower()
        eword, cword = ephrase.split(), cphrase.split()
        epat, cpat = ' '+ephrase+' ', ' '+cphrase+' '
        head, dep = eword[0], eword[-1]
        if head != 'negotiate' or dep != 'government': continue

        # Step 1: replace headword and translation
        dice, headtran = max([ (tm[head][c], c) for c in cword if head in tm and c in tm[head] and c not in CPREPS])
        epat, cpat = epat.replace(' '+head+' ', ' V '), cpat.replace(' '+headtran+' ', ' V ')
        
        # Step 2: replace dep and translation
        dice, deptran = max([ (tm[dep][c], c) for c in cword if dep in tm and c in tm[dep] and c not in CPREPS ])
        epat, cpat = epat.replace(dep, ' '+deptag+' '), cpat.replace(deptran, ' '+deptag+' ')
        
        # Step 3: remove non grammar elements
        epat, cpat = epat.strip().split(), cpat.strip().split()
        epat, cpat = ' '.join([x for x in epat if x in GRAMMAR+PREPS]), ' '.join([x for x in cpat if x in GRAMMAR+PREPS+CPREPS])
        
        print (ephrase, '-->', cphrase)
        print ('\t'+head+' | '+headtran, '-->', epat+' | '+cpat)
        print ()

    # Step 4: Group, count, and output synchronous rules and related headword translations 

            
if __name__ == '__main__':
    tm = read_tm()
    #print (PREPS)
    #print ( [x for x in tm.items() ][:1][:3] )
    read_phrase_tm(tm)
    
    # egrep '^[a-z][^\ \-]+\t(V|A|N):.*:N\t[a-z][^\ \-]+\t' mp.deps.txt | egrep -v ':(subj|appo|conj|gen|guest|amod|mod):' > mp.VANpn.txt
    