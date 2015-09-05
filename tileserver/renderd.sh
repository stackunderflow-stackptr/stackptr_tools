sudo apt-get install libicu-dev python-dev libboost-system-dev libboost-filesystem-dev libboost-iostreams-dev libboost-thread-dev \
libboost-python-dev libboost-program-options-dev libboost-regex-dev libxml2 libxml2-dev libfreetype6 libfreetype6-dev \
libjpeg-dev libpng-dev libtiff-dev libltdl-dev libproj-dev libcairo2 libcairo2-dev python-cairo python-cairo-dev \
libcairomm-1.0-1 libcairomm-1.0-dev ttf-dejavu ttf-dejavu-core ttf-dejavu-extra ttf-unifont libgdal-dev python-gdal \
libsqlite3-dev python-nose libharfbuzz-dev 

git clone https://github.com/mapnik/mapnik.git
cd mapnik
./configure
make
sudo make install

apt-get -y install apache2 apache2-dev
git clone https://github.com/openstreetmap/mod_tile/
cd mod_tile
./autogen.sh
./configure
make


touch /var/lib/mod_tile/planet-import-complete
touch /var/lib/mod_tile/osm_tiles/planet-import-complete
touch /var/lib/mod_tile/osm_tiles/style1/planet-import-complete
touch /var/lib/mod_tile/osm_tiles_2x/planet-import-complete
touch /var/lib/mod_tile/osm_tiles_2x/style2/planet-import-complete

