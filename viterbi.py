#!/usr/bin/env python
#coding: utf-8
import numpy as np


#init_status_pro
#trans_status_pro
#emit_pro
def viterbi(obs, init_status_pro, trans_status_pro, emit_pro):
    MIN_DOUBLE = -999999.0
    obs_num = len(obs)
    status_num = len(init_status_pro)
    weights = np.zeros((status_num, obs_num))
    paths = np.zeros((status_num, obs_num))
    weights[:, 0] = init_status_pro + emit_pro[:, obs[0]]
    for i in range(obs_num)[1:]:
        for j in range(status_num):
            weights[j, i] = MIN_DOUBLE
            paths[j, i] = -1
            tmp = weights[:, i-1] + trans_status_pro[:, j] + emit_pro[:, obs[i]]
            weights[j, i] = np.max(tmp)
            #print list(tmp).index(weights[j, i])
            paths[j, i] = list(tmp).index(weights[j, i])
    print 'weights:'
    print weights
    print 'paths:'
    print paths
    seq = []
    y = obs_num - 1
    x = list(weights[:, y]).index(max(weights[:, y]))
    seq.insert(0, x)
    for i in range(obs_num)[1:]:
        print x, y
        y = obs_num - i
        seq.insert(0, paths[x, y])
        x = int(paths[x, y])
    return seq

def test():
    init_status_pro = np.log2(np.array([0.2, 0.4, 0.4]).T)
    print 'init_status_pro:'
    print init_status_pro
    trans_status_pro = np.log2(np.array([[0.5, 0.2, 0.3],
                                        [0.3, 0.5, 0.2],
                                        [0.2, 0.3, 0.5]]
                                        ))
    print 'trans_status_pro:'
    print trans_status_pro
    emit_pro = np.log2(np.array([[0.5, 0.5],
                                [0.4, 0.6],
                                [0.7, 0.3]]
                                ))
    print 'emit_pro:'
    print emit_pro
    obs = [0, 1, 0]
    seq = viterbi(obs, init_status_pro, trans_status_pro, emit_pro)
    print 'seq:', seq

if __name__=='__main__':
    test()
