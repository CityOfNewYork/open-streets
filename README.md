# open street functions

## open_street_node (intersection)

<pre>
https://nycmap.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_node('<b><i>node_id</i></b>')
</pre>

#### arguments
  * **_node_id_** (text) 7 digit number left 0 padded 

#### geoclient intersection

##### request
LUDLOW STREET AND RIVINGTON STREET, MANHATTAN
<pre>
<a href="https://maps.nyc.gov/geoclient/v1/intersection.json?app_key=5AFBAC9D639EA01D6&app_id=covid-testing&crossStreetOne=LUDLOW%20STREET&crossStreetTwo=RIVINGTON%20STREET&borough=MANHATTAN">https://maps.nyc.gov/geoclient/v1/intersection.json?app_key=5AFBAC9D639EA01D6&app_id=covid-testing&crossStreetOne=<b><i>LUDLOW</i></b>%20<b><i>STREET</i></b>&crossStreetTwo=<b><i>RIVINGTON</i></b>%20<b><i>STREET</i></b>&borough=<b><i>MANHATTAN</i></b></a>
</pre>

##### response
```
{
  ...
  "lionNodeNumber": "0020769",
  ...
}
```

#### example
<pre><a href="https://nycmap.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_node('0020769')">https://nycmap.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_node('<b><i>0020769</i></b>')</a></pre>

## open_street_segment (address, blockface)

<pre>
https://nycmap.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_segment('<b><i>segment_id</i></b>')
</pre>

#### arguments
  * **_segment_id_** (text) 7 digit number left 0 padded 

#### geoclient address

##### request
117 LUDLOW STREET, MANHATTAN
<pre>
<a href="https://maps.nyc.gov/geoclient/v1/address.json?app_key=5AFBAC9D639EA01D6&app_id=covid-testing&houseNumber=117&street=LUDLOW%20STREET&borough=MANHATTAN">https://maps.nyc.gov/geoclient/v1/intersection.json?app_key=5AFBAC9D639EA01D6&app_id=covid-testing&houseNumber=<b><i>117</i></b>&street=<b><i>LUDLOW</i></b>%20<b><i>STREET</i></b>&borough=<b><i>MANHATTAN</i></b></a>
</pre>

##### response
```
{
  ...
  "segmentIdentifier": "0164354",
  ...
}
```

#### example
<pre><a href="https://nycmap.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_segment('0164354')
">https://nycmap.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_segment('<b><i>0164354</i></b>')</a></pre>

#### geoclient blockface

##### request
LUDLOW STREET BETWEEN DELANCEY STREET AND RIVINGTON STREET, MANHATTAN
<pre>
<a href="https://maps.nyc.gov/geoclient/v1/blockface.json?app_key=74DF5DB1D7320A9A2&app_id=nyc-lib-example&onStreet=LUDLOW%20STREET&crossStreetOne=DELANCY%20STREET&crossStreetTwo=RIVINGTON%20STREET&borough=MANHATTAN">https://maps.nyc.gov/geoclient/v1/blockface.json?app_key=74DF5DB1D7320A9A2&app_id=nyc-lib-example&onStreet=<b><i>LUDLOW%20STREET</i></b>&crossStreetOne=<b><i>DELANCY%20STREET</i></b>&crossStreetTwo=<b><i>RIVINGTON%20STREET</i></b>&borough=<b><i>MANHATTAN</i></b></a>
</pre>

##### response
```
{
  ...
  "segmentIdentifier": "0164353",
  ...
}
```

#### example
<pre><a href="https://nycmap.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_segment('0164353')">https://nycmap.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_segment('<b><i>0164353</i></b>')</a></pre>

## open_street_radius (any location)

<pre>
https://nycmap.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_radius(<b><i>x</i></b>,<b><i>y</i></b>,<b><i>radius_feet</i></b>)
</pre>

#### arguments
  * **_x_** (number) X ordinate of EPSG:2263 coordinate
  * **_y_** (number) Y ordinate of EPSG:2263 coordinate
  * **_radius_feet_**  (number) radial distance in feet 

#### example
<pre><a href="https://nycmap.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_radius(987296,201152,100)">https://nycmap.carto.com/api/v2/sql?q=SELECT%20*%20from%20open_street_radius(<b><i>987296</i></b>,<b><i>201152</i></b>,<b><i>100</i></b>)</a></pre>
