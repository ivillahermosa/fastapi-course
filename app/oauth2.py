from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Requirements for oauth2
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    # set expiration time from now and add to_encode variable exp
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # generate the token with secret_key and payload (to_encode)
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_access_token(token: str, credentials_exception):
    try:
        # decode and extract the id
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id")
        if id is None or id == '':
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        # There is an error here credentials exception no output
        return credentials_exception

    return token_data


# use in endpoint verification
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials!", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    if isinstance(token, HTTPException):
        return token

    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
