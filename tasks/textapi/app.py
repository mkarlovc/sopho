from flask import Flask
from data import get_data
import json

app = Flask(__name__)

@app.route('/api/rsr/<text>', methods=['GET'])
def search_rsr(text):
    index = get_data.loadIndexRsr()
    res = get_data.searchIndex(index, text)
    return json.dumps(res)

@app.route('/api/prj/<text>', methods=['GET'])
def search_prj(text):
    index = get_data.loadIndexPrj()
    res = get_data.searchIndex(index, text)
    return json.dumps(res)

@app.route('/api/org/<text>', methods=['GET'])
def search_org(text):
    index = get_data.loadIndexOrg()
    res = get_data.searchIndex(index, text)
    return json.dumps(res)

@app.route('/api/nyt/article/<text>', methods=['GET'])
def search_nyt(text):
    if (get_data.count_nyt()<50000):
        res = get_data.searchNytClusterId(text)
    else:
        res = {"info": "request limit"}
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

