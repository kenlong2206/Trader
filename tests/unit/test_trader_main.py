import sys
import os
import pytest
from fastapi.testclient import TestClient
from Trader.src.main import app, binance_client
from unittest.mock import MagicMock, patch
from datetime import datetime
from Trader.models.trade import Trade
from bs4 import BeautifulSoup

# Add the src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

@pytest.fixture
def client():
    return TestClient(app)


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('title')
    assert title is not None, "No <title> element found in the HTML"
    assert "Trade Manager" in title.text, f"Expected title 'Your Expected Title' but got '{title.text}'"


def test_read_trade_log(client):
    response = client.get("/trade_log")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('title')
    assert title is not None, "No <title> element found in the HTML"
    assert "Trade Log" in title.text, f"Expected title 'Your Expected Title' but got '{title.text}'"


def test_read_trade_form(client):
    response = client.get("/trade_form")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('title')
    assert title is not None, "No <title> element found in the HTML"
    assert "Trade Form" in title.text, f"Expected title 'Your Expected Title' but got '{title.text}'"


def test_read_analytics(client):
    response = client.get("/analytics")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('title')
    assert title is not None, "No <title> element found in the HTML"
    assert "Analytics" in title.text, f"Expected title 'Your Expected Title' but got '{title.text}'"

def test_read_portfolio(client):
    response = client.get("/portfolio")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('title')
    assert title is not None, "No <title> element found in the HTML"
    assert "Portfolio" in title.text, f"Expected title 'Your Expected Title' but got '{title.text}'"


def test_get_live_price(client):
    # """Test the /live_price endpoint."""
    mock_ticker = {"symbol": "BTCUSDT", "price": "35000.00"}
    #
    binance_client.get_symbol_ticker = MagicMock(return_value=mock_ticker)

    response = client.get("/live_price/BTCUSDT")
    assert response.status_code == 200
    assert response.json() == mock_ticker


def test_get_candlestick(client):
    """Test the /candlestick endpoint."""
    mock_candles = [
        [1623355200000, '35000.00', '35200.00', '34800.00', '35100.00', '500'],
        [1623358800000, '35100.00', '35400.00', '35050.00', '35200.00', '600']
    ]
    binance_client.get_klines = MagicMock(return_value=mock_candles)

    response = client.get("/candlestick/BTCUSDT")
    assert response.status_code == 200
    assert all("t" in candle and "o" in candle for candle in response.json())




def test_submit_trade_validation(client):
    """Test validation failure scenario for /submit_trade endpoint."""
    # Submitting trade without required fields should return HTTP 422
    invalid_trade_data = {
        "title": "Invalid Trade",
        "order_type": "Market",
        # Missing required fields like currency_pair, direction, amount, etc.
    }
    response = client.post("/submit_trade", data=invalid_trade_data)
    assert response.status_code == 422


