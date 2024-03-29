const csvFilePath = './YT2.csv';

Papa.parse(csvFilePath, 
    {
    download: true,
    header: true,
    complete: function(results) 
    {
        var data = results.data.slice(0, 30); // Only consider the top 30 rows

        data.forEach(function (row) 
        {
            row.subscribers = parseFloat(row.subscribers);
            row.highest_yearly_earnings = parseFloat(row.highest_yearly_earnings);
        });

        var subscribersData = data.map(row => row.subscribers);
        var earningsData = data.map(row => row.highest_yearly_earnings);

        // Normalize earningsData to be between 0 and 1 for colorscale
        var normalizedEarnings = earningsData.map(value => (value - Math.min(...earningsData)) / (Math.max(...earningsData) - Math.min(...earningsData)));

        var trace = {
            type: "treemap",
            labels: data.map(row => row.Youtuber),
            parents: data.map(row => 'Root'),
            values: subscribersData,
            textinfo: "label+value",
            hoverinfo: 'label+value+percent parent+percent root',
            customdata: data.map(row => ({ subscribers: row.subscribers, income: row.highest_yearly_earnings })),
            texttemplate: "<b>%{label}</b><br>Subscribers: %{customdata.subscribers}<br>Highest Annual Income: $%{customdata.income}",
            marker: 
            {
                colors: normalizedEarnings,
                colorscale: 
                [
                    [0, 'rgb(0, 100, 0)'],  // Dark green
                    [1, 'rgb(144, 238, 144)']  // Light green
                ],
                // colorscale: 'Viridis',
                reversescale: true,
                colorbar: {
                    title: 'Highest Annual Income',
                    tickmode: 'array',
                    tickvals: [0, 0.25, 0.5, 0.75, 1],
                    ticktext: ['Min', '', '', '', 'Max'],
                }
            }
        };

        var layout = {
            margin: { l: 0, r: 0, b: 0, t: 0 },
            plot_bgcolor: "white",
            annotations: 
            [
                {
                    text: "Top 30 Youtubers: Subscribers & Earnings",
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
