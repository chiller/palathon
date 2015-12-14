import random
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


import ast

def init_index(name):
    p = index.Property()
    p.dimension = 3
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    return index.Index(name, properties=p)

idx3d = init_index(name="3d_real_objects")
f = open('./products_with_colours.csv')

for row in f:
    fields = row.split('|')
    if fields[0]!='sku':
        index = fields[2]
        colours = ast.literal_eval(fields[1])
        colour = (colours[0][0][0],colours[0][0][1],colours[0][0][2],
                  colours[0][0][0],colours[0][0][1],colours[0][0][2])
        product = {}
        product['sku'] = fields[0]
        product['gallery_img'] = fields[3]
        product['colour_img'] = fields[4]
        product['product_url'] = fields[5]
        idx3d.insert(
            int(index),
            colour,
            obj=product
        )


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

print query((200,0,0), 10)
