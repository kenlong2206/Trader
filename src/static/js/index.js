document.addEventListener("DOMContentLoaded", function () {
    // Initialise DataTable
    $('#tradesTable').DataTable({
        "pageLength": 50
    });

    // Add event listeners for tab clicks
    document.getElementById('trade-log-tab').addEventListener('click', loadTradeLog);
    document.getElementById('add-trade-tab').addEventListener('click', loadTradeForm);
    document.getElementById('portfolio-tab').addEventListener('click', loadPortfolio);
    document.getElementById('analytics-tab').addEventListener('click', loadAnalytics);

    // Load the trade log by default when the page loads
    loadTradeLog();
});


async function loadTradeLog() {
    console.log('Index: Loading trade log...');
    try {
        const response = await fetch('/trade_log');
        const html = await response.text();
        document.getElementById('tradeLogContent').innerHTML = html;
    } catch (error) {
        console.error('Index: Error loading trade log:', error);
    }
}


async function loadTradeForm() {
    console.log('Index: Loading trade form 1...');
    try {
        const response = await fetch('/trade_form');
        const html = await response.text();
        document.getElementById('tradeFormContent').innerHTML = html;

        console.log('Index: Loading trade form 2...');

        // Ensure this function is called after the form is loaded
        initializeTradeForm();
    } catch (error) {
        console.error('Index: Error loading trade form:', error);
    }
}


async function loadPortfolio() {
    console.log('Index: Loading portfolio summary...');
    try {
        const response = await fetch('/portfolio');
        const html = await response.text();
        document.getElementById('portfolioContent').innerHTML = html;
    } catch (error) {
        console.error('Index: Error loading portfolio summary:', error);
    }
}


async function loadAnalytics() {
    console.log('Index: Loading analytics...');
    try {
        const response = await fetch('/analytics');
        const html = await response.text();
        document.getElementById('analyticsContent').innerHTML = html;
    } catch (error) {
        console.error('Index: Error loading analytics:', error);
    }
}
