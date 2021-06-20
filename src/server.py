from flask.json import jsonify
from flask.wrappers import Request
import scraping
from flask import Flask, request
from flask_pymongo import PyMongo

MONGO_USER = 'mongouser'
MONGODB_PASSWORD = 'mongopass'
MONGO_INITDB_DATABASE = 'mongoscrape'

app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb://' + MONGO_USER + ':' + MONGODB_PASSWORD \
                            + '@mongo:27017/' + MONGO_INITDB_DATABASE

@app.route('/', methods=['GET', 'POST'])
def hello():
    return jsonify(scraping.main(request.get_json()['keywords']))

app.run(host='0.0.0.0', port=8080, debug=False)