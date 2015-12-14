import random
from flask import Flask
from rtree import index

def generate_colors(rebuild=True):
    for i in xrange(0, 255, 16):
        for j in xrange(0, 255, 16):
            for k in xrange(0, 255, 16):
                cid = 1000000*i + 1000*j + k
                if rebuild:
                    idx3d.insert(
                        cid,
                        (i,j,k,i,j,k),
                        obj={
                            "color": "rgb(%d, %d, %d)" % (i, j, k),
                            "name" : random.choice(["sofa","chair","desk"])
                        }
                    )


def init_index(name):
    p = index.Property()
    p.dimension = 3
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    return index.Index(name, properties=p)

idx3d = init_index(name="3d_objects")
generate_colors(rebuild=True)


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

print query((10,10,10),10)
