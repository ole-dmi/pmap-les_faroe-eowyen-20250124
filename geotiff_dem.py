import rasterio
import numpy as np  

class GeoTiffDEM:
    # Geotiff origin is north,west
    # Pixel order is north->south,west->east
    # Coordinates in wsg84 aka lat,lon
    def __init__(self,filename):
        

        with rasterio.open(filename) as src:
            
            self.dem         = src.read(1)
            self.bounds      = src.bounds
            self.transform   = src.transform
            self.crs         = src.crs
            self.width       = src.width
            self.height      = src.height

            i        = np.arange(self.dem.shape[0])
            j        = np.arange(self.dem.shape[1])
            self.lat = (i+0.5) * self.transform.e + self.transform.f
            self.lon = (j+0.5) * self.transform.a + self.transform.c

    def info(self):

        print(f"CRS       : {self.crs}")
        print(f"Extent    : {self.bounds}")
        print(f"shape     : {self.dem.shape}")
        print(f"size      : {self.width}, {self.height}")
        print(f"transform : {self.transform}")
        
        print(self.transform.a,self.transform.b,self.transform.c)
        print(self.transform.d,self.transform.e,self.transform.f)
        print(self.transform.g,self.transform.h,self.transform.i)