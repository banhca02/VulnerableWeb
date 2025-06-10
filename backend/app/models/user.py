from sqlalchemy import Column, Integer, String, VARCHAR
from app.core.database import Base

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(VARCHAR)
#     email = Column(VARCHAR)

User = Base.classes.users