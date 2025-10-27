from string import Template

import yaml
from config import load_config
from geotiff_dem import GeoTiffDEM
import matplotlib.pyplot as plt
import numpy as np
from pyproj import Transformer
from scipy.interpolate import RegularGridInterpolator
import logging
import sys
import argparse
from pathlib import Path
import xarray as xr

def main() -> int:

    logging.basicConfig(level=logging.INFO,format="[%(levelname)s] %(name)-24s %(message)s")
    logger = logging.getLogger(__name__)
    logger.info("Starting copernicus_dem_faroe_to_pmap.py ...")

    #---------------------------------------------------------------------#
    # Parse command line arguments:
    #---------------------------------------------------------------------#
    parser = argparse.ArgumentParser(
        description="Generate seabed surface and volume grids from input data."
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/config.yaml"),
        help="Path to the YAML configuration file (default: config/config.yaml)"
    )

    args = parser.parse_args()

    #---------------------------------------------------------------------#
    # Set up logging:
    #---------------------------------------------------------------------#
    logging.basicConfig(level=logging.INFO,format="[%(levelname)s] %(name)-24s %(message)s")
    logger = logging.getLogger(__name__)

    #---------------------------------------------------------------------#
    # Load configuration:
    #---------------------------------------------------------------------#
    logger.info(f"Loading configuration from {args.config} ...")
    cfg = load_config()

    #-----------------------------------------------------------------------------#
    # Load the 4 GeoTIFF DEM files covering the Faroe Islands
    #-----------------------------------------------------------------------------#
    logger.info("Loading GeoTIFF DEM files ...")
    geotiffdem = [[None,None],
                [None,None]]
    j = 0
    for lon in range(8, 6, -1):
        i = 0
        for lat in range(62, 60, -1):
            filename = f"{cfg.geotiff.input_path}/Copernicus_DSM_COG_10_N{lat:02d}_00_W{abs(lon):03d}_00_DEM.tif"
            print(f"Loading {filename} ...")
            geotiffdem[i][j]=GeoTiffDEM(filename)
            geotiffdem[i][j].info()
            i += 1
        j += 1

    #-----------------------------------------------------------------------------#
    # Combine the 4 GeoTIFF DEM files into a single DEM array
    #-----------------------------------------------------------------------------#
    nx = geotiffdem[0][0].height + geotiffdem[1][0].height
    ny = geotiffdem[0][0].width  + geotiffdem[0][1].width
    logger.info(f"Total grid size: {nx} x {ny}")

    dem = np.zeros((nx,ny), dtype=np.float32)
    dem[0:geotiffdem[0][0].height,   0:geotiffdem[0][0].width]    = geotiffdem[0][0].dem
    dem[  geotiffdem[1][0].height:nx,0:geotiffdem[1][0].width]    = geotiffdem[1][0].dem
    dem[0:geotiffdem[0][1].height,     geotiffdem[0][1].width:ny] = geotiffdem[0][1].dem
    dem[  geotiffdem[1][1].height:nx,  geotiffdem[1][1].width:ny] = geotiffdem[1][1].dem


    lat                               = np.zeros(nx, dtype=np.float32)
    lat[0:geotiffdem[0][0].height]    = geotiffdem[0][0].lat
    lat[  geotiffdem[1][0].height:nx] = geotiffdem[1][0].lat

    lon                               = np.zeros(ny, dtype=np.float32)
    lon[0:geotiffdem[0][0].width]     = geotiffdem[0][0].lon
    lon[  geotiffdem[0][1].width:ny]  = geotiffdem[0][1].lon

    # Note: the latitude array needs to be reversed because the GeoTIFF origin is top-left
    lat = lat[::-1]
    dem = dem[::-1,:]

    #-----------------------------------------------------------------------------#
    # Create an interpolator for the DEM in lat,lon
    #-----------------------------------------------------------------------------#
    logger.info("Creating interpolators ...")
    dem_interp = RegularGridInterpolator(
        (lat, lon),
        dem,   
        bounds_error=False,
        fill_value=0.0)

    #-----------------------------------------------------------------------------#
    # Now sample the DEM on a regular grid in the target projection: ED50 / UTM zone 29N
    #-----------------------------------------------------------------------------#
    # Note: that the following coordinates are in the target projection (ED50 / UTM zone 29N)
    # and NOT in lat,lon

    logger.info("Sampling DEM on target grid ...")
    num_cells = [101,251,501,1001,2501,5001]
    for nx,ny in zip(num_cells,num_cells):
        logger.info(f"  nx={nx} ny={ny}")

        # Faroe Islands approx center in ED50 / UTM zone 29N:
        x0 = cfg.netcdf.x0
        y0 = cfg.netcdf.y0
        Lx = cfg.netcdf.Lx
        Ly = cfg.netcdf.Ly

        dx = Lx/(nx-1)
        dy = Ly/(ny-1)

        xmin = x0 - Lx/2
        xmax = x0 + Lx/2
        ymin = y0 - Ly/2
        ymax = y0 + Ly/2

        logger.info(f"Area of interest (ED50 / UTM zone 29N):")
        logger.info(f"Center       : {x0}, {y0} m")
        logger.info(f"Size         : {Lx} x {Ly} m")
        logger.info(f"Grid         : {nx} x {ny} points")
        logger.info(f"x            : {xmin} to {xmax} m")
        logger.info(f"y            : {ymin} to {ymax} m")
        logger.info(f"Grid spacing : {dx} x {dy} m")

        xv1d = np.linspace(xmin, xmax, nx)
        yv1d = np.linspace(ymin, ymax, ny)


        xv, yv      = np.meshgrid(xv1d, yv1d)
        zv          = np.zeros((ny,nx), dtype=np.float32)
        transformer = Transformer.from_crs("ED50 / UTM zone 29N","EPSG:4326", always_xy=True)
        lon, lat    = transformer.transform(xv, yv)
        zv          = dem_interp((lat, lon))

        logger.info(f"Sampled DEM shape: {zv.shape}")

        #-----------------------------------------------------------------------------#
        # Save the DEM to a NetCDF file
        #-----------------------------------------------------------------------------#
        logger.info("Saving DEM to NetCDF file ...")
        # Create DataArray
        da = xr.DataArray(
            data=zv,
            dims=("y", "x"),
            coords={
                "x": (("y", "x"), xv),
                "y": (("y", "x"), yv),
            },
            name="orog"
            )

        with open("config/config.yaml") as f:
            cfg_netcdf = yaml.safe_load(f)["netcdf"]
            
        filename    = str(f"faroe_dem_{Lx}x{Ly}_{nx}x{ny}.nc")
        output_file = Path(cfg_netcdf["output_path"]) / filename

        output_file.parent.mkdir(parents=True, exist_ok=True)
        da.to_netcdf(path=output_file)
        logger.info(f"✅ Saved to {output_file}")

        #-----------------------------------------------------------------------------#
        # Plot the DEM
        # ----------------------------------------------------------------------------##
        logger.info("Plotting ...")            
        plt.pcolormesh(xv,yv,zv,cmap='terrain',vmin=-10,vmax=800)
        plt.colorbar(label='Elevation (m)')
        plt.title(f'Faroe Islands (ED50 / UTM zone 29N) nx={nx} ny={ny}')
        plt.xlabel('West-East (m)')
        plt.ylabel('South-North (m)')
        plt.axis('equal')  
        plt.savefig(output_file.with_suffix('.png'), dpi=300)

    return 0

if __name__ == '__main__':
    sys.exit(main()) 