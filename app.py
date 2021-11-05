import os
from flask import Flask, render_template, abort, url_for, json, jsonify, request, session
import json
from datetime import datetime
from elasticsearch import Elasticsearch
import logging
from flask_session import Session
import traceback

es = Elasticsearch()

app = Flask(__name__,template_folder='.')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# read file
with open('file.json', 'r') as myfile:
    data = myfile.read()

@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        now=int(datetime.now().strftime('%s'))
        if "startTime" not in session:
            session["startTime"]=now
        if "elapsedTime" not in session:
            session["elapsedTime"]=now
        session["elapsedTime"]=(int(now)-int(session["startTime"]))
        app.logger.debug('startTime='+str(session["startTime"]))
        app.logger.debug('elapsedTime='+str(session["elapsedTime"]))
        data=request.args.get('q')
        body = {
            "query": {
                "multi_match": {
                    "query": data,
                    "fields": ["*"]
                }
            },
        "fields":['adi1','adi2','sku','cevirmen','basim_tarihi','basim_yeri', 'sayfa_sayisi','yazar'],
        "_source": False,
	"size": 50,
        }
        
        res = es.search(index="kutuphane", body=body)
        #app.logger.debug(res)
        #return jsonify(res["hits"])
        return render_template('index.html', data=res["hits"])
    except Exception as e:
        app.logger.error(traceback.format_exc())
    return jsonify({"hits":[]})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
