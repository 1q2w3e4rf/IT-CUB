import sqlite3

class Db():
        
    def register(self, chat_id, firstname, secondname, surname, isSiud = False, certNo = None):
        with sqlite3.connect('Base.db', timeout=30) as db:
            cursor = db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS users (chat_id INTEGER PRIMARY KEY, firstname TEXT, secondname TEXT, surname TEXT, isSiud BOOLEAN, certNo TEXT)')
            cursor.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)', (chat_id, firstname, secondname, surname, isSiud, certNo))
            db.commit()
    
    def register_pupil(self, cert, firstname, secondname, surname):
        with sqlite3.connect('Base.db', timeout=30) as db:
            cursor = db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS pupils (cert TEXT PRIMARY KEY, firstname TEXT, secondname TEXT, surname TEXT)')
            cursor.execute('INSERT INTO pupils VALUES(?, ?, ?, ?)', (cert, firstname, secondname, surname))
            db.commit()

    def get_user_data(self, chat_id):
        with sqlite3.connect('Base.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM users WHERE chat_id = ?', (chat_id,))
            return cursor.fetchone()

    def toRoboty(self, cert):
        with sqlite3.connect('Base.db') as db:
            cursor = db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS roboty (key INTEGER PRIMARY KEY AUTOINCREMENT, cert TEXT)')
            cursor.execute('INSERT INTO roboty VALUES(?, ?)', (None, cert))
            db.commit()


    def toSisadm(self, cert):
        with sqlite3.connect('Base.db') as db:
            cursor = db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS sisadmy (key INTEGER PRIMARY KEY AUTOINCREMENT, cert TEXT)')
            cursor.execute('INSERT INTO sisadmy VALUES(?, ?)', (None, cert))
            db.commit()
