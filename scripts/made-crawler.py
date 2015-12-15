import argparse
import csv
from urllib import urlretrieve
from os import path, makedirs
import logging

from PIL import Image
from colorific import palette

TMP_DIR = '/tmp/palathon'
CACHE_PATH = '{0}/cache'.format(TMP_DIR)
RESULT_PATH = '{0}/result'.format(TMP_DIR)


def info_msg(msg):
    logging.log(logging.INFO, msg)


def debug_msg(msg):
    logging.log(logging.DEBUG, msg)


def error_msg(msg):
    logging.log(logging.ERR, msg)


def create_directories():
    for dir_path in [CACHE_PATH, RESULT_PATH]:
        if not path.exists(dir_path):
            makedirs(dir_path)


def get_product_filename(prod, check_file_exists=False):
    filename = '{0}/{1}.jpg'.format(CACHE_PATH, prod['sku'])
    if not path.isfile(filename) and check_file_exists:
        return None

    return filename


def transform_image_to_rgba(filename):
    debug_msg('Making product image {0} transparent'.format(filename))

    try:
        img = Image.open(filename)
    except IOError:
        error_msg('Invalid image file: {0}'.format(filename))
        return None

    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    new_filename = '{0}.png'.format(filename)
    img.save(new_filename, "PNG")

    return new_filename

def colour_file_already_saved(filename):
    if hasattr(colour_file_already_saved, 'ignore_cache'):
        return False

    return path.isfile(filename)


def read_csv_file(data_filename):
    data = []
    with open(data_filename, 'rb') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            data.append(row)
    info_msg('Total number of produds found in the CSV: {0}'.format(len(data)))
    return data


def save_csv_file(data):
    fields = data[0].keys()
    filename = '{0}/products_with_colours.csv'.format(RESULT_PATH)
    info_msg('Saving file: {0}'.format(filename))
    with open(filename, 'wb') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields ,delimiter='|')
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    return filename


def get_all_colour_images(product_data, image_column):
    info_msg("CSV column used {0}".format(image_column))
    info_msg("Getting all colour images")
    total_products = len(product_data)
    for index, data in enumerate(product_data):
        filename = get_product_filename(data)
        if filename is None:
            continue

        if colour_file_already_saved(filename):
            continue

        info_msg("[{0}/{1}] Downloading colour picture for product {2}".format(index,total_products,data['sku']))
        image_url = data[image_column]

        if 'productno_selection' in image_url:
            continue

        try:
            urlretrieve(data[image_column], filename)
        except Exception:
            error_msg("Colour image for product {0} not found".format(data['sku']))


def attach_colour_to_product(product_data, using_gallery_img):
    info_msg("Attaching colours to products")
    total_products = len(product_data)
    for index, data in enumerate(product_data):
        info_msg("[{0}/{1}]Extracting colours for product {2}".format(
            index,
            total_products,
            data['sku'])
        )
        product_filename = get_product_filename(data, check_file_exists=True)
        if product_filename is None:
            continue

        if using_gallery_img:
            product_filename = transform_image_to_rgba(product_filename)

        if product_filename is None:
            continue

        colours_found = palette.extract_colors(product_filename)

        bg_colour = colours_found.bgcolor
        if bg_colour:
            data['background'] = (bg_colour.value, bg_colour.prominence)
        else:
            data['background'] = None

        data['colours'] = [
            (c.value, c.prominence)
            for c in colours_found.colors
        ]


def main(args):
    print "Starting the process"
    csv_file = args.csv_file
    image_column = args.image_column
    create_directories()
    data = read_csv_file(csv_file)
    get_all_colour_images(data, image_column)
    using_gallery_img = image_column == 'gallery_img'
    attach_colour_to_product(data, using_gallery_img)
    result_file = save_csv_file(data)
    print "Results saved: {0}".format(result_file)


def parse_parameters():
    parser = argparse.ArgumentParser(description='Process image colours.')
    parser.add_argument('--ignore-cache', dest='ignore_cache', action='store_true', default=False)
    parser.add_argument('-d', action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.WARNING)
    parser.add_argument('-v', action="store_const", dest="loglevel", const=logging.INFO)
    parser.add_argument('--use-gallery-img', action="store_const", dest="image_column", const='gallery_img', default='colour_img')
    parser.add_argument('csv_file', nargs='?')
    parsed, _ = parser.parse_known_args()

    if parsed.ignore_cache:
        debug_msg("Ignoring Cache..")
        colour_file_already_saved.ignore_cache = True

    logging.basicConfig(level=parsed.loglevel)

    return parsed

if __name__ == '__main__':
    args = parse_parameters()
    main(args)
