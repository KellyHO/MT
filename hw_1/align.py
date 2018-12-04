#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from collections import defaultdict, Counter
from itertools import product
from operator import itemgetter
import fileinput

# f --> e
def init_IBM_Prob(bitext):
    e_word = set()
    f_word = set()
    CORPUS_F = []
    CORPUS_EN = []

    for sent in bitext:
        CORPUS_F.append(sent[0])
        CORPUS_EN.append(sent[1])
        for f in sent[0]:
            f_word.add(f)
        for e in sent[1]:
            e_word.add(e)
    # print(CORPUS_F, CORPUS_EN)
    
    IBM_Prob = defaultdict(lambda: defaultdict())
    for f in list(f_word):
        for e in list(e_word):
            IBM_Prob[e][f] = 1.0/len(e_word)
    return IBM_Prob, f_word, e_word, CORPUS_F, CORPUS_EN

def compute_em_trans_p(ibm_prob):
    # TODO: implement IBM Model 1

    C = defaultdict(lambda: {})
    # E
    for all_e, all_f in zip(CORPUS_EN, CORPUS_F):
        for ei in all_e:  
            sum_t = sum(ibm_prob[ei].values() ) * 1.0
            for fj in all_f:
                delta = ibm_prob[ei][fj] / sum_t
                C[fj][ei] =  C[fj].get(ei, 0) + delta
    # M
    for e in e_word:
        for f in f_word:
            if f in C and e in C[f]:
                ibm_prob[e][f] = C[f][e] / sum(C[f].values())


    return ibm_prob


def read_bitext(iterable):
    return [[(sent.split()) for sent in line.strip().split('\t')] for line in iterable]


def compute_dice(bitext):
    f_count, e_count, fe_count = Counter(), Counter(), Counter()
    for f, e in bitext:
        f, e = set(f), set(e)
        f_count.update(f)
        e_count.update(e)
        fe_count.update(product(f, e))

    dice = defaultdict(float)
    for f_i, e_j in fe_count:
        dice[f_i, e_j] = 2 * fe_count[f_i, e_j] / (f_count[f_i] + e_count[e_j])
    return dice


if __name__ == '__main__':
    bitext = read_bitext(fileinput.input())
    phraseTable = compute_dice(bitext)
    print(phraseTable)
    # TODO: use following line after IBM Model 1 is implemented
    phraseTable, f_word, e_word, CORPUS_F, CORPUS_EN  = init_IBM_Prob(bitext)
    for epoch in range(5):
        phraseTable = compute_em_trans_p(phraseTable)
    # print(phraseTable)


    for f, e in bitext[:10]:
        alignProb = [(i, j, f_i, e_j, phraseTable[e_j][f_i])
                     for i, f_i in enumerate(f) for j, e_j in enumerate(e)
                     if e_j in phraseTable and f_i in phraseTable[e_j]]
        alignProb.sort(key=itemgetter(4), reverse=True)

    # for f, e in bitext[:10]:
    #     alignProb = [(i, j, f_i, e_j, phraseTable[f_i, e_j])
    #                  for i, f_i in enumerate(f) for j, e_j in enumerate(e)
    #                  if (f_i, e_j) in phraseTable]
    #     alignProb.sort(key=itemgetter(4), reverse=True)

        doneF, doneE = set(), set()
        res = []
        for i, j, f_i, e_j, prob in alignProb:
            if i not in doneF and j not in doneE:
                res.append((i, j, f_i, e_j, prob))
                doneF.add(i)
                doneE.add(j)

        print(' '.join(f))
        print(' '.join(e))

        res.sort(key=itemgetter(0))
        for i, j, f_i, e_j, prob in res:
            print(i, j, f_i, e_j, prob, sep='\t')
