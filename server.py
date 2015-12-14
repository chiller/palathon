import json
from flask import Flask, request, send_from_directory, Response
from rtree import index
import os

def init_index(name='3d_real_objects'):
    p = index.Property()
    p.dimension = 3
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    return index.Index(name, properties=p)

idx3d = init_index()

# API nearest

def query(query, num=5, distance=20):
    query_box = (
        query[0]-distance,
        query[1]-distance,
        query[2]-distance,
        query[0]+distance,
        query[1]+distance,
        query[2]+distance
    )
    # return [i for i in idx3d.intersection(query_box)]
    return [i.object for i in idx3d.nearest(query_box, num, objects=True)]


here = os.path.dirname(__file__)
app = Flask(__name__, static_url_path=here)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route("/")
def hello():
    return app.send_static_file('index.html')

@app.route('/colors/<int:num>/<int:r>/<int:g>/<int:b>')
def show_post(num, r, g, b):
    result = query((r, g, b), num)
    return Response(json.dumps(result),  mimetype='application/json')

if __name__ == "__main__":
    app.debug = True
    app.run()
