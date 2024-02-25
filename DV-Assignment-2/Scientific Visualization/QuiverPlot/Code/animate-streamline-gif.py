import imageio
from matplotlib import rcParams
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from utils import process, slice_data
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER

lat_start = 0
lat_end = 20
lon_start = 68
lon_end = 100


dates = [
    "1-JAN-2013",
    "15-JAN-2013",
    "1-FEB-2013",
    "15-FEB-2013",
    "1-MAR-2013",
    "15-MAR-2013",
    "1-APR-2013",
]


def update(frame, dpi=100):
    print("Processing file " + dates[frame])
    metadata, longitude, latitude, meridonial_values = process(
        filepath="Data/Meridonial/" + dates[frame] + ".txt"
    )
    _, _, _, zonal_values = process(filepath="Data/Zonal/" + dates[frame] + ".txt")

    lon, lat = np.meshgrid(longitude, latitude)

    plt.clf()
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent(
        [lon_start, lon_end, lat_start, lat_end],
        crs=ccrs.PlateCarree(),
    )
    # slice_interval = 4
    # skip = slice(None, None, slice_interval)
    magnitude = np.sqrt(zonal_values**2 + meridonial_values**2)
    norm = plt.Normalize(vmin=0, vmax=10)

    fig = plt.streamplot(
        lon,
        lat,
        zonal_values,
        meridonial_values,
        color=magnitude,
        cmap="viridis",
        norm=norm,
    )
    ax.set_title(metadata["time"])
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.coastlines()
    ax.gridlines(draw_labels=True)

    plt.colorbar()
    return fig, ax


fig = plt.figure(figsize=(14, 8))

animation = animation.FuncAnimation(fig, update, frames=7, interval=7000)

frames = []
for i in range(len(dates)):
    update(i)
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype="uint8")
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    frames.append(image)

imageio.mimsave("animation.gif", frames, duration=250)
