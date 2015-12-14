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
    return endex.Index(name, properties=p)

idx3d = init_index()
generate_colors(rebuild=False)

# API nearest

tolerance = 20
query = (148, 100, 211)
query_box = (
    query[0]-tolerance,
    query[1]-tolerance,
    query[2]-tolerance,
    query[0]+tolerance,
    query[1]+tolerance,
    query[2]+tolerance
)
print query
print [i for i in  idx3d.intersection( query_box)]


