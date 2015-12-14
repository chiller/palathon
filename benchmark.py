from rtree import index


db = {}


def generate_colors(rebuild=True):

    cid = 1
    for i in xrange(0, 255, 16):
        for j in xrange(0, 255, 16):
            for k in xrange(0, 255, 16):
                db[cid] = str( (i,j,k) )
                if rebuild:
                    idx3d.insert(cid, (i,j,k,i,j,k))
                cid = cid + 1


def init_index(name='3d_index'):
    p = index.Property()
    p.dimension = 3
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    return index.Index(name, properties=p)

idx3d = init_index()
generate_colors(rebuild=True)

# API nearest

def query(coordinate, distance=20):
    query = (148, 100, 211)
    query_box = (
        query[0]-distance,
        query[1]-distance,
        query[2]-distance,
        query[0]+distance,
        query[1]+distance,
        query[2]+distance
    )
    return [db[i] for i in idx3d.intersection(query_box)]

print query((150,150,150), 20)
