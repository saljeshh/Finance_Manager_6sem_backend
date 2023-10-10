from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
import schemas, utils, models
from database import get_db
import oauth2
from config import settings

router = APIRouter(tags=["Authentication"])


@router.post("/register")
async def register_account(user: schemas.UserBase, db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Password and confirm password should match",
        )

    hashed_password = utils.hash(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        currency=user.currency,
        city=user.city,
        phone_no=user.phone_no,
    )

    db.add(new_user)
    db.commit()

    return {"message": "User Registered Successfully"}


@router.post("/login")
async def login_account(users: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == users.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, details="Invalid credentials"
        )

    if not utils.verify(users.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    # create jwt token
    access_token = oauth2.create_access_token(data={"user_id": user.user_id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
