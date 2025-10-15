import xarray as xr
import matplotlib.pyplot as plt
import numpy as np


for i in range(5):
    ds = xr.open_dataset(f"data_{i}.nc")
    print(ds['uvelx'])
    uvelx = ds['uvelx'].isel(time=0)
    plt.figure()
    plt.pcolormesh(uvelx[:,:,0])

    plt.figure()
    plt.pcolormesh(uvelx[:,51,:])

plt.show()
