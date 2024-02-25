const csvFilePath = './YT2.csv';

Papa.parse(csvFilePath, 
{
    download: true,
    header: true,
    complete: function(results) 
    {
        var data = results.data.slice(0, 30); // Only consider the top 30

        var trace = 
        {
            type: "treemap",
            labels: data.map(row => row.Youtuber),
            parents: data.map(row => 'Root'),
            values: data.map(row => row.subscribers),
            textinfo: "label+value",
            marker: 
            {
                colorscale: 
                [
                    [0, 'rgb(0, 100, 0)'],  // Dark green
                    [1, 'rgb(144, 238, 144)']  // Light green
                ],
                // colorscale: 'Viridis',
                reversescale: true,
            }
        };

        var layout = 
        {
            margin: { l: 0, r: 0, b: 0, t: 0 },
            plot_bgcolor: "white",
            annotations: [
                {
                    text: "Top 30 Youtubers: Subscriber Wise",
                    font: {
                        size: 24,
                        color: "black"
                    },
                    showarrow: false,
                    xref: "paper",
                    yref: "paper",
                    x: 0.5, 
                    y: 1.015,
                    bgcolor: "white"
                }
            ]
            
        };

        Plotly.newPlot('treemapDiv', [trace], layout);
    }
});
