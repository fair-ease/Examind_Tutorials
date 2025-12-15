# Examind Tutorials 🗺️

This repository contains a list of tutorials on various Examind features.

If you have any questions, or if you want the latest docker image of Examind Community, please contact :
- ✉️ quentin.bialota@geomatys.com
- ✉️ dorian.ginane@geomatys.com
- ✉️ pascal.broglie@geomatys.com

---

### 📑 List of tutorials 
- 🌍 **OpenEO**
  - 📙 *OpenEO Jupyter Notebooks* :
    -  [Notebook with Http requests](./openEO/openeo_examind_http_example.ipynb)
    -  [Notebook with the OpenEO web editor](./openEO/openeo_examind_web_editor_example.ipynb)
    -  [Notebook with the python client](./openEO/openeo_examind_python_client_example.ipynb)
  - 📋 *Import data* -> [How to import my data in examind ?](./openEO/import_data.md)
  - 📋 *Retrieve data Id & service Id* -> [How do you retrieve the id of the data you want to use ?](./openEO/retrieve_data_id.md)


- **Run external process via CWL** *(Expose external processes through WPS, Processes, OpenEO using Common Workflow Language)*
  - 📋 *Pre-configuration of Examind if you use Podman Rootless* -> [Podman Rootless Conf](./ExternalProcesses/podman_rootless.md)
  - 📋 *Configuration of Examind (any cases)* -> [Examind Conf](./ExternalProcesses/examind_conf_cwl.md)
  - 📙 *Tutorial with dockerized NDVI process (Jupyter Notebook)* -> [Dockerized NDVI process tutorial with CWL](./ExternalProcesses/cwl_dockerized_ndvi.ipynb)
  - 📙 *Tutorial for External STAC management (Juypyter Notebook)* -> [Dockerized External Stac tutorial with CWL](./ExternalProcesses/cwl_stac_downloader.ipynb)


- **Galaxy Workflows through WPS**
  - 📙 *Example (Jupyter Notebook)* -> [Jupyter notebook with some WPS requests for Galaxy workflows](./GalaxyWPS/galaxy_workflows_wps.ipynb)
  - 📄 *Tutorial (PDF)* -> [Deploy and use Galaxy Workflows with Examind WPS](./GalaxyWPS/Deploy%20and%20Use%20Galaxy%20Workflow%20With%20Exa%20WPS.pdf)


- **Time Data Aggregation**
  - 📄 *Tutorial (PDF)* -> [Importing geotiff time series data into Examind Community](./TimeDataAggregation/Importing%20geotiff%20time%20series%20data%20into%20Examind%20Community.pdf)
  - 📼 *Video (Italy Soil data aggregation through S3)* -> [Access link](https://nextcloud.geomatys.com/s/jQi6aj2iXXDFkKG)


- **Setup WMS, and visualisation in Terriamap**
  - 📋 *Import data* -> [How to import my data in examind ?](./wms-terriamap/import_data.md)
  - 📋 *Style data* -> [How to set a style to my data in examind ?](./wms-terriamap/style_data.md)
  - 📋 *WMS setup* -> [WMS setup example](./wms-terriamap/wms_setup.md)
  - 📋 *Terriamap configuration for Examind WMS* -> [Terriamap configuration example](./wms-terriamap/terriamap_config.md)
  - 🐱 *Terriamap setup example* -> [FairEase Terriamap](https://github.com/fair-ease/terria-config)

---

You also have in this repository :
- A 🐋 [docker-compose](./docker-compose.yml) file (for examind-community) (**you need to import the docker image before**)
- A 📜 [run.sh](./run.sh) script (to run examind)
- A 📜 [stop.sh](./stop.sh) script (to stop examind)