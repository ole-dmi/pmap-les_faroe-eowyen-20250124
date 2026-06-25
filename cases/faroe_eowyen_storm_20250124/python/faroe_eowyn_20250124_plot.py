import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

input_dir = "/projappl/project_465000527/olindber/data/pmap-les/pmap-les_faroe-eowyen-20250124/output/500000x500000_251x251"
for i in range(0,94,1):
    filename = f"{input_dir}/data_{i}.nc"
    print(f"Opening ${filename} ...")
    ds       = xr.open_dataset(filename)
    
    print(ds)
    
    
    x = np.array(ds['xcr']).transpose()
    y = np.array(ds['ycr']).transpose()
    
    u = ds['uvelx'].isel(time=0)[:,:,0]
    v = ds['uvely'].isel(time=0)[:,:,0]
    w = ds['uvelz'].isel(time=0)[:,:,0]

    vel = np.sqrt(u**2 + v**2 + w**2)
    
    print(x.shape)
    print(y.shape)
    print(u.shape)
    print(v.shape)
    print(w.shape)
    plt.figure() 
    plt.contourf(x,y,vel,cmap="coolwarm",vmin=5,vmax=15,levels=11)
    plt.contour (x,y,vel,vmin=5,vmax=15,levels=11, colors="black",linewidths=0.1)
    
    filename = f"{input_dir}/data_{i}.png"

    print(f"Saving ${filename} ...")
    plt.savefig(filename)
#    plt.figure()
#    plt.pcolormesh(uvelx[:,51,:])

#plt.show()
