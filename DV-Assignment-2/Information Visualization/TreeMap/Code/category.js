const csvFilePath = './YT2.csv';

Papa.parse(csvFilePath, {
    download: true,
    header: true,
    skipEmptyLines: true,
    complete: function (results) {
        originalData = processData(results.data);
        createOuterTreemap(originalData, 'category');
    }
});

function processData(data) {
    return data.reduce((acc, row) => {
        const category = row['category'];
        if (category) {
            if (!acc[category]) {
                acc[category] = { YouTubers: {} };
            }

            const Youtuber = row['Youtuber'];
            acc[category].YouTubers[Youtuber] = {
                subscribers: parseFloat(row['subscribers']),
                video_views: parseFloat(row['video_views']),
                // Add other relevant data as needed
            };
        }
        return acc;
    }, {});
}

function createOuterTreemap(data, eventType) {
    const labels = Object.keys(data);
    const values = Object.values(data).map(item => Object.keys(item.YouTubers).length);

    const trace = {
        type: "treemap",
        labels: labels,
        parents: labels.map(() => ''),
        values: values,
        textinfo: "none",
        hoverinfo: 'label+value',
        texttemplate: "<b>%{label}</b><br>YouTubers Count: %{value}",
        marker: {
            reversescale: true,
            colors: values,
            colorscale: 'Viridis',
            colorbar: {
                title: 'YouTubers Count',
            }
        }
    };

    const layout = {
        margin: { l: 0, r: 0, b: 0, t: 50 },
        title: {
            text: `${eventType.charAt(0).toUpperCase() + eventType.slice(1)} Distribution`,
            font: { size: 24, family: "Arial" },
            x: 0.5,
            y: 0.98
        }
    };

    Plotly.newPlot('treemapDiv', [trace], layout);

    const backButton = document.getElementById('backButton');
    if (backButton) {
        backButton.style.display = eventType === 'category' ? 'none' : 'block';
    }

    currentData = data;
    currentEventType = eventType;

    treemapDiv.on('plotly_click', handleTreemapClick);
}

function createInnerTreemap(data, eventType) {
    const labels = Object.keys(data);
    const values = Object.values(data).map(item => item.subscribers);

    const trace = {
        type: "treemap",
        labels: labels,
        parents: labels.map(() => ''),
        values: values,
        textinfo: "none",
        hoverinfo: 'label+value',
        texttemplate: "<b>%{label}</b><br>Subscribers: %{value}",
        marker: {
            reversescale: true,
            colors: values,
            // colorscale: 'Viridis',
            colorscale: 
            [
                [0, 'rgb(0, 100, 0)'],  // Dark green
                [1, 'rgb(144, 238, 144)']  // Light green
            ],
            colorbar: {
                title: 'Subscribers Count',
            }
        }
    };

    const layout = {
        margin: { l: 0, r: 0, b: 0, t: 50 },
        title: {
            text: `${eventType.charAt(0).toUpperCase() + eventType.slice(1)} Distribution`,
            font: { size: 24, family: "Arial" },
            x: 0.5,
            y: 0.98
        }
    };

    Plotly.newPlot('treemapDiv', [trace], layout);

    const backButton = document.getElementById('backButton');
    if (backButton) {
        backButton.style.display = 'block';
    }

    currentData = data;
    currentEventType = eventType;

    treemapDiv.on('plotly_click', handleTreemapClick);
}

function handleTreemapClick(event) {
    if (event.points && event.points[0]) {
        const selectedLabel = event.points[0].label;
        const selectedData = currentData[selectedLabel];

        if (selectedData) {
            if (currentEventType === 'category') {
                createInnerTreemap(selectedData.YouTubers, 'Youtuber');
            }
        }
    }
}


function goBack() {
    if (currentEventType === 'Youtuber') {
        createOuterTreemap(originalData, 'category');
    } else {
        const backButton = document.getElementById('backButton');
        if (backButton) {
            backButton.style.display = currentEventType === 'category' ? 'none' : 'block';
        }

        currentData = originalData;
        currentEventType = 'category';
        createOuterTreemap(originalData, 'category');
    }
}


