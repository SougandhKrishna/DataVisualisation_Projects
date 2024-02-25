import matplotlib.pyplot as plt
import numpy as np 
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
import glob
from PIL import Image

def get_mins(filepath:str):
    '''
    Processes a ascii file with gridded data to obtain the required value in the form of [latitude, longitude, value. 
        Args:
            filepath: str 
        Returns:  
            metadata: Dict
            values: List[List[float]]
    '''
    metadata = {}
    longitudes = []
    values = []
    sizes = []
    i = 0 
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if i == 0: metadata["varname"] = line.split(":")[1].strip()
            if i == 1: metadata["filename"] = line.split(":")[1].strip()
            if i == 2: pass 
            if i == 3: metadata["badflag"] = line.split(":")[1].strip()
            if i == 4: metadata["subset"] = line.split(":")[1].strip()
            if i == 5: metadata["time"] = line.split(":")[1].strip()
            if i == 6: 
                for idx, l in enumerate(line.split('\t')):
                    # if idx == min_of_max:
                    #     break
                    try:
                        if l.strip()=='** line too long **':
                            # longitudes.append(-1*float(l.strip()[:-1]))
                            continue
                        else:
                            longitudes.append(float(l.strip()[:-1]))
                    except Exception as e:
                        print(l)
                        print(e)
                    
            if i > 6:
                t = line.split('\t')
                lat = t[0]
                if(lat[-1]=='S'):
                    latval = -1*float(lat[:-1])
                else:
                    latval = float(lat[:-1])

                # print(t)
                t = t[1:]
                tempvals = []
                sizes.append(len(t))
            i+=1    
    return min(sizes), len(longitudes)

def process(filepath:str, min_of_max):
    '''
    Processes a ascii file with gridded data to obtain the required value in the form of [latitude, longitude, value. 
        Args:
            filepath: str 
        Returns:  
            metadata: Dict
            values: List[List[float]]
    '''
    metadata = {}
    longitudes = []
    values = []
    sizes = []
    i = 0 
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if i == 0: metadata["varname"] = line.split(":")[1].strip()
            if i == 1: metadata["filename"] = line.split(":")[1].strip()
            if i == 2: pass 
            if i == 3: metadata["badflag"] = line.split(":")[1].strip()
            if i == 4: metadata["subset"] = line.split(":")[1].strip()
            if i == 5: metadata["time"] = line.split(":")[1].strip()
            if i == 6: 
                for idx, l in enumerate(line.split('\t')):
                    if idx == min_of_max:
                        break
                    try:
                        if l.strip()=='** line too long **':
                            continue
                        else:
                            longitudes.append(float(l.strip()[:-1]))
                    except Exception as e:
                        print(l)
                        print(e)
                        raise e
                    
            if i > 6:
                t = line.split('\t')
                lat = t[0]
                if(lat[-1]=='S'):
                    latval = -1*float(lat[:-1])
                else:
                    latval = float(lat[:-1])

                t = t[1:]
                tempvals = []
                sizes.append(len(t))
                for idx, val in enumerate(t):
                    if idx == min_of_max:
                        break
                    if val.endswith('** line too long **'):
                        val = val.replace('** line too long **', '')
                        continue
                    try:
                        if(val==metadata["badflag"]):
                            tempvals = [longitudes[idx],latval,-1e34]
                        else:
                            tempvals = [longitudes[idx],latval,float(val)]
                        values.append(tempvals)
                    except Exception as e:
                        print()
                        print(idx)
                        print("Val", val)
                        print("t", t)
                        raise e
            i+=1    
    return metadata, values

min_sizes = []
min_of_max = -1
txt_files = glob.glob('Data/*.txt')
txt_files.sort()
for file_path in txt_files:
    min_sizes.append(min(get_mins(filepath=file_path)))
    
min_of_max = min(min_sizes)
print(min_of_max)
    
metadata_lst = []
data_lst = []
for file_path in txt_files:    
    metadata, data = process(filepath=file_path, min_of_max=min_of_max)
    
    metadata_lst.append(metadata)
    data_lst.append(data)

date_lst = [
    '01-01-2023',
    '11-01-2023',
    '21-01-2023',
    '01-02-2023',
    '11-02-2023',
    '21-02-2023',
    '01-03-2023',
    '11-03-2023',
    '21-03-2023',
]

for i, data in enumerate(data_lst):
    lons, lats, values = zip(*data)

    lats = np.array(lats)
    lons = np.array(lons)
    values = np.array(values)
    mask = (values < -10)
    values[mask] = -1e10

    projection = ccrs.PlateCarree()

    fig = plt.figure(figsize=(10, 6))

    fig, ax = plt.subplots(subplot_kw={'projection': projection})
    
    contour_values = range(-1, 32, 4)

    contour = ax.tricontourf(lons, lats, values, transform=projection, levels=contour_values, cmap='viridis')

    ax.coastlines()

    cbar = plt.colorbar(contour, ax=ax, shrink=0.7)
    cbar.set_label('Value')

    ax.set_title(f'Sea Surface Temperature {date_lst[i]}')
    
    contour.colorbar.ax.set_ylabel("Temperature Values in Celsius")

    plt.savefig(f'Images/{i+1}.png', dpi=600, bbox_inches='tight')
    plt.close()

def create_gif(image_paths, output_path, duration=250):
    images = []

    for path in image_paths:
        img = Image.open(path)
        images.append(img)

    images[0].save(output_path, save_all=True, append_images=images[1:], duration=duration, loop=0)

image_paths = glob.glob('Images/*.png')
output_path = "output.gif"
create_gif(image_paths, output_path)


