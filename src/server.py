from flask.json import jsonify
import scraping
from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def scrape():
    data = scraping.main(
        elements = request.get_json()['keywords'],
        proxy = request.get_json().get('proxy') or None
    )
    return jsonify(data)

app.run(host='0.0.0.0', port=8080, debug=False)