import suds
import xmltodict
from json import loads, dumps
from collections import OrderedDict
from tinydb import TinyDB, where
import time
import shutil
import whoosh.index as windex 
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.query import *
import urllib2
import base64
import json
import re
from itertools import islice

dbNyt = TinyDB('/home/luis/data/mario/openedu/tinydb/nyt.json')
tblNyt = dbNyt.table('nyt')

path = "/home/luis/data/mario/nyt/nyt-text/"

clusterIID = {}
articleIID = {}
cach = {}

reqcount = {}
totalcount = 0

def getReq():
    return reqcount

def getTotalReq():
    return totalcount

def loadNytText():
    ins = open(path+'texts.txt', "rw+")
    line = 1
    while line:
        pos = ins.tell()
        line = ins.readline()
        cid = line.split('#')[0]
        #print 'pos',str(pos)
        clusterIID[cid] = pos

def loadNytCluster():
    ins = open(path+'cluster_article_id.txt', "rw+")
    ins.readline()
    line = 1
    while line:
        pos = ins.tell()
        line = ins.readline()
        cid = line.split('\t')[0]
        #print 'pos',str(pos)
        articleIID[cid] = pos

def searchNytClusterIds(inIds):
    inIds = inIds.split(',')
    arr = []
    for inId in inIds[0:10]:
        arr.append(searchNytClusterId(inId))
    return arr

def searchNytClusterId(inId):
    if not cach.has_key(inId):
        return fileSearch(inId)
    else:
        return cachSearch(inId)

def cachSearch(inId):
    if tblNyt.get(where('id') == inId):
        print "tblNyt return"
        return tblNyt.get(where('id') == inId)
    else:
        return cach[inId]

def count_nyt():
    return int(len(cach))

def idSearch(inId):
    lnum = -1
    text = ""
    title = ""
    if articleIID.has_key(inId):
        lnum = articleIID[inId]
    cid = ""

    if lnum != -1:
        lnum += 2
        fo = open(path+'cluster_article_id.txt',"rw+")
        fo.seek(lnum,0)
        line = fo.readline()
        cid = line.split('\t')[1].rstrip('\n')

    return cid

def fileSearch(inId):
    lnum = -1
    text = ""
    title = ""
    if articleIID.has_key(inId):
        lnum = articleIID[inId]
    cid = ""

    if lnum != -1:
        lnum += 2
        fo = open(path+'cluster_article_id.txt',"rw+")
        fo.seek(lnum,0)
        line = fo.readline()
        print "line1: ",line
        cid = line.split('\t')[1].rstrip('\n')
        #with open('/media/mario/My Book/mario/sopho/nyt/nyt/nyt-text/cluster_article_id.txt') as f:
            #line = next(islice(f, lnum - 1, lnum))
            #cid = line.split('\t')[1].rstrip('\n')
            
    if clusterIID.has_key(cid):
        lnum = clusterIID[cid]
        fo = open(path+'texts.txt',"rw+")
        fo.seek(lnum,0)
        line = fo.readline()
        print "line2:", line
        text = line.split('#')[1].rstrip('\n')
        #with open('/media/mario/My Book/mario/sopho/nyt/nyt/nyt-text/texts.txt') as f:
            #line = next(islice(f, lnum - 1, lnum))
            #text = line.split('#')[1].rstrip('\n')
        
        ''' 
        fo = open('/media/mario/My Book/mario/sopho/nyt/nyt/nyt-text/titles.txt',"rw+")
        fo.seek(lnum,0)
        line = fo.readline()
        print "line3:", line
        #line = next(islice(f, lnum - 1, lnum))
        title = line.split('#')[2].rstrip('\n')
        #with open('/media/mario/My Book/mario/sopho/nyt/nyt/nyt-text/titles.txt') as f:
            #line = next(islice(f, lnum - 1, lnum))
            #title = line.split('#')[2].rstrip('\n')
        '''

    out = {}
    #out['title'] = title
    out['text'] = text
    out['id'] = inId
    out['cid'] = cid

    cach[inId] = out
    if tblNyt.get(where('id') == inId) == None:
        tblNyt.insert(out)
        print 'tblNyt insert'

    return out
      
# from sorted dict to dict
def to_dict(input_ordered_dict):
    return loads(dumps(input_ordered_dict))
