import ast

f = open('/Users/jon/Code/products_with_colours.csv')
for row in f:
    fields = row.split('|')
    if fields[0]!='sku':
        index = fields[2]
        colours = ast.literal_eval(fields[1])
        colour = (colours[0][0][0],colours[0][0][1],colours[0][0][2],
                  colours[0][0][0],colours[0][0][1],colours[0][0][2])
        product = {}
        product['sku'] = fields[0]
        product['colour_img'] = fields[4]
        product['product_url'] = fields[5]

    #rtree.insert(index, colour, product)

