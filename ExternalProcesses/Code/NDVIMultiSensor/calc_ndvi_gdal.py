from osgeo import gdal
from osgeo import osr
import numpy as np
import sys
import zipfile
import uuid
import os
import shutil

def calcNDVIProbav(hdf_file, path):

    print("Proba-V file detected: " + hdf_file)
    hdf_ds = gdal.Open(hdf_file, gdal.GA_ReadOnly)

   
    # en cas d'inversion utiliser -resy dans la transform et utiliser botly a la place de toply
    toplx = float(hdf_ds.GetMetadata()["TOP_LEFT_LONGITUDE"])
    toply = float(hdf_ds.GetMetadata()["TOP_LEFT_LATITUDE"])
    
    toprx = float(hdf_ds.GetMetadata()["TOP_RIGHT_LONGITUDE"])
    botly = float(hdf_ds.GetMetadata()["BOTTOM_LEFT_LATITUDE"])
   
    r = None
    n = None

    for name in hdf_ds.GetSubDatasets():
        if (name[0].find("//LEVEL1C/RED") != -1):
            r = name[0]
        if (name[0].find("//LEVEL1C/NIR") != -1):
            n = name[0]
	
    # memory save purpose
    hdf_ds = None

    red = gdal.Open(r, gdal.GA_ReadOnly)
    nir = gdal.Open(n, gdal.GA_ReadOnly)

    print("calculating NDVI.")
    b3 = red.ReadAsArray().astype(np.float32)
    b4 = nir.ReadAsArray().astype(np.float32)

    ndvi = (b4 - b3)/(b4 + b3)


    resx = (toprx - toplx) / red.RasterXSize
    resy = (botly - toply) / red.RasterYSize



    print("creating NDVI File: " + path + ".tif" + '(resx=' + str(resx) + ' resy=' + str(resy) + ')');
    drv = gdal.GetDriverByName ( "GTiff" )
    dst_ds = drv.Create ( path + ".tif", red.RasterXSize, red.RasterYSize, 1, gdal.GDT_Float32, options=["COMPRESS=LZW"] )

    # Define the spatial information for the new image.
    geoProjection = osr.SpatialReference()
    geoProjection.SetWellKnownGeogCS("WGS84")
    dst_ds.SetProjection(str(geoProjection))

    geoTransform = [toplx, resx, 0.0, toply, 0.0, resy]
    dst_ds.SetGeoTransform(geoTransform)

    dst_ds.GetRasterBand(1).WriteArray ( ndvi.astype (np.float32) )
    print("Proba-V file " + hdf_file + " processed in " +  path + ".tif")
    
    # clean up memory (Not sure is usefull/necessary)
    dst_ds = None
    red    = None
    nir    = None
    ndvi   = None
    b3     = None
    b4     = None

def calcNDVISentinel2(zip_file, path):

    print("Sentinel-2 Zip file detected: " + zip_file)
    print("extracting: " + zip_file)

    zip_ref = zipfile.ZipFile(zip_file, 'r')
    zip_ref.extractall(path)
    zip_ref.close()

    red = None
    nir = None
    for root, dirs, files in os.walk(path):
        for name in files:
            filepath = root + os.sep + name

            if name.endswith(("B04.jp2")):
                red = filepath
            if name.endswith(("B08.jp2")):
                nir = filepath

    if red is None:
        print("Couldn't find *B04.jp2 file (red band)")
        sys.exit(0)
    if nir is None:
        print("Couldn't find *B08.jp2 file (red band)")
        sys.exit(0)

    r = gdal.Open (red)
    if r is None:
        print("Couldn't open " + red)
        sys.exit(0)
    n = gdal.Open (nir)
    if n is None:
        print("Couldn't open " + nir)
        sys.exit(0)

    print("calculating NDVI.")

    b3 = r.GetRasterBand(1).ReadAsArray().astype(np.float32)
    b4 = n.GetRasterBand(1).ReadAsArray().astype(np.float32)

    ndvi = (b4 - b3)/(b4 + b3)

     # Get the spatial information from the input file
    geoTransform = r.GetGeoTransform()
    geoProjection = r.GetProjection()

    print("creating NDVI File: " + path + ".tif")
    drv = gdal.GetDriverByName ( "GTiff" )
    dst_ds = drv.Create ( path + ".tif", r.RasterXSize, r.RasterYSize, 1, gdal.GDT_Float32, options=["COMPRESS=LZW"] )

    # Define the spatial information for the new image.
    dst_ds.SetGeoTransform(geoTransform)
    dst_ds.SetProjection(geoProjection)

    dst_ds.GetRasterBand(1).WriteArray ( ndvi.astype (np.float32) )
    print("removing temporary files")
    shutil.rmtree(path)

    print("Sentinel-2 Zip file " + zip_file + " processed in " +  path + ".tif")

    # clean up memory (Not sure is usefull/necessary)
    dst_ds = None
    red    = None
    nir    = None
    ndvi   = None
    b3     = None
    b4     = None

def calcNDVIDeimos(tif_file, path):

    print("Deimos file detected: " + tif_file)
    
    deimos = gdal.Open (tif_file)

    print("calculating NDVI.")

    b3 = deimos.GetRasterBand(3).ReadAsArray().astype(np.float32)
    b4 = deimos.GetRasterBand(4).ReadAsArray().astype(np.float32)

    ndvi = (b4 - b3)/(b4 + b3)

    print("creating NDVI File: " + path + ".tif")
    drv = gdal.GetDriverByName ( "GTiff" )
    dst_ds = drv.Create ( path + ".tif", deimos.RasterXSize, deimos.RasterYSize, 1, gdal.GDT_Float32, options=["COMPRESS=LZW"] )

 
    # Get the spatial information from the input file
#    geoTransform = deimos.GetGeoTransform()

    geoTransform = [-95.392312627064513, 5.2545917606984414e-05, 0.0, 29.176790479721699, 0.0, -2.263635176302332e-05]



#    geoProjection = deimos.GetProjection()
    geoProjection = osr.SpatialReference()
    geoProjection.SetWellKnownGeogCS("WGS84")


    # Define the spatial information for the new image.
    dst_ds.SetGeoTransform(geoTransform)
    dst_ds.SetProjection(str(geoProjection))

    dst_ds.GetRasterBand(1).WriteArray ( ndvi.astype (np.float32) )

    print("Deimos file " + tif_file + " processed in " +  path + ".tif")

    # clean up memory (Not sure is usefull/necessary)
    dst_ds = None
    deimos = None
    ndvi   = None
    b3     = None
    b4     = None

# iterating on input arguments
for x in sys.argv[1:]:
    path = str(uuid.uuid4())
    if x.endswith((".zip")):
        calcNDVISentinel2(x, path)
    elif x.endswith((".HDF5")):
        calcNDVIProbav(x, path)
    elif x.endswith((".tif")):
        calcNDVIDeimos(x, path)
    else:
        print("unexpexted file extenson:" + x);
