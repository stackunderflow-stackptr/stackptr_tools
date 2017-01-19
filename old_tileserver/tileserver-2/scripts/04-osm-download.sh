cat > /tmp/download.sh << EOF
	set -euxo pipefail
	cd ~
	axel -n 8 http://download.geofabrik.de/australia-oceania/australia-latest.osm.pbf
EOF

su osm -c "bash /tmp/download.sh" 