from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
import schemas, utils, models
from database import get_db
import oauth2

router = APIRouter(tags=["Profile"])


@router.get("/api/profile")
def get_profile(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    user = (
        db.query(models.User)
        .filter(models.User.user_id == current_user.user_id)
        .first()
    )
    return user
