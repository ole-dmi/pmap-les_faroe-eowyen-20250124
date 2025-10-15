import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

input_dir = "/projappl/project_465000527/olindber/data/pmap-les/faroe_eowyn_20250124/output/500000x500000_251x251"

for i in range(0,90,10):
    filename = f"{input_dir}/data_{i}.nc"
    print(f"Opening ${filename} ...")
    ds       = xr.open_dataset(filename)
    u = ds['uvelx'].isel(time=0)[:,:,0]
    v = ds['uvely'].isel(time=0)[:,:,0]
    w = ds['uvelz'].isel(time=0)[:,:,0]

    vel = np.sqrt(u**2 + v**2 + w**2)

    plt.figure()
    plt.pcolormesh(vel)
    
    filename = f"{input_dir}/data_{i}.png"

    print(f"Saving ${filename} ...")
#    plt.savefig(filename)
#    plt.figure()
#    plt.pcolormesh(uvelx[:,51,:])

plt.show()
