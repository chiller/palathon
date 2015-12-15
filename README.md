# palathon

## Installing requirements

You need libspatialindex v1.7.1  to run the server

http://libspatialindex.github.io/

http://download.osgeo.org/libspatialindex/spatialindex-src-1.7.1.tar.gz

untar
./configure
make
make install

On Ubuntu linux this library was installed in /usr/local/lib and I had to add

`include /usr/local/lib`

to /etc/ld.so.conf and run `ldconfig` only after that was I able to run

pip install -r requirements.txt

## Building index

make sure you have a copy of products_with_colours_using_gallery_image.csv in the project folder and do

`python build_index.py`

## Running the server

`python server.py`
