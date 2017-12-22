#!/usr/bin/env python3

'''
This script reads some files with words (attributes and target groups)
and creates a new file with combinations of those

'''

import itertools

crim = [line.strip() for line in open('../ressources/words_crime.txt').readlines() if len(line)>1]
low  = [line.strip() for line in open('../ressources/words_lowlife.txt').readlines() if len(line)>1]
targ  = [line.strip() for line in open('../ressources/words_target.txt').readlines() if len(line)>1]


# remove duplicates

crim = set(crim)
low = set(low)
targ = set(targ)


pairs_crim = list(itertools.product(crim,targ))
pairs_low = list(itertools.product(low,targ))


with open('../ressources/combinations_crime',mode='w') as fo:
    for pair in pairs_crim:
        fo.write("{},{}\n".format(pair[0],pair[1]))
        

with open('../ressources/combinations_lowlife',mode='w') as fo:
    for pair in pairs_low:
        fo.write("{},{}\n".format(pair[0],pair[1]))