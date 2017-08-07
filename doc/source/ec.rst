Entity catalog
==============

Command line end point for entity catalog

Usage
-----

python -m nordlys.services.ec  -o <operation> -i <input>


Examples
--------

  - python -m nordlys.services.ec  -o lookup_id -i <dbpedia:Audi_A4>
  - python -m nordlys.services.ec  -o "lookup_sf_dbpedia" -i "audi a4"
  - python -m nordlys.services.ec  -o "lookup_sf_facc" -i "audi a4"
  - python -m nordlys.services.ec  -o "dbpedia2freebase" -i "<dbpedia:Audi_A4>"
  - python -m nordlys.services.ec  -o "freebase2dbpedia" -i "<fb:m.030qmx>"


:Author: Faegheh Hasibi
