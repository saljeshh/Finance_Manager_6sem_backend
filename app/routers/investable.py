from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
import schemas, models
import oauth2
from database import get_db

router = APIRouter(prefix="/api/investable", tags=["Investable"])


@router.get("/")
def get_investable_percent(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    investable = (
        db.query(models.Investable)
        .filter(models.Investable.user_id == current_user.user_id)
        .first()
    )

    return investable


# only once
@router.post("/")
async def set_investable_percent(
    investable: schemas.InvestableBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # check if the users_id aready exist in the databaes
    checksum = (
        db.query(models.Investable)
        .filter(models.Investable.user_id == current_user.user_id)
        .first()
    )

    if checksum:
        return {"message": "User already exists"}

    new_investable = models.Investable(
        user_id=current_user.user_id, investable_percent=investable.investable_percent
    )

    db.add(new_investable)
    db.commit()
    return {"message": "Investable added successfully"}


@router.put("/")
async def update_percent(
    investable: schemas.InvestableBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    investable_query = db.query(models.Investable).filter(
        models.Investable.user_id == current_user.user_id
    )

    investable_database = investable_query.first()

    if investable_database == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Investable with id:{id} not found",
        )

    investable_database.investable_percent = investable.investable_percent

    db.commit()
    return {"message": "Investable Updated successfully"}
