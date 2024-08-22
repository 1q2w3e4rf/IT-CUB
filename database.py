import sqlite3

class Db():
        
    def register(self, chat_id, firstname, secondname, surname):
        with sqlite3.connect('Base.db', timeout=30) as db:
            cursor = db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS users (chat_id STRING PRIMARY KEY, firstname TEXT, secondname TEXT, surname TEXT)')
            cursor.execute('INSERT OR REPLACE INTO users VALUES(?, ?, ?, ?)', (chat_id, firstname, secondname, surname))
            db.commit()

    def register_pupil(self, cert, firstname, secondname, surname):
        with sqlite3.connect('Base.db', timeout=30) as db:
            cursor = db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS pupils (cert TEXT PRIMARY KEY, firstname TEXT, secondname TEXT, surname TEXT)')
            cursor.execute('INSERT INTO pupils VALUES(?, ?, ?, ?)', (cert, firstname, secondname, surname))
            db.commit()
    def regiser_pazents(self, firstname, secondname, surname):
        with sqlite3.connect('Base.db', timeout=30) as db:
            cursor = db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS pazents (nume INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, secondname TEXT, surname TEXT)')
            cursor.execute('INSERT INTO pazents (firstname, secondname, surname) VALUES(?, ?, ?)', (firstname, secondname, surname))
            db.commit()
            cursor.execute('SELECT nume FROM pazents ORDER BY nume DESC LIMIT 1')
            return cursor.fetchone()[0]
    
    def get_pupils(self,cert):
        with sqlite3.connect('Base.db', timeout=30) as db:
            cursor = db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS pupils (cert TEXT PRIMARY KEY, firstname TEXT, secondname TEXT, surname TEXT)')
            cursor.execute('SELECT * FROM pupils WHERE cert = ?', (cert,))
            return cursor.fetchone()
    def get_user_data(self, chat_id):
            with sqlite3.connect('Base.db', timeout=30) as db:
                cursor = db.cursor()
                cursor.execute('CREATE TABLE IF NOT EXISTS users (chat_id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT, secondname TEXT, surname TEXT)')
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

    def toPython(self, cert):
        with sqlite3.connect('Base.db') as db:
            cursor = db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS python (key INTEGER PRIMARY KEY AUTOINCREMENT, cert TEXT)')
            cursor.execute('INSERT INTO python VALUES(?, ?)', (None, cert))
            db.commit()

    def toJava(self, cert):
        with sqlite3.connect('Base.db') as db:
            cursor = db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS java (key INTEGER PRIMARY KEY AUTOINCREMENT, cert TEXT)')
            cursor.execute('INSERT INTO java VALUES(?, ?)', (None, cert))
            db.commit()
    
    def toMobile(self, cert):
        with sqlite3.connect('Base.db') as db:
            cursor = db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS mobile (key INTEGER PRIMARY KEY AUTOINCREMENT, cert TEXT)')
            cursor.execute('INSERT INTO mobile VALUES(?, ?)', (None, cert))
            db.commit()

    def toAlglog(self, cert):
        with sqlite3.connect('Base.db') as db:
            cursor = db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS alglog (key INTEGER PRIMARY KEY AUTOINCREMENT, cert TEXT)')
            cursor.execute('INSERT INTO alglog VALUES(?, ?)', (None, cert))
            db.commit()