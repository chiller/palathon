import base64
import json

from flask import Flask, send_from_directory, Response, request, render_template
from rtree import index
import os


def init_index(name='3d_real_objects'):
    p = index.Property()
    p.dimension = 3
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    return index.Index(name, properties=p)

idx3d = init_index()


def query(query, num=5, distance=20):
    query_box = (
        query[0] - distance,
        query[1] - distance,
        query[2] - distance,
        query[0] + distance,
        query[1] + distance,
        query[2] + distance
    )
    return [i.object for i in idx3d.nearest(query_box, num, objects=True)]


here = os.path.dirname(__file__)
app = Flask(__name__, static_url_path=here)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route("/", methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        image = request.files['image']
        content = image.stream.read()
        uploaded = base64.b64encode(content).decode("utf-8")
        return render_template('index.html', uploaded=uploaded)
    return render_template('index.html')


@app.route('/colors/<int:num>/<int:r>/<int:g>/<int:b>')
def show_post(num, r, g, b):
    result = query((r, g, b), num)
    return Response(json.dumps(result),  mimetype='application/json')

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
