# Examind Tutorials

This repository contains a list of tutorials on various Examind features.

If you have any questions, or if you want the latest docker image of Examind Community, please contact :
- quentin.bialota@geomatys.com
- dorian.ginane@geomatys.com

---

### List of tutorials 
- **OpenEO** -> [Jupyter notebook with openEO examples](./openEO/openeo_examind_example.ipynb)
  - *Import data* -> [How to import my data in examind ?](./openEO/import_data.md)
  - *Retrieve data Id* -> [How do you retrieve the id of the data you want to use ?](./openEO/retrieve_data_id.md)


- **Galaxy Workflows through WPS** -> [Jupyter notebook with some WPS requests for Galaxy workflows](./GalaxyWPS/galaxy_workflows_wps.ipynb)
  - *Tutorial (PDF)* -> [Deploy and use Galaxy Workflows with Examind WPS](./GalaxyWPS/Deploy%20and%20Use%20Galaxy%20Workflow%20With%20Exa%20WPS.pdf)


- **Time Data Aggregation**
  - *Tutorial (PDF)* -> [Importing geotiff time series data into Examind Community](./TimeDataAggregation/Importing%20geotiff%20time%20series%20data%20into%20Examind%20Community.pdf)
  - *Video (Italy Soil data aggregation through S3)* -> [Access link](https://nextcloud.geomatys.com/s/jQi6aj2iXXDFkKG)

---

You also have in this repository :
- A [docker-compose](./docker-compose.yml) file (for examind-community) (**you need to import the docker image before**)
- A [run.sh](./run.sh) script (to run examind)
- A [stop.sh](./stop.sh) script (to stop examind)