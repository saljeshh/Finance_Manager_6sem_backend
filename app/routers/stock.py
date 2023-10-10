from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional
import models, oauth2


from routers.accounts import get_accounts


router = APIRouter(prefix="/api/stocks", tags=["Stocks"])


def stock_data_according_to_category(stock, investable_amount):
    quantity = investable_amount / stock.ltp
    quantity = round(quantity, 0)
    stock_data = {
        "stock_id": stock.stock_id,
        "ltp": stock.ltp,
        "pb": stock.pb,
        "roa": stock.roa,
        "pe": stock.pe,
        "symbol": stock.symbol,
        "sector": stock.sector,
        "roe": stock.roe,
        "quantity": quantity,
    }

    return stock_data


# Function to filter and process the stock data
def filter_and_process_stocks(stocks, id, db):
    accounts_connector = get_accounts(db, id)
    investable_amount = accounts_connector.investable_balance
    filtered_stocks = []

    for stock in stocks:
        if stock.sector == "Commercial Banks":
            if (
                (stock.roa > 1)
                and (stock.roe > 12)
                and (stock.pe < 14)
                and (stock.pb < 2)
            ):
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Microfinance":
            if (
                (stock.pe > 23 and stock.pe < 50)
                and (stock.roe > 15)
                and (stock.pb < 5)
            ):
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Development Banks":
            if (
                (stock.pe > 10 and stock.pe < 30)
                and (stock.roe > 10)
                and (stock.pb < 3)
            ):
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Hydro Power":
            if (stock.pe > 4 and stock.pe < 20) and (stock.pb < 5):
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Manufacturing And Processing":
            if stock.pe > 5 and stock.pe < 30:
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Finance":
            if (stock.pe > 10 and stock.pe < 30) and stock.roe > 10:
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Life Insurance":
            if stock.roe > 6:
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Non Life":
            if stock.roe > 10 and stock.pb < 5:
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Investment":
            if stock.pe < 30:
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Others" or stock.sector == "Tradings":
            if stock.pe < 30:
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Hotels":
            if stock.roe > 10 and stock.pe < 40:
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

    return filtered_stocks


def test(stocks):
    print(stocks)


@router.get("/")
def get_stocks_recommended(
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
    limit: int = 100,
    search: Optional[str] = "",
):
    stocks = (
        db.query(models.Stocks)
        .filter(models.Stocks.sector.contains(search))
        .limit(limit)
        .all()
    )

    analyzed = filter_and_process_stocks(stocks, current_user, db)

    return analyzed
