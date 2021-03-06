cat > /tmp/postgres.sh << EOF
	set -uxo pipefail
	cd ~
	createuser --no-superuser --createdb osm
	createdb -E UTF8 -O osm osm
	psql -d osm -c "CREATE EXTENSION postgis;"
	psql -d osm -c "CREATE EXTENSION hstore;"
	echo "ALTER USER osm WITH PASSWORD 'osm';" | psql -d osm
EOF

su postgres -c "bash /tmp/postgres.sh" 