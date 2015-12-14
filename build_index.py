import random
from rtree import index
import csv

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


def read_csv_file(data_filename):
    data = []
    with open(data_filename, 'rb') as csv_file:
        reader = csv.DictReader(csv_file, delimiter='|')
        for row in reader:
            data.append(row)
    return data


data = read_csv_file('./products_with_colours_using_gallery_image.csv')
for row in data:

    try:
        colour = ast.literal_eval(row['colours'])
    except SyntaxError, e:
        print 'problem with colour for product ' + row['sku']
        pass
    colourxyz = colour[0][0]
    colourxyzxyz = list(colourxyz) + list(colourxyz)

    idx3d.insert(
        int(row['entity_id']),
        colourxyzxyz,
        obj=row
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
