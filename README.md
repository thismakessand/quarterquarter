quarterquarter
==============

Break up square-ish polygons into quarters (4), quarter-quarters (16), or quarter-quarter-quarters (64).

quarters (``--operation q``):  
![quarters.png](quarters.png)  
quarter-quarters (``--operation qq``):  
![quarter_quarters.png](quarter_quarters.png)  
quarter-quarter-quarters (``--operation qqq``):  
![quarter_quarter_quarters.png](quarter_quarter_quarters.png)  

#### CLI usage:
```
docker build -t quarterquarter .
docker run -it quarterquarter --operation q --input_shp /path/to/shapefile.shp --output_shp /path/to/shapefile_to_create.shp
```

#### Limitations:
Only designed to be used on north-oriented polygons with 4 sides.
