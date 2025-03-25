export const schoolsFONDistanceSummary = {
    type: 'bar',
    options: {
        indexAxis: 'y', // Horizontal bar
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                stacked: true,
                display: false,
            },
            y: {
                stacked: true,
                display: false,
            },
        },
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    boxWidth: 12,
                    font: { size: 12 },
                    padding: 10,
                },
            },
            tooltip: { enabled: false },
        },
    },
};

export const schoolsFONDistance = {
    type: 'bar',
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                min: 0, // Ensure the scale starts at 0
                ticks: {
                    display: true,
                    font: { weight: 'bold', size: 12 }, // Make labels bold
                    callback: function (value, index, values) {
                        // show first and last labels

                        if (value === 0) return '0 KM';

                        if (index + 1 === values.length) {
                            return `${value} KM`;
                        }

                        return ''; // Hide other labels
                    },
                    autoSkip: false, // Prevent skipping labels
                    maxRotation: 0, // Keep labels horizontal
                    minRotation: 0,
                },
                grid: { display: false }, // Hide vertical grid lines
            },
            y: { display: false }, // Hide Y-axis
        },
        plugins: {
            legend: { display: false }, // Hide legend (only one dataset)
            tooltip: { enabled: false }, // Enable tooltips
        },
    },
};

export const mobileCoverageSummary = {
    type: 'bar',
    options: {
        indexAxis: 'y', // Horizontal bar
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                stacked: true,
                display: false,
            },
            y: {
                stacked: true,
                display: false,
            },
        },
        plugins: {
            legend: {
                display: false,
            },
            tooltip: { enabled: false },
        },
    },
};

export const regionsMobileCoverage = {
    type: 'scatter',
    options: {
        indexAxis: 'y', // Horizontal bar
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                grid: { display: false },
                title: {
                    text: 'POPULATION DENSITY',
                    display: true,
                },
            },
            y: {
                grid: { display: false },
                title: {
                    text: 'COVERAGE %',
                    display: true,
                },
            },
        },
        plugins: {
            legend: {
                display: false,
            },
            tooltip: { enabled: false },
        },
    },
};
