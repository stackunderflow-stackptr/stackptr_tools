cat > /tmp/imposm3-import.sh << EOF
	set -euxo pipefail
	cd ~
	~/go/bin/imposm3 import -mapping example-mapping.json -write -connection postgis://osm:osm@localhost/osm?prefix=planet_osm_ -cachedir imposm-cache -diff
EOF

su osm -c "bash /tmp/imposm3-import.sh || read -p 'press enter...'" 