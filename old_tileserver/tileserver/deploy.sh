#!/bin/bash
set -euxo pipefail

if [ $EUID -ne 0 ]
	then su -c "bash $0"
	exit
fi

apt-get -y remove rdnssd

echo "deb http://ftp.jp.debian.org/debian/ testing main" > /etc/apt/sources.list
echo "deb-src http://ftp.jp.debian.org/debian/ testing main" >> /etc/apt/sources.list

apt-get update
apt-get -y dist-upgrade
apt-get -y install git vim sudo postgresql-9.5-postgis-2.2 postgresql-contrib-9.5 build-essential screen libxml2-dev libz-dev libbz2-dev libgeos-dev libgeos++-dev libproj-dev postgresql-server-dev-9.5 libboost-dev autoconf libtool libexpat-dev libboost-system-dev libboost-filesystem-dev libboost-thread-dev lua5.2 liblua5.2-dev axel htop mosh ethtool
adduser gm sudo

# do only if
#git clone https://github.com/openstreetmap/osm2pgsql.git
# do only if compile not complete
#cd osm2pgsql
#./autogen.sh
#./configure
#make
#make install

cat > /tmp/postgres.sh << EOF
set -euxo pipefail
createuser gm
createdb -E UTF8 -O gm gis
psql -c "CREATE EXTENSION hstore;" -d gis
psql -c "CREATE EXTENSION postgis;" -d gis
EOF

su postgres -c "bash /tmp/postgres.sh"

cat > /tmp/download.sh << EOF
axel -n 32 http://ftp5.gwdg.de/pub/misc/openstreetmap/planet.openstreetmap.org/pbf/planet-latest.osm.pbf
EOF

# TCP tuning

sysctl -w net.core.wmem_max=12582912
sysctl -w net.core.rmem_max=12582912
sysctl -w net.ipv4.tcp_rmem='10240 87380 12582912'
sysctl -w net.ipv4.tcp_wmem='10240 87380 12582912'
sysctl -w net.ipv4.tcp_window_scaling=1
sysctl -w net.ipv4.tcp_timestamps=1
ethtool -K eth1 tso off
ifconfig eth1 mtu 1450

# postgresql adjustments

# start actual import?

# tileserver setup
