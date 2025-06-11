from sqlalchemy.orm import Session
from app.models.user import User, Customer
from app.schemas.user import UserCreate, UserLogin, TokenData, RegisterRequest
from sqlalchemy import text
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy import func
# --- Cài đặt bảo mật (Password Hashing & JWT) ---
# Khóa bí mật cho JWT (THAY ĐỔI THÀNH MỘT CHUỖI NGẪU NHIÊN, MẠNH MẼ TRONG PRODUCTION!)
SECRET_KEY = "your-very-secure-random-secret-key-that-no-one-can-guess-please-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def login_for_access_token( user_login: UserLogin, db : Session):
    query = f"select * from users where username = '{user_login.username}' and password = '{user_login.password}'"
    user = db.execute(text(query) ).fetchone()
    # user = get_user_by_username(db, username=user_login.username)
    if not user: # <-- SO SÁNH TRỰC TIẾP
        raise HTTPException(
            status_code=401,
            detail="Tên đăng nhập hoặc mật khẩu không đúng",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Tạo một JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_customer_information(username: str, db: Session):
    user = get_user_by_username(db, username)
    if user:
        query_str = f"SELECT * FROM customer WHERE userid = {user.userid}" # <-- LỖ HỔNG Ở ĐÂY  
        # Thực thi truy vấn SQL thô
        result = db.execute(text(query_str) )
        customer_row = result.fetchone()
        if customer_row:
            return dict(customer_row._mapping)
        return None
    return None

def get_current_user(db: Session, token: str):
    print(token)
    credentials_exception = HTTPException(
        status_code=401,
        detail="Không thể xác thực thông tin đăng nhập",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_customer_information(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user

def create_user(db: Session, user: RegisterRequest):
    max_id = db.query(func.max(User.userid)).scalar()
    new_id = (max_id or 0) + 1
    db_user = User(
        userid = new_id,
        username=user.username,
        password=user.password,
        email=user.email,
    )
    db_customer = Customer(
        userid = new_id,
        fullname=user.fullname,
        address=user.address,
        phonenumber=user.phonenumber,
        birthdate=user.birthdate,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user) 

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer) 




# def get_users(db: Session):
#     return db.query(Customer).all()

# def get_user_by_id(db: Session, user_id: int):
#     return db.query(User).filter(User.id == user_id).first()

# def create_user(db: Session, user: UserCreate):
#     db_user = User(name=user.name, email=user.email)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def get_user_by_id(db: Session, user_id: int):
#     stmt = text("SELECT * FROM users WHERE id = :user_id")
#     result = db.execute(stmt, {"user_id": user_id})
#     return result.fetchone()