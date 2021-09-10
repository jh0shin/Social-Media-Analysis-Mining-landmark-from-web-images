#!/usr/bin/python3
import os
import shutil
import csv

import pandas as pd
from math import log

##### Global Settings #####
CLUSTER_NUM = '4'
CLUSTER_DIR = f'../cluster_phase2/{CLUSTER_NUM}/'
NEW_CLUSTER_DIR = f'../cluster_phase3/{CLUSTER_NUM}/'

THRESHOLD = 0.5
CLUSTER_MIN_SIZE = 3
MIN_TAGNUM = 2

subcluster = []
subclustername = []

tagFile = '../Tag.csv'
tag = {}

##### File reading #####
# tag reading
f = open(tagFile, 'r', encoding='UTF8')
for line in csv.reader(f):
    # break if eof
    if not line: break

    if line[1] == '0':
        tag[line[0]] = [line[2]]
    else:
        tag[line[0]].append(line[2])
f.close()

# cluster reading
subclusterlist = os.listdir(CLUSTER_DIR)
subclusterlist.sort()

for sub in subclusterlist:
    tmp = os.listdir(CLUSTER_DIR + sub + '/')
    subFile = []

    for file in tmp:
        subFile.append(file.split('.')[0])
    
    subclustername.append(sub)
    subcluster.append(subFile)

'''
##### Tag scoring 1 #####
# 1. build vocabulary
# 2. calculate jaccard similarity between vocab and picture's tag
# 3. choose pictures over threshold for cluster
for i in range(len(subcluster)):
    vocab = []
    score = []

    # build vocab if tag exists
    for picture in subcluster[i]:
        if picture in list(tag.keys()):
            for value in tag[picture]:
                if value not in vocab:
                    vocab.append(value)

    # calculate jaccard similarity
    for picture in subcluster[i]:
        if picture in list(tag.keys()):
            jaccard_sim = len(set(vocab).intersection(tag[picture])) \
                        / len(set(vocab).union(tag[picture]))
            score.append(jaccard_sim)
        else:
            score.append(0)
        
        # print(f"{picture}, {jaccard_sim}")

    # cluster above threshold score
    cluster = []
    clustertag = []

    for j in range(len(subcluster[i])):
        if score[j] > THRESHOLD:
            cluster.append(subcluster[i][j])
            clustertag.append(tag[subcluster[i][j]])
    
    # skip if cluster is smaller than CLUSTER_MIN_SIZE
    if len(cluster) < CLUSTER_MIN_SIZE:
        continue
    
    # cluster file copy
    for c in cluster:
        os.makedirs(NEW_CLUSTER_DIR + str(subclustername[i]), exist_ok=True)
        for index in c:
            shutil.copyfile(                                                \
                CLUSTER_DIR + str(subclustername[i]) + '/' + c + '.jpg',                                            \
                NEW_CLUSTER_DIR + str(subclustername[i]) + '/' + c + '.jpg'\
            )
'''

##### Tag scoring 2 #####
# 1. build vocabulary
# 2. calculate TF-IDF for each tag
#    => tf = 1 for all tags
#    => 1d score array
# 3. choose pictures over threshold for cluster
for i in range(len(subcluster)):
    subimage = []
    subtag = []
    vocab = []
    score = []

    # save image info and build vocab when tag exists
    for picture in subcluster[i]:
        if picture in list(tag.keys()):
            subimage.append(picture)
            subtag.append(tag[picture])

            for value in tag[picture]:
                if value not in vocab:
                    vocab.append(value)

    # calculate tf-idf score
    for t in vocab:
        df = 0
        for s in subtag:
            if t in s: df += 1

        score.append(log((1 + len(subimage)) / (1 + df)))


    # cluster above threshold score
    cluster = []
    clustertag = []

    for j in range(len(subimage)):
        idf_mean = 0
        idf_num = 0
        for t in subtag[j]:
            idf_mean += score[vocab.index(t)]
            idf_num += 1
        idf_mean /= idf_num

        if idf_mean < THRESHOLD and len(subtag[j]) >= MIN_TAGNUM:
            cluster.append(subimage[j])
            clustertag.append(subtag[j])

    # skip if cluster is smaller than CLUSTER_MIN_SIZE
    if len(cluster) < CLUSTER_MIN_SIZE:
        continue
    
    # cluster file copy
    for c in cluster:
        os.makedirs(NEW_CLUSTER_DIR + str(subclustername[i]), exist_ok=True)
        for index in c:
            shutil.copyfile(                                                \
                CLUSTER_DIR + str(subclustername[i]) + '/' + c + '.jpg',                                            \
                NEW_CLUSTER_DIR + str(subclustername[i]) + '/' + c + '.jpg'\
            )