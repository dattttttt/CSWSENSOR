from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://mongo:27017/")
db = client["csw"]
door_col = db["door_logs"]

@app.route("/api/latest")
def latest_button():
    doc = db["tohop_logs"].find_one(sort=[('_id', -1)])
    if doc:
        return jsonify({"type": "button", "tohop": doc["tohop"], "time": doc["time"]})
    return jsonify({"type": "button", "tohop": "-", "time": "-"})

@app.route("/api/door")
def get_door():
    last = door_col.find_one(sort=[("_id", -1)])
    if last:
        return jsonify({
            "status": last.get("trang_thai", "-"),
            "time": last.get("time", "-"),
            "type": "door"
        })
    return jsonify({"status": "-", "time": "-", "type": "door"})

@app.route("/api/temp")
def latest_temp():
    doc = db["temp_logs"].find_one(sort=[('_id', -1)])
    if doc:
        return jsonify({
            "type": "temp",
            "temperature": doc["temperature"],
            "humidity": doc["humidity"],
            "time": doc["time"]
        })
    return jsonify({
        "type": "temp",
        "temperature": "-",
        "humidity": "-",
        "time": "-"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
