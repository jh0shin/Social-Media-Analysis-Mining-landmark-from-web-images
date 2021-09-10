#!/usr/bin/python3

import os
import shutil

##### Global Settings #####
CLUSTER_NUM = '2'
CLUSTER_DIR = f'../cluster_phase2/{CLUSTER_NUM}/'

THRESHOLD = 0.5
CLUSTER_MIN_SIZE = 3

filelist = []
pairwise_score = []
cluster = []

##### File reading #####
# photo file list reading
f = open(f'./list_{CLUSTER_NUM}.txt', 'r', encoding='UTF8')
for line in f:
    # break if eof
    if not line: break

    filelist.append(line.strip().split(' ')[0])
f.close()

# pairwise score list reading
f = open(f'./pairwise_scores_{CLUSTER_NUM}.txt', 'r', encoding='UTF8')
for line in f:
    # break if eof
    if not line: break

    pairwise_score.append(line.split(' '))
f.close()

##### Clustering #####
for edge in pairwise_score:
    # break if score is below THRESHOLD
    if float(edge[2]) < THRESHOLD: continue

    xlocate = -1
    ylocate = -1

    # check existing clusters
    for it, c in enumerate(cluster):
        if edge[0] in c: xlocate = it
        if edge[1] in c: ylocate = it
    
    
    if xlocate == -1 and ylocate == -1:
        # no existing cluster include node
        cluster.append(edge[:2])
    elif xlocate == ylocate:
        # already in same cluster:
        continue
    elif xlocate != -1 and ylocate != -1:
        # two different existing node
        # combine two cluster into one
        cluster[xlocate].extend(cluster[ylocate])
        cluster.remove(cluster[ylocate])
    elif xlocate != -1:
        # only edge[0] belongs to existing cluster
        cluster[xlocate].append(edge[1])
    elif ylocate != -1:
        # only edge[1] belongs to existing cluster
        cluster[ylocate].append(edge[0])

##### File copy by cluster #####
for it, c in enumerate(cluster):
    # skip if cluster is smaller than CLUSTER_MIN_SIZE
    if len(c) < CLUSTER_MIN_SIZE:
        continue

    os.makedirs(CLUSTER_DIR + str(it), exist_ok=True)
    for index in c:
        shutil.copyfile(                                                \
            '../' + filelist[int(index)],                                            \
            CLUSTER_DIR + str(it) + '/' + filelist[int(index)].split('/')[2] \
        )