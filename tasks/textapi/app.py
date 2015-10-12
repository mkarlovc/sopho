from flask import Flask
from data import get_data
import json
import datetime

app = Flask(__name__)

@app.route('/api/nyt/reqcount', methods=['GET'])
def req_count():
    res = get_data.getReq()
    return json.dumps(res)

@app.route('/api/nyt/reqtotalcount', methods=['GET'])
def req_toal_count():
    out = {}
    res = get_data.getTotalReq()
    out["count"] = res
    return json.dumps(out)

@app.route('/api/nyt/article/<text>', methods=['GET'])
def search_nyt(text):
    now = datetime.datetime.now()
    key = str(now.year)+"-"+str(now.month)+"-"+str(now.day)

    current = 0
    if not get_data.reqcount.has_key(key):
        get_data.reqcount[key] = 0
    else:
        current = get_data.reqcount[key]

    if current < 100:
        res = get_data.searchNytClusterId(text)
        get_data.reqcount[key] = current + 1
        get_data.totalcount += 1
    else:
        res = {"info": "request limit 100"}
    
    return json.dumps(res)

@app.route('/api/nyt/articles/<text>', methods=['GET'])
def search_nyts(text):
    out = {}
    if get_data.count_nyt()<50000:
        res = get_data.searchNytClusterIds(text)
        out['articles'] = res
    else:
        out["info"] = "request limit"

    return json.dumps(out)

@app.route('/api/nyt/cache', methods=['GET'])
def cache_nyt():
    print "start cache"
    get_data.loadNytCluster()
    get_data.loadNytText()
    print "end cache"
    return json.dumps({})

@app.route('/api/nyt/count', methods=['GET'])
def count_nyt():
    count = get_data.count_nyt()
    out = {}
    out['count'] = count
    return json.dumps(count)

# Main
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=8080)

