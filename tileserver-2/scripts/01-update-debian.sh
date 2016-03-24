set -euxo pipefail

echo "deb http://mirror.internode.on.net/pub/debian/ testing main" > /etc/apt/sources.list
echo "deb-src http://mirror.internode.on.net/pub/debian/ testing main" >> /etc/apt/sources.list

apt-get update
apt-get -y dist-upgrade
apt-get -y install git vim sudo postgresql-9.5-postgis-2.2 postgresql-contrib-9.5 build-essential screen axel htop mosh ethtool rsync golang

adduser osm --disabled-password || true