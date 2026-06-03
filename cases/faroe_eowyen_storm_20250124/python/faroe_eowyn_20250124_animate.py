import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

fig, ax = plt.subplots()

#x = np.arange(0, 2*np.pi, 0.01)
#line, = ax.plot(x, np.sin(x))


def animate(i):
    ds = xr.open_dataset(f"output/500000x500000_251x251/data_{i}.nc")

    uvelx = ds['uvelx'].isel(time=0)
    plot = plt.pcolormesh(uvelx[:,:,0], vmin=15, vmax=25)

#    plt.figure()
#    plt.pcolormesh(uvelx[:,51,:])
#    line.set_ydata(np.sin(x + i / 50))  # update the data.
    print(i)
    return plot,


ani = animation.FuncAnimation(fig, animate, blit=True, frames=5)

# To save the animation, use e.g.
#
#ani.save("movie.mp4")
#
# or
#
writer = animation.FFMpegWriter(
     fps=1, metadata=dict(artist='Me'), bitrate=1800)
ani.save("movie.mp4", writer=writer)

plt.show()


asdf


for i in range(5):
    ds = xr.open_dataset(f"data_{i}.nc")

    uvelx = ds['uvelx'].isel(time=0)
    plt.figure()
    plt.pcolormesh(uvelx[:,:,0])

    plt.figure()
    plt.pcolormesh(uvelx[:,51,:])

plt.show()
