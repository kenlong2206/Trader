import os
from fastapi import FastAPI, Form, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from binance.client import Client
from typing import Optional, List
from pydantic import BaseModel, create_model
from datetime import datetime
from Trader.src.data_access import create_trade, read_trades, update_trade, delete_trade
from Trader.models.trade import Trade
from Trader.src.logging_config import setup_logging

# Set up logging
logger = setup_logging()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = FastAPI()
templates = Jinja2Templates(directory=TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Initialize Binance client
api_key = "YOUR_BINANCE_API_KEY"
api_secret = "YOUR_BINANCE_API_SECRET"
binance_client = Client(api_key, api_secret)


@app.get("/", response_class=HTMLResponse)
async def get_main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/trade_log", response_class=HTMLResponse)
async def get_trade_log(request: Request):
    trades = read_trades()  # Function to read trade data
    return templates.TemplateResponse("trade_log.html", {"request": request, "trades": trades})


@app.get("/trade_form", response_class=HTMLResponse)
async def get_trade_form(request: Request):
    return templates.TemplateResponse("trade_form.html", {"request": request})


@app.get("/portfolio", response_class=HTMLResponse)
async def get_portfolio(request: Request):
    return templates.TemplateResponse("portfolio.html", {"request": request})


@app.get("/analytics", response_class=HTMLResponse)
async def get_analytics(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})


@app.get("/live_price/{symbol}")
async def get_live_price(symbol: str):
    try:
        ticker = binance_client.get_symbol_ticker(symbol=symbol)
        return JSONResponse(content=ticker)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/candlestick/{symbol}", response_model=List[dict])
async def get_candlestick(symbol: str, interval: str = "1d", limit: int = 50):
    try:
        candles = binance_client.get_klines(symbol=symbol, interval=interval, limit=limit)
        candle_data = []
        for candle in candles:
            candle_data.append({
                "t": datetime.fromtimestamp(candle[0] / 1000),  # Convert timestamp to datetime
                "o": float(candle[1]),  # Open
                "h": float(candle[2]),  # High
                "l": float(candle[3]),  # Low
                "c": float(candle[4])   # Close
            })
        return candle_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class TradeForm(BaseModel):
    title: str
    order_type: str
    currency_pair: str
    direction: str
    limit_order_price: float
    take_profit_price: float
    stop_loss_price: float
    amount: float
    leverage: float
    exchange: Optional[str] = None
    trade_id: Optional[str] = None
    trade_status: Optional[str] = None
    notes: Optional[str] = None
    strategy: Optional[str] = None
    links: Optional[str] = None
    capital_at_risk: Optional[float] = None
    fees: Optional[float] = None
    user: Optional[str] = None
    risk_rating: Optional[str] = None
    pnl: Optional[float] = None
    created_timestamp: Optional[str] = None
    executed_timestamp: Optional[str] = None
    closed_timestamp: Optional[str] = None


@app.post("/submit_trade")
async def submit_trade(
    title: str = Form(...),
    order_type: str = Form(...),
    currency_pair: str = Form(...),
    direction: str = Form(...),
    limit_order_price: float = Form(...),
    take_profit_price: float = Form(...),
    stop_loss_price: float = Form(...),
    amount: float = Form(...),
    leverage: float = Form(...),
    exchange: Optional[str] = Form(None),
    trade_id: Optional[str] = Form(None),
    trade_status: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    strategy: Optional[str] = Form(None),
    links: Optional[str] = Form(None),
    capital_at_risk: Optional[float] = Form(None),
    fees: Optional[float] = Form(None),
    user: Optional[str] = Form(None),
    risk_rating: Optional[str] = Form(None),
    pnl: Optional[float] = Form(None),
    created_timestamp: Optional[str] = Form(None),
    executed_timestamp: Optional[str] = Form(None),
    closed_timestamp: Optional[str] = Form(None),
):
    trade_data = TradeForm(
        title=title,
        order_type=order_type,
        currency_pair=currency_pair,
        direction=direction,
        limit_order_price=limit_order_price,
        take_profit_price=take_profit_price,
        stop_loss_price=stop_loss_price,
        amount=amount,
        leverage=leverage,
        exchange=exchange,
        trade_id=trade_id,
        trade_status=trade_status,
        notes=notes,
        strategy=strategy,
        links=links,
        capital_at_risk=capital_at_risk,
        fees=fees,
        user=user,
        risk_rating=risk_rating,
        pnl=pnl,
        created_timestamp=created_timestamp,
        executed_timestamp=executed_timestamp,
        closed_timestamp=closed_timestamp,
    )

    logger.info("Trade form data: %s", trade_data.dict())

    # Call the create_trade function to write data to the file
    created_trade = create_trade(trade_data)

    # Return JSON response indicating success
    return {
        "status": "success",
        "message": f"Trade '{title}' submitted successfully!",
        "trade": {
            "title": title,
            "trade_id": trade_id
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
