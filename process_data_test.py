from erddapy import ERDDAP
import json
import xarray
import netCDF4
import rioxarray
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

def main():
    datums = {'geo': 'EPSG:4326', 'proj': 'EPSG:9377'}

    # Connect to the NOAA Coastwatch server
    e = ERDDAP(
        server="https://coastwatch.noaa.gov/erddap",
        protocol="griddap",
    )
    # Choose the daily blended SST dataset
    e.dataset_id = "noaacwBLENDEDsstDaily"

    e.griddap_initialize()
    
    # Only use the SST data
    e.variables = ["analysed_sst"]

    # Set the bounds for the data
    # By default, this function retrieves the most recent data from the server, but you can also specify a time range
    bounds = {
        # "time>=": (datetime.now() - timedelta(days=7)).isoformat(), # Optional - get data from the last 7 days
        'latitude>=': -8,
        'latitude<=': 20,
        'latitude_step': 1, # This should be 1 unless you want to downscale the data
        'longitude>=': -90,
        'longitude<=': -60,
        'longitude_step': 1 # This should be 1 unless you want to downscale the data
        }
    e.constraints.update(bounds)
    
    # Convert the data to an xarray dataset
    ds = e.to_xarray()
    # Apply the correct CRS to the data
    ds.rio.write_crs("EPSG:4326", inplace=True)
    # Convert the temperature from Kelvin to Celsius
    ds['analysed_sst_degC'] = ds.analysed_sst - 273.15
    dt = np.datetime_as_string(ds.time.values[0], unit='D') # There should only be one value in the array

    # Create a PNG image of the celsius data
    ds.analysed_sst_degC.plot(cmap='jet', vmin=18, vmax=34)
    plt.title(f"Sea Surface Temperature (°C) {dt}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig(f"analysed_sst_{dt}.png")

    # Export the data to GeoTIFFs
    for datum, epsg in datums.items():
        for var in ds.data_vars:
            print(var)
            if datum == 'proj' and ds.rio.crs == "EPSG:4326":
                ds = ds.rio.reproject(epsg)
            ds[var].rio.to_raster(f"{var}_{dt}_{datum}.tif")    

if __name__ == '__main__':
    main()
