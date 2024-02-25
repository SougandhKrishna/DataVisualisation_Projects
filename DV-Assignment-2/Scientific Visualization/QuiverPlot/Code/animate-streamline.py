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

dpi = 100

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
        # color=magnitude,
        # cmap="viridis",
        # norm=norm,
    )
    ax.set_title(metadata["time"])
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.coastlines()
    ax.gridlines(draw_labels=True)

    # plt.colorbar()
    return fig, ax


ffmpegwriter = animation.writers["ffmpeg"]
rcParams["animation.codec"] = "h264_videotoolbox"
writer = ffmpegwriter(fps=2)

fig = plt.figure(figsize=(14, 8))
with writer.saving(fig, "streamline_animation_wo_cmap.mp4", dpi=200):
    for i in range(len(dates)):
        update(i)
        writer.grab_frame()
