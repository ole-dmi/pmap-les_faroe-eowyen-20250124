import rasterio
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Transformer

print("Plotting Copernicus DEM for Faroe Islands ...")
print("TIF files are loaded in longitude/latitude (EPSG:4326) and transformed to ED50 / UTM zone 29N (EPSG:23029) ...")

transformer = Transformer.from_crs("EPSG:4326", "ED50 / UTM zone 29N", always_xy=True)

for lat in range(61, 63):
    for lon in range(7, 9):

        with rasterio.open(f"data/copernicus_dem_faroe/Copernicus_DSM_COG_10_N{lat:02d}_00_W{abs(lon):03d}_00_DEM.tif") as src:

            dem         = src.read(1)
            extent      = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top] 
            transform   = src.transform
            crs = src.crs
            print(f"File   : Copernicus_DSM_COG_10_N{lat:02d}_00_W{abs(lon):03d}_00_DEM.tif")
            print(f"CRS    : {crs}")
            print(f"Extent : {extent}")
            print(f"shape  : {dem.shape}")
            print(f"size   : {src.width}, {src.height}")
            print(f"transform: {transform}")
            print(transform.a,transform.b,transform.c)
            print(transform.d,transform.e,transform.f)
            print(transform.g,transform.h,transform.i)

            i        = np.arange(dem.shape[1])
            j        = np.arange(dem.shape[0])
            longitude      = i * transform.a + transform.c
            latitude      = j * transform.e + transform.f
            LON, LAT = np.meshgrid(longitude, latitude)
            X, Y     = transformer.transform(LON, LAT)
            
            plt.pcolormesh(X,Y,dem,cmap='terrain',vmin=-10,vmax=800)

plt.colorbar(label='Elevation (m)')
plt.title('Copernicus DEM - Faroe Islands (ED50 / UTM zone 29N)')
plt.xlabel('West-East (m)')
plt.ylabel('South-North (m)')
plt.axis('equal')  

print("Saving figure to data/copernicus_dem_faroe/copernicus_dem_faroe.png ...")
plt.savefig('data/copernicus_dem_faroe/copernicus_dem_faroe.png', dpi=300)
#plt.show()
