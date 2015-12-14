from flask import Flask
from rtree import index


def init_index(name='3d_objects'):
    p = index.Property()
    p.dimension = 3
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    return index.Index(name, properties=p)

idx3d = init_index()

# API nearest

def query(query, distance=20):
    query_box = (
        query[0]-distance,
        query[1]-distance,
        query[2]-distance,
        query[0]+distance,
        query[1]+distance,
        query[2]+distance
    )
    # return [i for i in idx3d.intersection(query_box)]
    return [i.object for i in idx3d.nearest(query_box, 20, objects=True)]

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/colors/<int:distance>/<int:r>/<int:g>/<int:b>')
def show_post(distance, r, g, b):
    result = query((r, g, b), distance)
    return str([str(i) for i in result])

if __name__ == "__main__":
    app.debug = True
    app.run()