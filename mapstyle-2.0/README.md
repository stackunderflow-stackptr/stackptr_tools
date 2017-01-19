# StackPtr 2.0 Map Style

The StackPtr 2.0 map style is based on the Lyrk OpenStreetMap style and parts of Smartrak's OpenStreetMap style, as well as a modified colour scheme, which in turn is based on the [OSM Bright Style](https://github.com/mapbox/osm-bright).

Key features include multi-language support - if there is a `name` and `name:en` that differ, the name is displayed as `name (name:en)`.

## Installation

The style is based on the imposm version of OSM Bright, thus it needs [imposm3](https://github.com/omniscale/imposm3) for importing the data. The mapping file for imposm is located under `imposm/mapping.json`. The database can be imported by running `imposm3 import -read germany-latest.osm.pbf -write -mapping imposm/mapping.json -connection postgis://localhost/osm_imposm -deployproduction`.

The mapnik.xml can be generated using [magnacarto](https://github.com/omniscale/magnacarto) or [kosmtik](https://github.com/kosmtik/kosmtik/).

### Magnacarto

The paths to the `shape` and `font` directory have to be set to the project path inside the magnacarto configuration. The XML output path has to be set to the project path or you will have problems reading the GeoJSON files.


### Kosmtik

In the `localconfig.json` a rule has to be added in order to be able to read the raster files.

	{
		"where": "Layer",
		"if": {
			"geometry": "raster"
		},
		"then": {
			"Datasource.type": "raster"
		}
	}

### Shape Files

The following files need to be downloaded and stored inside the `shape` directory:

* http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_boundary_lines_land.zip
* http://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_0_countries.zip
* http://data.openstreetmapdata.com/simplified-land-polygons-complete-3857.zip
* http://data.openstreetmapdata.com/land-polygons-split-3857.zip

### Raster Files

Optional: hillshanding and areal imagery can be added for nicer colors. Those files need to be stored inside the `raster` directory.

* [Our improved True Marble Data](https://github.com/lyrk/true-marble-edit)
* **TODO** Hillshading TIFF
