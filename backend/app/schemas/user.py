from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

# --- User Schema ---
class UserBase(BaseModel):
    username: str = Field(..., max_length=100)
    password: str = Field(..., max_length=256)
    email: Optional[str] = Field(None, max_length=255)

class UserCreate(UserBase):
    pass # Kế thừa tất cả các trường từ UserBase

class UserUpdate(BaseModel): # Chỉ cập nhật Username, Email
    Username: Optional[str] = Field(None, max_length=100)
    Email: Optional[str] = Field(None, max_length=255)
    # PasswordHash thường được xử lý riêng nếu muốn cập nhật mật khẩu

class UserInDB(UserBase):
    UserID: int
    CreatedAt: datetime

    class Config:
        from_attributes  = True

# --- Customer Schema ---
class CustomerBase(BaseModel):
    fullname: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = Field(None, max_length=255)
    phonenumber: Optional[str] = Field(None, max_length=20)
    birthdate: Optional[date] = None

    class Config:
        from_attributes  = True

class CustomerCreate(CustomerBase):
    UserID: int # Cần UserID để tạo customer mới liên kết với Users

class CustomerUpdate(CustomerBase):
    pass # Kế thừa CustomerBase, tất cả đều là Optional

class CustomerInDB(CustomerBase):
    UserID: int

    class Config:
        from_attributes  = True

# --- Admin Schema ---
class AdminBase(BaseModel):
    PhoneNumber: Optional[str] = Field(None, max_length=20)

class AdminCreate(AdminBase):
    UserID: int # Cần UserID để tạo admin mới liên kết với Users

class AdminUpdate(AdminBase):
    pass # Kế thừa AdminBase, tất cả đều là Optional

class AdminInDB(AdminBase):
    UserID: int

    class Config:
        from_attributes  = True

class UserLogin(BaseModel):
    username: str
    password: str

# --- NEW: Token Schema ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

# Đây là schema sẽ được sử dụng để nhận dữ liệu từ frontend khi đăng ký
class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str
    fullname: str
    address: Optional[str] = None
    phonenumber: Optional[str] = None
    birthdate: Optional[datetime] = None