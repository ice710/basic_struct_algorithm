#!/usr/bin/env python
#coding:utf-8

import sys
import random

if __name__=='__main__':
    
    if len(sys.argv) < 3:
        print 'input [infile][lines][outfile]'
    infile = sys.argv[1]
    k = int(sys.argv[2])
    if len(sys.argv) >= 4:
        sys.stdout = open(sys.argv[3], 'w')

    reservior = []
    lineno = 0

    with open(infile) as fr:
        for i in range(k):
            reservior.append(fr.readline())
            lineno += 1

        while True:
            line = fr.readline()
            if not line:
                break
            lineno +=1 
            n = random.randint(1, lineno)
            if n < k:
                reservior[n] = line


    for item in reservior:
        print item

