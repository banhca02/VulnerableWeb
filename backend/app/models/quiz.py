from sqlalchemy import Column, Integer, VARCHAR, PrimaryKeyConstraint
from app.core.database import Base

# class Quizzes(Base):
#     __tablename__ = "Quizzes"
#     ClassID = Column(Integer, nullable=False)
#     QuizName = Column(VARCHAR, nullable=False)
#     TimeTaken = Column(Integer)
#     NumQuestions = Column(Integer)
#     QuizPoint = Column(Integer)
#     __table_args__ = (
#     PrimaryKeyConstraint('ClassID', 'QuizName'),
# )
# Giờ bạn có thể sử dụng các model đã được tạo tự động từ cơ sở dữ liệu
Quizzes = Base.classes.Quizzes
Questions = Base.classes.Questions