from data import get_data
import json

get_data.loadNytCluster()
print "start write"
with open("./data/nyt-text/articles_by_components.txt", "r") as ins:
    f = open('./data/nyt-text/articles_by_components1.txt','w')
    for line in ins:
        line = line.rstrip('\n')
        if len(line.split('\t')) >= 2:
            idold = line.split('\t')[0]
            comp = line.split('\t')[1]
            res = get_data.idSearch(idold)
            f.write(res+'\t'+comp+'\n')
    f.close()

