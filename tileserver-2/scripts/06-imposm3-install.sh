cat > /tmp/imposm3-install.sh << EOF
	set -euxo pipefail
	cd ~
	rm example-mapping.json || true
	wget https://raw.githubusercontent.com/omniscale/imposm3/master/example-mapping.json
	rm -rf go || true
	mkdir go
	export GOPATH=~/go
	go get github.com/omniscale/imposm3
	go install github.com/omniscale/imposm3
EOF

su osm -c "bash /tmp/imposm3-install.sh"
read -p "press enter..."