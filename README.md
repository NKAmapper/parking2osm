# parking2osm
Converts parking areas from Parkeringsregisteret to OSM.

Usage: <code>python3 parking2osm.py [output_filename.osm]</code>.

* Stores an OSM file in "parkeringsregisteret.osm" or given filename.
* An OSM file may also be retrieved from [the 'parking' folder](https://www.jottacloud.com/s/059f4e21889c60d4e4aaa64cc857322b134).
* Contains more than 5000 public parking facilities across Norway.
* Please incldue the *ref:pregister* tag to make updates to capacity etc. possible.

### References ###

* [Statens Vegvesen - Parkeringsregisteret](https://www.vegvesen.no/trafikkinformasjon/langs-veien/parkering/parkeringsregisteret/).
* [API for Parkeringsregisteret](https://parkreg-open.atlas.vegvesen.no/swagger-ui/index.html?configUrl=/v3/api-docs/swagger-config).
