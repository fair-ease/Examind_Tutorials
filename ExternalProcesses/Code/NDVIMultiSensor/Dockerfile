FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
        software-properties-common

RUN add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable && \
    apt-get update && apt-get install -y \
	build-essential \
        gdal-bin \
        libgdal-dev \
	python-gdal



ADD calc_ndvi_gdal.py / 
ENTRYPOINT ["python", "/calc_ndvi_gdal.py"]
