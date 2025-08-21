from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey

Base = declarative_base()

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    number = Column(Integer)

    answers = relationship('Answers', back_populates='question')

    def __repr__(self):
        return f"{self.id}--{self.text}"

class Answers(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    question_id = Column(Integer, ForeignKey('question.id'))

    question = relationship('Question', back_populates='answers')
    def __repr__(self):
        return f"({self.id}) -- {self.text}"


class DB():
    def __init__(self):
        engine = create_engine('sqlite:///quiz.db')
        Base.metadata.create_all(engine)
        self.Session= sessionmaker(bind=engine)

    def get_next_question(self, prev_number=0):
        next_number = prev_number + 1
        with self.Session() as session:
            question = session.query(Question).filter_by(number=next_number).first()
        return question

    def get_answers(self, question_id):
        with self.Session() as session:
            answers_list = session.query(Answers).filter_by(question_id=question_id).all()
            return answers_list

db = DB()
# res = db.get_next_question()
# print(res)
# answers = db.get_answers(res.id)
# for answer in answers:
#     print(answer)


























# from sqlalchemy.orm import declarative_base, sessionmaker
# from sqlalchemy import Column, Integer, String, create_engine


# Base = declarative_base()


# class Question(Base):
#     __tablename__ = 'question'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     text = Column(String)
#     number = Column(Integer)

#     # answers = relationship('Answers', back_populates = 'question')
    
#     def __repr__(self):
#         return f"{self.id}--{self.text}"
# class Answers(Base):
#         __tablename__ = 'answers'

#         id = Column(Integer, primary_key=True, autoincrement=True)
#         text = Column(String)
#         # question_id = Column(Integer, ForeignKey('question.id'))

#         question = Column('Question', back_populates = 'answers')

# class DB():
#     def __init__(self):
#         engine = create_engine('sqlite:///quiz.db')
#         Base.metadata.create_all(engine)
#         self.Session= sessionmaker(bind=engine)
#     def get_next_question(self, prev_number = 0):
#         next_number = prev_number + 1
#         with self.Session() as session:
#              question = session.query(Question).filter_by(number = next_number).first()
#         return question
#     def get_answers(self, question_id):
#         with self.Session() as session:
#             question_id = session.query(Answers).filter_by(question_id = question_id).all()
#             return question_id

# db = DB()
# res = db.get_next_question()
# print(res)
# print(db.get_answers(res.id))