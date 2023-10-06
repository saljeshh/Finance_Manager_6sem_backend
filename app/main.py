from fastapi import FastAPI
import models
from database import engine
from routers import accounts, stock, investable, transaction, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(accounts.router)
app.include_router(stock.router)
app.include_router(auth.router)
app.include_router(investable.router)
app.include_router(transaction.router)
