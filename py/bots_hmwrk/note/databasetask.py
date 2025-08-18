import sqlite3
from app.draft_handl import config

db = sqlite3.connect('tasker.db')

c = db.cursor()
# c.execute("""
# CREATE TABLE note (
#         tg_id integer,
#         name text
          
#           )

# """)


c.execute(f"INSERT INTO articles VALUES({config.user_id}, {config.name})")

db.commit()

db.close()