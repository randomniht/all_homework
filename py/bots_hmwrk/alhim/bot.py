from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine



Base = declarative_base()


class Notes(Base):
    __tablename__ = 'note'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    text = Column(String)
    def __repr__(self):
        return f"{self.id}--{self.title}"







# Add note


class DB:
    def __init__(self):
        engine = create_engine('sqlite:///note.db')
        self.Session= sessionmaker(bind=engine)
    def add_note(self,title,text):
        with self.Session() as session:
            note = Notes(title = title, text = text)
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


db = DB()

while True:
    user = int(input('1-Добавить заметку\n' \
    '2-посмотреть заметки\n' \
    '3-удалить\n' \
    '4-exit\n'))
    if user == 1:
        name = input('name = ')
        text = input('text = ')
        db.add_note(name,text)
    elif user == 2:
        notes = db.get_note()
        for note in notes:
            print( f'({note.id})',note.title, note.text)
    elif user == 3:
        note_id = int(input('id? '))
        db.del_by_id(note_id)
    else:
        break

