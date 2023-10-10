from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy import and_
from sqlalchemy.orm import Session
from database import get_db
import schemas, models, oauth2
from routers.accounts import update_account
from schemas import AccountsBase
from datetime import datetime


router = APIRouter(prefix="/api/transactions", tags=["Transaction"])


@router.get("/")
async def get_transactions(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    all_transactions = (
        db.query(models.Transactions)
        .filter(models.Transactions.user_id == current_user.user_id)
        .all()
    )
    return all_transactions


# need to update accounts table
@router.post("/")
def create_transaction(
    transaction: schemas.TransactionBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # Assuming transaction_data contains the timestamp as a string
    timestamp_str = str(transaction.timestamp)

    # Parse the timestamp string into a datetime object
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S%z")

    new_transaction = models.Transactions(
        user_id=current_user.user_id,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        account_type=transaction.account_type,
        category=transaction.category,
        timestamp=timestamp,
    )

    db.add(new_transaction)
    db.commit()

    try:
        # # fetch the current user account
        user_account = (
            db.query(models.Accounts)
            .filter(models.Accounts.user_id == current_user.user_id)
            .first()
        )

        post = {"cash": user_account.cash_balance, "bank": user_account.bank_balance}

        # # update based on condition
        if transaction.transaction_type == "expense":
            if transaction.account_type == "cash":
                post["cash"] -= transaction.amount
            elif transaction.account_type == "bank":
                post["bank"] -= transaction.amount

        elif transaction.transaction_type == "income":
            if transaction.account_type == "cash":
                post["cash"] += transaction.amount
            elif transaction.account_type == "bank":
                post["bank"] += transaction.amount

        # createing pydantic model
        post_pydantic = AccountsBase(**post)
        update_account(post_pydantic, db, current_user)

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    return {
        "message": "Transactions added successfully",
    }


@router.put("/{id}")
def update_transaction(
    id: int,
    transaction: schemas.TransactionBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    transaction_query = db.query(models.Transactions).filter(
        and_(
            models.Transactions.transaction_id == id,
            models.Transactions.user_id == current_user.user_id,
        )
    )

    transactions_database = transaction_query.first()

    if transactions_database == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction with id:{id} not found",
        )

    old_amount = transactions_database.amount

    new_account_type = transaction.account_type
    new_amount = transaction.amount
    new_transaction_type = transaction.transaction_type
    new_category = transaction.category

    transactions_database.account_type = new_account_type
    transactions_database.amount = new_amount
    transactions_database.transaction_type = new_transaction_type
    transactions_database.category = new_category

    try:
        # # fetch the current user account
        user_account = (
            db.query(models.Accounts)
            .filter(models.Accounts.user_id == current_user.user_id)
            .first()
        )

        post = {"cash": user_account.cash_balance, "bank": user_account.bank_balance}

        # fetch new one row of data of current user and current transaction
        transactions_database = transaction_query.first()

        # # update based on condition
        if transactions_database.transaction_type == "expense":
            if transactions_database.account_type == "cash":
                # if creating new transaction then obviously there is no old_amount so check
                if old_amount:
                    post["cash"] -= old_amount
                post["cash"] -= transactions_database.amount
            elif transactions_database.account_type == "bank":
                if old_amount:
                    post["bank"] -= old_amount
                post["bank"] -= transactions_database.amount

        elif transactions_database.transaction_type == "income":
            if transactions_database.account_type == "cash":
                if old_amount:
                    post["cash"] -= old_amount
                post["cash"] += transactions_database.amount
            elif transactions_database.account_type == "bank":
                if old_amount:
                    post["bank"] -= old_amount
                post["bank"] += transactions_database.amount

        # createing pydantic model
        post_pydantic = AccountsBase(**post)
        update_account(post_pydantic, db, current_user)

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    db.commit()

    return {"message": "Transaction Updated successfully"}


@router.delete("/{id}")
def delete_transaction(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    transaction_query = db.query(models.Transactions).filter(
        and_(
            models.Transactions.transaction_id == id,
            models.Transactions.user_id == current_user.user_id,
        )
    )

    transactions_database = transaction_query.first()
    print(transactions_database)

    old_amount = transactions_database.amount

    if transactions_database == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )

    try:
        # # fetch the current user account
        user_account = (
            db.query(models.Accounts)
            .filter(models.Accounts.user_id == current_user.user_id)
            .first()
        )

        post = {"cash": user_account.cash_balance, "bank": user_account.bank_balance}

        # fetch new one row of data of current user and current transaction
        transactions_database = transaction_query.first()

        # # update based on condition
        if transactions_database.transaction_type == "expense":
            if transactions_database.account_type == "cash":
                # when deleting old amount must be again revived so we do opposite of transaction type
                if old_amount:
                    post["cash"] += old_amount

            elif transactions_database.account_type == "bank":
                if old_amount:
                    post["bank"] += old_amount

        elif transactions_database.transaction_type == "income":
            if transactions_database.account_type == "cash":
                if old_amount:
                    post["cash"] -= old_amount

            elif transactions_database.account_type == "bank":
                if old_amount:
                    post["bank"] -= old_amount

        # createing pydantic model
        post_pydantic = AccountsBase(**post)
        update_account(post_pydantic, db, current_user)

    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    transaction_query.delete()
    db.commit()

    return {"message": "transaction deleted successfully"}
