from time import monotonic
from flask.json import jsonify
from flask.wrappers import Request
import scraping
from flask import Flask, request
from flask_pymongo import PyMongo

MONGO_USER = 'user'
MONGODB_PASSWORD = 'pass'
MONGO_INITDB_DATABASE = 'scrape'
MONGO_HOSTNAME = 'mongodb'

app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb://' + MONGO_USER + ':' + MONGODB_PASSWORD \
                            + '@'+MONGO_HOSTNAME+':27017/' + MONGO_INITDB_DATABASE

mongo = PyMongo(app)

@app.route('/', methods=['GET', 'POST'])
def scrape():
    data = scraping.main(
        elements = request.get_json()['keywords'],
        proxy = request.get_json().get('proxy') or None
    )
    try:
        mongo.db.todos.insert_many(data)
    except Exception as e:
        print('Exception with mongo '+ str(e))
    return jsonify(data)

@app.route('/all', methods=['GET'])
def get_all_data():
    return jsonify(
        mongo.db.find()
    )

app.run(host='0.0.0.0', port=8080, debug=False)