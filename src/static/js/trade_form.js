let currentSymbol = 'BTCUSDT'; // Initial symbol

// Candlestick chart instance
let candlestickChart = null;


function initializeTradeForm() {
    console.log('trade_form.js: initialiseTradeForm ...');

    const currencyPairElement = document.getElementById('currency_pair');
    if (currencyPairElement) {
        console.log('trade_form.js: Found currency_pair element');
        currencyPairElement.addEventListener('change', async (event) => {
            console.log('trade_form.js: Event Listener update currency pair');
            currentSymbol = event.target.value.replace('/', '');
            await updateLivePrice();
            updateCandlestickChart();
        });

        // Optionally, trigger a change event manually for testing
        const event = new Event('change');
        currencyPairElement.dispatchEvent(event);
    }

    document.getElementById('limit_order_price').addEventListener('input', updateCandlestickChart);
    document.getElementById('take_profit_price').addEventListener('input', updateCandlestickChart);
    document.getElementById('stop_loss_price').addEventListener('input', updateCandlestickChart);
}

async function updateLivePrice() {
    console.log('trade_form.js: updateLivePrice ... ');
    const livePrice = await fetchLivePrice(currentSymbol);
    console.log('trade_form.js: updateLivePrice ... ', livePrice);
    if (livePrice !== null) {
        const livePriceElement = document.getElementById('live_price');
        if (livePriceElement) {
            livePriceElement.innerHTML = `Live Price: ${livePrice}`;
        } else {
            console.error('trade_form.js: Live price element not found.');
        }
    } else {
        console.error('trade_form.js: Error fetching live price');
    }
}

async function fetchLivePrice(symbol) {
    console.log('trade_form.js: fetchLivePrice ...', symbol);
    try {
        const response = await fetch(`/live_price/${symbol}`);
        if (!response.ok) {
            throw new Error('Error fetching live price');
        }
        const data = await response.json();
        console.log('trade_form.js: fetchLivePrice ...', data);
        return data.price; // Assuming the API response has a 'price' field
    } catch (error) {
        console.error('trade_form.js: Fetch live price error:', error);
        return null;
    }
}

// Candlestick chart functions are already defined in the previous response

// Example form submission handler
function handleSubmit(event) {
    event.preventDefault();
    // Implement your form submission logic here
}


// ---------------------------------------------------------------------------
// ---------------------------    CANDLESTICK CHART      ---------------------
// ---------------------------------------------------------------------------

// Initial symbol for fetching live price (example)
const candlestickData = []


async function initializeCandlestickChart() {
    console.log('trade_form.js: initializeCandlestickChart 1 ...');

    // Fetch initial candlestick data
    const initialData = await fetchCandlestickData(currentSymbol);

    console.log('trade_form.js: initializeCandlestickChart 2 ...', initialData);

    // Render the initial candlestick chart
    renderCandlestickChart(initialData);
}


// Function to fetch candlestick data
async function fetchCandlestickData(symbol) {
    console.log('trade_form.js: fetchCandlestickData ...' );
    try {
        console.log('trade_form.js: fetchCandlestickData ...');
        const response = await fetch(`/candlestick/${symbol}`);
        if (!response.ok) {
            throw new Error('Error fetching candlestick data');
        }
        const data = await response.json();
        // Convert 't' property to Date objects
        return data.map(item => ({
            ...item,
            x: new Date(item.t).getTime()
        }));
    } catch (error) {
        console.error('trade_form.js: Fetch candlestick data error:', error);
        return null;
    }
}

// Function to update candlestick chart
async function updateCandlestickChart() {
    console.log('trade_form.js: updateCandlestickChart ...' );
    const candlestickData = await fetchCandlestickData(currentSymbol);
    if (candlestickData !== null) {
        console.log('trade_form.js: updateCandlestickChart1', candlestickData);
        renderCandlestickChart(candlestickData);
    } else {
        console.error('trade_form.js: Error fetching candlestick data');
    }
}


// Function to render candlestick chart
async function renderCandlestickChart(candlestickData) {
    console.log('trade_form.js: renderCandlestickChart 1 ...', candlestickData);
    const candlestickCtx = document.getElementById('candlestickChart').getContext('2d');

    if (candlestickChart) {
        candlestickChart.destroy();
    }

    // Get values from input fields
    const limitOrderPrice = parseFloat(document.getElementById('limit_order_price').value);
    const takeProfitPrice = parseFloat(document.getElementById('take_profit_price').value);
    const stopLossPrice = parseFloat(document.getElementById('stop_loss_price').value);
    console.log('trade_form.js: renderCandlestickChart 1', limitOrderPrice, takeProfitPrice, stopLossPrice);

    // Create annotation objects if the prices are defined
    const annotations = [];
    if (!isNaN(limitOrderPrice)) {
        annotations.push({
            type: 'line',
            mode: 'horizontal',
            scaleID: 'y',
            value: limitOrderPrice,
            borderColor: 'blue',
            borderWidth: 2,
            label: {
                content: 'Limit Order',
                enabled: true,
                position: 'end'
            }
        });
    }
    if (!isNaN(takeProfitPrice)) {
        annotations.push({
            type: 'line',
            mode: 'horizontal',
            scaleID: 'y',
            value: takeProfitPrice,
            borderColor: 'green',
            borderWidth: 2,
            label: {
                content: 'Take Profit',
                enabled: true,
                position: 'end'
            }
        });
    }
    if (!isNaN(stopLossPrice)) {
        annotations.push({
            type: 'line',
            mode: 'horizontal',
            scaleID: 'y',
            value: stopLossPrice,
            borderColor: 'red',
            borderWidth: 2,
            label: {
                content: 'Stop Loss',
                enabled: true,
                position: 'end'
            }
        });
    }

    console.log('trade_form.js: renderCandlestickChart 2', candlestickData);
    candlestickChart = new Chart(candlestickCtx, {
        type: 'candlestick',
        data: {
            datasets: [{
                label: 'Candlestick Dataset',
                data: candlestickData,
                borderColor: 'red',
                backgroundColor: 'rgba(255, 0, 0, 0.1)',
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Candlestick Chart'
                },
                annotation: {
                    annotations: annotations
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        // Luxon specific format option
                        parser: 'YYYY-MM-DD',
                        tooltipFormat: 'MMM DD YYYY',
                    },
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Value'
                    }
                }
            }
        }
    });

    // Update the chart with the provided candlestick data
    candlestickChart.data.datasets[0].data = candlestickData;
    candlestickChart.update();
}


// Event delegation for dynamic content
document.addEventListener('change', async function (event) {
    const target = event.target;

    if (target.matches('#currency_pair')) {
        console.log('index.js: Event Listener update currency pair');
        currentSymbol = target.value.replace('/', '');
        await updateLivePrice();
        updateCandlestickChart();
    }
});
