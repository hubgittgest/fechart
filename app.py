import sqlite3
from flask import Flask, request, render_template, jsonify
app = Flask(__name__)
def get_db():
    db = sqlite3.connect('mydb.db')
    db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    rv = cur.fetchall()
    db.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/render", methods=["GET"])
def render():
    return render_template("render.html")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/weather", methods=["GET"])
def weather():
    if request.method == "GET":
        res = query_db("SELECT * FROM weather")

    return jsonify(month=[x[0] for x in res],
                   evaporation=[x[1] for x in res],
                   precipitation=[x[2] for x in res])

@app.route('/map')
def map():
    return render_template('map.html')


if __name__ == "__main__":
    app.run(debug=True)