# parking2osm
Converts parking areas from Parkeringsregisteret to OSM.

Usage: <code>python parking2osm.py [output_filename.osm]</code>.

* Stores an OSM file in "parkeringsregisteret.osm" or given filename.
* An OSM file may also be retrieved from [this folder](https://drive.google.com/drive/folders/1JkIIUxwNh9WZx4lzt7rmqCwa6G_p9MAB?usp=sharing).
* Contains approx. 3.300 public parking facilities across Norway.
* Please incldue the *ref:pregister* tag to make updates to capacity etc. possible.

### References ###

* [Statens Vegvesen - Parkeringsregisteret](https://www.vegvesen.no/parkeringsregisteret/).
* [API for Parkeringsregisteret](https://www.vegvesen.no/om+statens+vegvesen/om+organisasjonen/apne-data/parkeringsregisteret-api).
