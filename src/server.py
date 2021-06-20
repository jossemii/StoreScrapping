from time import monotonic
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

mongo = PyMongo(app)

@app.route('/', methods=['GET', 'POST'])
def scrape():
    data = scraping.main(request.get_json()['keywords'])
    mongo.db.todos.insert_many(data)
    return jsonify(data)

@app.route('/', methods=['GET'])
def get_all_data():
    return jsonify(
        mongo.db.find()
    )

app.run(host='0.0.0.0', port=8080, debug=False)