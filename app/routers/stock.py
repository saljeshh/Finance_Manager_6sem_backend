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

def average_finder(stocks, sector):
    total_roe = 0
    total_pe = 0
    total_pb = 0
    total_roa = 0
    count = 0

    for stock in stocks:
        if stock.sector == sector:
            total_roe += stock.roe
            total_pe += stock.pe
            total_pb += stock.pb
            total_roa += stock.roa
            count += 1

    if count == 0:
        return 0, 0, 0,0  # Avoid division by zero if there are no stocks in the sector

    avg_roe = round(total_roe / count, 2)
    avg_pe = round(total_pe / count, 2)
    avg_pb = round(total_pb / count, 2)
    avg_roa = round(total_roa / count, 2)

    return avg_roe, avg_pe, avg_pb, avg_roa




# Function to filter and process the stock data
def filter_and_process_stocks(stocks, id, db):
    accounts_connector = get_accounts(db, id)
    investable_amount = accounts_connector.investable_balance
    filtered_stocks = []

    for stock in stocks:
        if stock.sector == "Commercial Banks":
            avg_roe, avg_pe, avg_pb,avg_roa = average_finder(stocks, 'Commercial Banks')
            if (

                (stock.roe > avg_roe)
                and (stock.pe < avg_pe)
                and (stock.pb < avg_pb)
                and (stock.roa > avg_roa)
            ):
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Microfinance":
            avg_roe, avg_pe, avg_pb,avg_roa = average_finder(stocks, 'Microfinance')
            if (
                (stock.roe > avg_roe)
                and (stock.pe < avg_pe)
                and (stock.pb < avg_pb)
                and (stock.roa > avg_roa)
            ):
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Development Banks":
            avg_roe, avg_pe, avg_pb,avg_roa = average_finder(stocks, 'Development Banks')
            if (
                (stock.roe > avg_roe)
                and (stock.pe < avg_pe)
                and (stock.pb < avg_pb)
                and (stock.roa > avg_roa)
            ):
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Hydro Power":
            avg_roe, avg_pe, avg_pb,avg_roa = average_finder(stocks, 'Hydro Power')
            if ((stock.roe > avg_roe)
                and (stock.pe < avg_pe)
                and (stock.pb < avg_pb)
                and (stock.roa > avg_roa)):
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Manufacturing And Processing":
            avg_roe, avg_pe, avg_pb,avg_roa = average_finder(stocks, 'Manufacturing And Processing')
            if ((stock.roe > avg_roe)
                and (stock.pe < avg_pe)
                and (stock.pb < avg_pb)
                and (stock.roa > avg_roa)):
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Finance":
            avg_roe, avg_pe, avg_pb,avg_roa = average_finder(stocks, 'Finance')
            if ((stock.roe < avg_roe)
                and (stock.pe < avg_pe)
                and (stock.pb > avg_pb)
                and (stock.roa < avg_roa)):
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Life Insurance":
            avg_roe, avg_pe, avg_pb,avg_roa = average_finder(stocks, 'Life Insurance')
            if((stock.roe > avg_roe)
                and (stock.pe < avg_pe)
                and (stock.pb < avg_pb)
                and (stock.roa > avg_roa)):
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Non Life":
            avg_roe, avg_pe, avg_pb,avg_roa = average_finder(stocks, 'Non Life')
            if ((stock.roe > avg_roe)
                and (stock.pe < avg_pe)
                and (stock.pb < avg_pb)
                and (stock.roa > avg_roa)):
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Investment":
            avg_roe, avg_pe, avg_pb,avg_roa = average_finder(stocks, 'Investment')
            if ((stock.roe > avg_roe)
                and (stock.pe < avg_pe)
                and (stock.pb < avg_pb)
                and (stock.roa > avg_roa)):
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Others":
            avg_roe, avg_pe, avg_pb,avg_roa = average_finder(stocks, 'Others')
            if ((stock.roe > avg_roe)
                and (stock.pe < avg_pe)
                and (stock.pb < avg_pb)
                and (stock.roa > avg_roa)):
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)
        
        if stock.sector == "Tradings":
            avg_roe, avg_pe, avg_pb,avg_roa = average_finder(stocks, 'Tradings')
            if ((stock.roe > avg_roe)
                and (stock.pe > avg_pe)
                and (stock.pb < avg_pb)
                and (stock.roa > avg_roa)):
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

        if stock.sector == "Hotels":
            avg_roe, avg_pe, avg_pb,avg_roa = average_finder(stocks, 'Hotels')
            if ((stock.roe > avg_roe)
                and (stock.pe < avg_pe)
                and (stock.pb < avg_pb)
                and (stock.roa > avg_roa)):
                stock_data = stock_data_according_to_category(stock, investable_amount)
                filtered_stocks.append(stock_data)

    return filtered_stocks



@router.get("/")
def get_stocks_recommended(
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
    limit: int = 200,
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
