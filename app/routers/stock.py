from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional
import models, oauth2


from routers.accounts import get_accounts


router = APIRouter(prefix="/api/stocks", tags=["Stocks"])


# def stock_data_according_to_category(category):


# Function to filter and process the stock data
def filter_and_process_stocks(stocks, id, db):
    accounts_connector = get_accounts(db, id)
    investable_amount = accounts_connector.investable_balance

    filtered_stocks = []

    for stock in stocks:
        if stock.category == "Commercial Banks":
            if stock.roa > 5 and stock.roe > 14 and 10 < stock.pe < 20 and stock.pb < 3:
                quantity = investable_amount / stock.ltp
                quantity = round(quantity, 0)
                stock_data = {
                    "stock_id": stock.stock_id,
                    "ltp": stock.ltp,
                    "pb": stock.pb,
                    "roa": stock.roa,
                    "pe": stock.pe,
                    "symbol": stock.symbol,
                    "category": stock.category,
                    "roe": stock.roe,
                    "quantity": quantity,
                }
                filtered_stocks.append(stock_data)

        elif stock.category == "Microfinance":
            if stock.roa > 5 and stock.roe > 14 and 10 < stock.pe < 20 and stock.pb < 3:
                quantity = investable_amount / stock.ltp
                quantity = round(quantity, 0)
                stock_data = {
                    "stock_id": stock.stock_id,
                    "ltp": stock.ltp,
                    "pb": stock.pb,
                    "roa": stock.roa,
                    "pe": stock.pe,
                    "symbol": stock.symbol,
                    "category": stock.category,
                    "roe": stock.roe,
                    "quantity": quantity,
                }
                filtered_stocks.append(stock_data)

    return filtered_stocks


@router.get("/")
def get_stocks_recommended(
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
    limit: int = 5,
    search: Optional[str] = "",
):
    stocks = (
        db.query(models.Stocks)
        .filter(models.Stocks.category.contains(search))
        .limit(limit)
        .all()
    )

    analyzed = filter_and_process_stocks(stocks, current_user, db)

    return analyzed
