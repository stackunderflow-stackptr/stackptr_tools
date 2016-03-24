cat > /tmp/imposm3-read.sh << EOF
	set -euxo pipefail
	cd ~
	rm -rf imposm-cache || true
	mkdir imposm-cache
	~/go/bin/imposm3 import -mapping example-mapping.json -read *.osm.pbf -cachedir imposm-cache -diff
EOF

su osm -c "bash /tmp/imposm3-read.sh || read -p 'press enter...'" 