cd mod_tile
./configure
sudo make install

echo "LoadModule tile_module /usr/lib/apache2/modules/mod_tile.so" > /etc/apache2/mods-available/tile.load
a2enmod tile

cat > /etc/apache2/sites-available/000-default.conf << EOF
<VirtualHost *:80>
	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html
	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
	LoadTileConfigFile /usr/local/etc/renderd.conf
	ModTileRenderdSocketName /var/run/renderd/renderd.sock
	# Timeout before giving up for a tile to be rendered
	ModTileRequestTimeout 300
	# Timeout before giving up for a tile to be rendered that is otherwise missing
	ModTileMissingRequestTimeout 300
</VirtualHost>
EOF

cat > /usr/local/etc/renderd.conf << EOF
[renderd]
num_threads=4
tile_dir=/var/lib/mod_tile
stats_file=/var/run/renderd/renderd.stats

[mapnik]
plugins_dir=/usr/local/lib/mapnik/input
font_dir=/usr/share/fonts/truetype
font_dir_recurse=1

[style1]
URI=/osm_tiles/
TILEDIR=/var/lib/mod_tile/osm_tiles/
XML=/usr/share/OSMSmartrak/OSMStackPtr.xml
HOST=localhost
TILESIZE=256

[style2]
URI=/osm_tiles_2x/
TILEDIR=/var/lib/mod_tile/osm_tiles_2x/
XML=/usr/share/OSMSmartrak/OSMStackPtr.xml
HOST=localhost
TILESIZE=512
SCALE=2.0

[style3]
URI=/osm_tiles_cg/
TILEDIR=/var/lib/mod_tile/osm_tiles_cg/
XML=/usr/share/OSMSmartrak/OSMStackPtrCG.xml
HOST=localhost
TILESIZE=256

[style4]
URI=/osm_tiles_cg_2x/
TILEDIR=/var/lib/mod_tile/osm_tiles_cg_2x/
XML=/usr/share/OSMSmartrak/OSMStackPtrCG.xml
HOST=localhost
TILESIZE=512
SCALE=2.0

EOF

tar xvzf ~gm/backup/osmsmartrak.tgz
chown -R gm:gm /usr/share/osmsmartrak

mkdir -p /var/lib/mod_tile/osm_tiles/
mkdir /var/lib/mod_tile/osm_tiles_2x/
mkdir /var/lib/mod_tile/osm_tiles_cg/
mkdir /var/lib/mod_tile/osm_tiles_cg_2x/
chown -R gm:gm /var/lib/mod_tile/

sudo /etc/init.d/apache2 restart
ldconfig

mkdir /var/run/renderd/
chown gm:gm /var/run/renderd/

# install DIN fonts
sudo cp -R ~/din /usr/share/fonts/truetype/

#unifont?


# init scripts, register with systemd
#---
# start renderd

# pre-render tiles

# touch import done


