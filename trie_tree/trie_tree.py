#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys

class trie_tree(object):
    def __init__(self):
        self.tree = {}
        self.buff = ['root']

    def _insert(self, word):
        tree = self.tree
        for c in word:
            tree = tree.setdefault(c, {})
        tree['exist'] = True

    def _search(self, word):
        tree = self.tree
        for c in word:
            if c in tree:
                tree = tree.get(c)
            else:
                return False

        if 'exist' in tree and tree['exist'] == True:
            return True
        else:
            return False

    def _print(self, tree, level=0, prefix=''):
        count = len(tree.items())
        for k, v in tree.items():
            count -= 1
            self.buff.append('%s +- %s' % (prefix , k if k!='exist' else 'NULL'))
            if v and not isinstance(v, bool):
                if count == 0:
                    self._print(v, level+1, prefix+'    ')
                else:
                    self._print(v, level+1, prefix+' |  ')

def test(f_name):
    lfreq = {}
    ltotal = 0.0
    tree = trie_tree()
    with open(f_name, 'rb') as f:
        lineno = 0
        for line in f.read().rstrip().decode('utf-8').split('\n'):
            lineno += 1
            print lineno
            try:
                word,freq,_ = line.split(' ')
                freq = float(freq)
                lfreq[word] = freq
                ltotal+=freq
                tree._insert(word)
            except ValueError, e:
                print e

    tree._print(tree.tree, 0)
    print '\n'.join(tree.buff).encode('utf-8')
    print '美如画'
    if tree._search(u'美如画'):
        print 'find it'
    else:
        print 'no exsit'

if __name__ == '__main__':
    test(sys.argv[1])
