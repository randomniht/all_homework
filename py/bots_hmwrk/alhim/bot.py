from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine



Base = declarative_base()


class Notes(Base):
    __tablename__ = 'note'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    text = Column(String)
    grade = Column(Integer)
    def __repr__(self):
        return f"{self.id}--{self.title}"







# Add note


class DB:
    def __init__(self):
        engine = create_engine('sqlite:///note.db')
        Base.metadata.create_all(engine)
        self.Session= sessionmaker(bind=engine)
    def add_note(self,title,text,grade):
        with self.Session() as session:
            note = Notes(title = title, text = text, grade = grade)
            session.add(note)
            session.commit()
    def get_note(self):
        with self.Session() as session:
            notes = session.query(Notes).all()
            return notes
    def del_by_id(self,id):
       with self.Session() as session:
            notes = session.query(Notes).filter_by(id = id).first()
            if notes:
                session.delete(notes)
                session.commit() 
    def like_dy_id(self,id):
        with self.Session() as session:
            notes = session.query(Notes).filter_by(id = id).first()
            if notes:
                notes.grade += 1
                session.commit()



db = DB()

while True:
    user = int(input('1-Добавить заметку\n' \
    '2-посмотреть заметки\n' \
    '3-удалить\n' \
    '4-оценить\n'
    '5-exit\n'))
    if user == 1:
        name = input('name = ')
        text = input('text = ')
        grade = 0
        db.add_note(name,text,grade)
    elif user == 2:
        notes = db.get_note()
        for note in notes:
            print( f'({note.id})',note.title, note.text, note.grade)
    elif user == 3:
        note_id = int(input('id? '))
        db.del_by_id(note_id)
    elif user == 4:
        id_ask = int(input('Id? '))
        db.like_dy_id(id=id_ask)
    else:
        break

