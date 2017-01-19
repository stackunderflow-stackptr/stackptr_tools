cat > /tmp/imposm3-deploy.sh << EOF
	set -euxo pipefail
	cd ~
	~/go/bin/imposm3 import -mapping example-mapping.json -connection postgis://osm:osm@localhost/osm?prefix=planet_osm_ -cachedir imposm-cache -optimize
	~/go/bin/imposm3 import -mapping example-mapping.json -connection postgis://osm:osm@localhost/osm?prefix=planet_osm_ -cachedir imposm-cache -deployproduction
EOF

su osm -c "bash /tmp/imposm3-deploy.sh" 