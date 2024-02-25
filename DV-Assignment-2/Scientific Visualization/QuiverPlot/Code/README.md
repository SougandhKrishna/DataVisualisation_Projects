## Dependencies to install

1. Install ImageIO for running the gif based python files using pip

   ```bash
   pip install imageio
   ```

2. Install Cartopy using pip

   ```bash
   pip install Cartopy
   ```

3. Install Matplotlib, Pandas and Numpy using pip

   ```bash
   pip install numpy
   pip install pandas
   pip install matplotlib
   ```

4. To use the mp4 generation code, make sure you have the encoder installed. For our experiment we use the h264_videotoolbox encoding. This is part of the ffmpeg encoding package and can be installed by following the instruction [here](https://ffmpeg.org/download.html)

## Instruction to run

1. Once the dependencies are installed. One can run the code using:

   ```bash
   python <filename.py>
   ```

2. Following files are present for experiments mentioned in report:

   1. animate-quiver-sampling-gif.py: This file will generate a quiverplot gif by using the data from the Data folder.
   2. animate-streamline-gif.py: This file will generate a streamline gif by using data.
   3. animate-quiver-sampling.py: This file will generate a quiverplot .mp4 by using the data from the Data folder.
   4. animate-streamline.py: This file will generate a streamline .mp4 by using the data from the Data folder.

Comments are present in code wherever necessary to reproduce various results and try more new stuff.

The data folder consist of both Zonal and Meridional data present in their respective folders.
