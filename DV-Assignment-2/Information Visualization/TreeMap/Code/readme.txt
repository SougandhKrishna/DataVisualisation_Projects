I have written seperate .js files for different plots and just a single html file with all the .js scripts commented out.
So to view the plots, uncomment any one of the scripts and then open the html file.

If the HTML file is not opening, run the following commands in your terminal:
python3 -m http.server

You should get a message like this: Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...

Now open http://localhost:8000/ in your browser and you should be able to view the html file.

(Also note that the dataset in the same folder, else you have to write its relative path in .js file)