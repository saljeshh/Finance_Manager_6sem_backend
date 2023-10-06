from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
import schemas, models, oauth2
from routers.investable import get_investable_percent

router = APIRouter(prefix="/api/accounts", tags=["Accounts"])


# get specific users account
@router.get("/")
def get_accounts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    get_account_data = (
        db.query(models.Accounts)
        .filter(models.Accounts.user_id == current_user.user_id)
        .first()
    )
    return get_account_data


# to make users to only set the account once, we will make UI like that once its initialized we cant do again
# we can just updated after once account is created
@router.post("/")
def init_accounts(
    post: schemas.AccountsBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # validation check if account already exists
    checksum = (
        db.query(models.Accounts)
        .filter(models.Accounts.user_id == current_user.user_id)
        .first()
    )

    if checksum:
        return {"message": "Account already exists"}

    cash_balance = post.cash
    bank_balance = post.bank
    total_balance = cash_balance + bank_balance
    user_id = current_user.user_id

    # for investable
    investable_connector = get_investable_percent(db, current_user)
    investable_percent = investable_connector.investable_percent
    investable_balance = (total_balance * investable_percent) / 100

    new_account = models.Accounts(
        user_id=user_id,
        cash_balance=cash_balance,
        bank_balance=bank_balance,
        total_balance=total_balance,
        investable_balance=investable_balance,
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return {"message": "Account created successfully"}


# update account on basis of user_id
@router.put("/")
def update_account(
    post: schemas.AccountsBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    accounts_query = db.query(models.Accounts).filter(
        models.Accounts.user_id == current_user.user_id
    )

    accounts_database = accounts_query.first()

    if accounts_database == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with user id {current_user.user_id} not found",
        )

    cash_balance = post.cash
    bank_balance = post.bank
    total_balance = cash_balance + bank_balance
    user_id = current_user.user_id

    # for investable
    investable_connector = get_investable_percent(db, current_user)
    investable_percent = investable_connector.investable_percent
    investable_balance = (total_balance * investable_percent) / 100

    accounts_database.cash_balance = cash_balance
    accounts_database.bank_balance = bank_balance
    accounts_database.total_balance = total_balance
    accounts_database.investable_balance = investable_balance

    db.commit()

    return {"message": "Updated successfully"}
