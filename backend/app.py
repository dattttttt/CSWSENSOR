from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://host.docker.internal:27017/")
db = client['csw']
col = db['tohop_logs']

@app.route("/api/latest")
def latest():
    last = col.find_one(sort=[('_id', -1)])
    if last:
        return jsonify({"tohop": last['tohop'], "time": last['time']})
    return jsonify({"tohop": "-", "time": "-"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
