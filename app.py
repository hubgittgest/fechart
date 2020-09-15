import sqlite3
from flask import Flask, request, render_template, jsonify
import random
from pyecharts.charts import Scatter3D

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


def generate_3d_random_point():
    return [random.randint(0, 100),
            random.randint(0, 100),
            random.randint(0, 100)]

def scatter3d():
    data = [generate_3d_random_point() for _ in range(80)]
    range_color = [
        '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
        '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    scatter3D = Scatter3D()
    scatter3D.add("", data)
    return scatter3D


@app.route("/e3d", methods=["GET"])
def e3d():
    print("in e3d")
    s3d = scatter3d()
    return render_template('e3d.html',
                           myechart=s3d.render_embed())

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