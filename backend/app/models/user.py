from sqlalchemy import Column, Integer, String, VARCHAR
from app.core.database import Base

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(VARCHAR)
#     email = Column(VARCHAR)

User = Base.classes.users
Customer = Base.classes.customer
Admin = Base.classes.admins

# # models.py
# from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base # Import this

# # Đây là base class mà các model của chúng ta sẽ kế thừa.
# # Hãy đảm bảo rằng Base được import từ database.py hoặc được định nghĩa ở đây
# # Nếu bạn đã import từ database.py, bạn có thể xóa dòng declarative_base ở đây
# # For consistency, let's assume 'Base' comes from database.py as defined previously
# from database import Base # Import Base from database.py

# class User(Base):
#     __tablename__ = "users"

#     UserID = Column(Integer, primary_key=True)
#     Username = Column(String(100), nullable=False, unique=True)
#     PasswordHash = Column(String(256), nullable=False)
#     Email = Column(String(255), nullable=True)
#     CreatedAt = Column(DateTime, default=datetime.utcnow) # Sử dụng datetime.utcnow cho mặc định

#     # Định nghĩa quan hệ với Customer và Admins
#     customer = relationship("Customer", back_populates="user", uselist=False)
#     admin = relationship("Admin", back_populates="user", uselist=False)

#     def __repr__(self):
#         return f"<User(UserID={self.UserID}, Username='{self.Username}')>"

# class Customer(Base):
#     __tablename__ = "customer" # Tên bảng trong database là 'customer'

#     UserID = Column(Integer, ForeignKey("users.UserID"), primary_key=True)
#     FullName = Column(String(255), nullable=True)
#     Address = Column(String(255), nullable=True)
#     PhoneNumber = Column(String(20), nullable=True)
#     BirthDate = Column(Date, nullable=True)

#     # Định nghĩa quan hệ với User
#     user = relationship("User", back_populates="customer")

#     def __repr__(self):
#         return f"<Customer(UserID={self.UserID}, FullName='{self.FullName}')>"

# class Admin(Base):
#     __tablename__ = "admins" # Tên bảng trong database là 'admins'

#     UserID = Column(Integer, ForeignKey("users.UserID"), primary_key=True)
#     PhoneNumber = Column(String(20), nullable=True)

#     # Định nghĩa quan hệ với User
#     user = relationship("User", back_populates="admin")

#     def __repr__(self):
#         return f"<Admin(UserID={self.UserID})>"