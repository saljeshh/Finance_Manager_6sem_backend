from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import accounts, stock, investable, transaction, auth, profile

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://192.168.10.68:3000",
    "http://127.0.0.1:57472",
    "http://127.0.0.1:3000",
]

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    # You can specify specific HTTP methods (e.g., ["GET", "POST"])
    allow_methods=["*"],
    # You can specify specific HTTP headers (e.g., ["Authorization"])
    allow_headers=["*"],
)

app.include_router(accounts.router)
app.include_router(stock.router)
app.include_router(auth.router)
app.include_router(investable.router)
app.include_router(transaction.router)
app.include_router(profile.router)
