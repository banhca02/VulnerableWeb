from sqlalchemy.orm import Session
from app.models.quiz import Quizzes, Questions
from app.schemas.quiz import QuizCreate, QuestionOut, QuizOut, ChoicesOut
from sqlalchemy import text



# def get_quiz_by_name(db: Session, classID: int, quizName: str):
#     return db.query(Quizzes).filter(
#         (Quizzes.ClassID == classID) & (Quizzes.QuizName == quizName)
#     ).first()

def get_quiz_by_name(db: Session, classID: int, quizName: str):
    quiz_stmt = text("SELECT * FROM QuizzEs WHERE ClassID = :classID and QuizName = :quizName")
    quiz_result = db.execute(quiz_stmt, {"classID": classID, "quizName": quizName}).mappings().first()

    if not quiz_result:
        return None

    questions_stmt = text("SELECT * FROM questions WHERE ClassID = :classID and QuizName = :quizName")
    questions_result = db.execute(questions_stmt, {"classID": classID, "quizName": quizName}).mappings().fetchall()
    
    choices_stmt = text("select * from Choices where ClassID = :classID and QuizName = :quizName")
    choices_result = db.execute(choices_stmt, {"classID": classID, "quizName": quizName}).mappings().fetchall()


    question_list = []
    for q in questions_result:
        choices_list =[]
        for c in choices_result:
            if c['QuestionNumber'] == q['QuestionNumber']:
                choices_list.append(ChoicesOut(
                    ChoiceText=c['ChoiceText'],
                    IsTrue=c['IsTrue']
                ))
        question_list.append(QuestionOut(
            QuestionNumber=q['QuestionNumber'],
            QuestionText=q['QuestionText'],
            QuestionPoint=q['QuestionPoint'],
            Choices=choices_list,
        ))

    return QuizOut(
        ClassID=quiz_result['ClassID'],
        QuizName=quiz_result['QuizName'],
        TimeTaken=quiz_result['TimeTaken'],
        NumQuestions=quiz_result['NumQuestions'],
        QuizPoint=quiz_result['QuizPoint'],
        Questions=question_list
    )