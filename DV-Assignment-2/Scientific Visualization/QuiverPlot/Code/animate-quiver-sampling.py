import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from utils import process, slice_data
import cartopy.crs as ccrs
from matplotlib import rcParams
import matplotlib.animation as animation


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
frame = 0


def update(frame, sampling_technique="full"):
    print("Processing file " + dates[frame])
    metadata, longitude, latitude, meridonial_values = process(
        filepath="Data/Meridonial/" + dates[frame] + ".txt"
    )
    _, _, _, zonal_values = process(filepath="Data/Zonal/" + dates[frame] + ".txt")

    u_values = zonal_values
    v_values = meridonial_values
    lon_grid, lat_grid = np.meshgrid(longitude, latitude)

    # change for sampling rate for subsampling
    sub_samp_val = 2
    # sampling code block
    if sampling_technique == "full":
        x, y = lon_grid, lat_grid
        u, v = u_values, v_values
    elif sampling_technique == "subsample":
        x, y = (
            lon_grid[::sub_samp_val, ::sub_samp_val],
            lat_grid[::sub_samp_val, ::sub_samp_val],
        )
        u, v = (
            u_values[::sub_samp_val, ::sub_samp_val],
            v_values[::sub_samp_val, ::sub_samp_val],
        )
    elif sampling_technique == "interp":
        x, y = np.linspace(min(longitude), max(longitude), 100), np.linspace(
            min(latitude), max(latitude), 100
        )
        x, y = np.meshgrid(x, y)
        u = griddata(
            (lon_grid.flatten(), lat_grid.flatten()),
            u_values.flatten(),
            (x, y),
            method="linear",
        )
        v = griddata(
            (lon_grid.flatten(), lat_grid.flatten()),
            v_values.flatten(),
            (x, y),
            method="linear",
        )
    else:
        raise ValueError("Invalid sampling technique")

    # plotting
    plt.clf()
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent(
        [lon_start, lon_end, lat_start, lat_end],
        crs=ccrs.PlateCarree(),
    )

    magnitude = np.sqrt(u**2 + v**2)
    norm = plt.Normalize(vmin=0, vmax=10)

    fig = plt.quiver(
        x,
        y,
        u,  # divide by /magnitude for same size arrows
        v,  # divide by /magnitude for same size arrows
        magnitude,  # comment for no cmap
        angles="uv",
        pivot="mid",
        scale=250,  # use 250 for reproducing results with arrow length varying. 45 for same size.
        scale_units="width",
        cmap="viridis",  # comment for no cmap
        norm=norm,  # comment for no cmap
    )
    ax.set_title(metadata["time"])
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.coastlines()
    ax.gridlines(draw_labels=True)

    # comment for no colormap
    plt.colorbar()
    return fig, ax


ffmpegwriter = animation.writers["ffmpeg"]
rcParams["animation.codec"] = "h264_videotoolbox"
writer = ffmpegwriter(fps=2)

fig = plt.figure(figsize=(14, 8))
with writer.saving(fig, "quiver_animation_widths.mp4", dpi=200):
    for i in range(len(dates)):
        update(i, "full")
        writer.grab_frame()
