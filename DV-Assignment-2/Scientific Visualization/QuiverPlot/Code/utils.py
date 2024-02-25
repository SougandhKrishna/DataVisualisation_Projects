import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
import numpy as np


def process(filepath: str):
    """
    Processes a ascii file with gridded data to obtain the required value in the form of [latitude, longitude, value.
        Args:
            filepath: str
        Returns:
            metadata: Dict
            values: List[List[float]]
    """
    metadata = {}
    longitudes = []
    values = []
    latitudes = []
    i = 0
    with open(filepath, "r") as file:
        for line in file:
            line = line.strip()
            if i == 0:
                metadata["varname"] = line.split(":")[1].strip()
            if i == 1:
                metadata["filename"] = line.split(":")[1].strip()
            if i == 2:
                pass
            if i == 3:
                metadata["badflag"] = line.split(":")[1].strip()
            if i == 4:
                metadata["subset"] = line.split(":")[1].strip()
            if i == 5:
                metadata["time"] = line.split(":")[1].strip()
            if i == 6:
                for l in line.split("\t"):
                    if l.strip()[-1] == "W":
                        longitudes.append(-1 * float(l.strip()[:-1]))
                    else:
                        longitudes.append(float(l.strip()[:-1]))
            if i > 6:
                t = line.split("\t")
                lat = t[0]
                if lat[-1] == "S":
                    latval = -1 * float(lat[:-1])
                else:
                    latval = float(lat[:-1])
                latitudes.append(latval)
                t = t[1:]
                tempvals = []
                for idx, val in enumerate(t):
                    if val == metadata["badflag"]:
                        tempvals.append(np.nan)
                    else:
                        tempvals.append(float(val))
                values.append(tempvals)
            i += 1
    return metadata, np.array(longitudes), np.array(latitudes), np.array(values)


def slice_data(
    longitudes: np.array,
    latitudes: np.array,
    data: np.array,
    lat_start: float,
    lat_end: float,
    lon_start: float,
    lon_end: float,
):
    """
    Returns slice of the dataset with coordinates and values in the defined range as per arguments.
    Args:
        longitudes: list[float] - longitudes
        latitudes: list[float] - latitudes
        data: list[any] - data array
        lat_start: float - starting latitude
        lat_end: float - ending latitude
        lon_start: float - starting longitude
        lon_end: float - ending longitude
    Returns:
        list[float] - the slice of the required lon
        list[float] - the slice of the required lat
        list[list[float]] - values of the slice
    """
    final_lon = []
    final_lat = []
    final_val = []
    for i in range(len(latitudes)):
        tempval = []
        flag = False
        for j in range(len(longitudes)):
            if (
                lat_start <= latitudes[i] <= lat_end
                and lon_start <= longitudes[j] <= lon_end
            ):
                flag = True
                tempval.append(data[i][j])
                if longitudes[j] not in final_lon:
                    final_lon.append(longitudes[j])
        if flag == True:
            final_val.append(tempval)
            final_lat.append(latitudes[i])

    return np.array(final_lon), np.array(final_lat), np.array(final_val)
