import sqlite3
import datetime
def create_connection():
    connection = sqlite3.connect("pages/memory.db")
    return connection

def create_table():
    con = create_connection()
    cur = con.cursor()
    
    cur.execute('''CREATE TABLE IF NOT EXISTS question_and_answer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT,
                    answer TEXT)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS Task (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT,
                    status TEXT)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS Note (
                note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                note TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Reminder (
                    reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    when_time TEXT,
                    what_time TEXT,
                    noted TEXT)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS user_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                command_keyword TEXT)''')
    
        
    con.commit()
    con.close()

def insert_question_and_answer(question, answer):
    con = create_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO question_and_answer (question, answer) VALUES (?, ?)", (question, answer))
    con.commit()
    con.close()

def insert_task(task, status):
    con = create_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO Task (task, status) VALUES (?, ?)", (task,status ))
    con.commit()
    con.close()

def insert_note(title, note):
    con = create_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO Note (title, note) VALUES (?, ?)", (title, note))
    con.commit()
    con.close()

def insert_reminder( what_time,noted):
    con = create_connection()
    cur = con.cursor()
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute("INSERT INTO Reminder (when_time, what_time, noted) VALUES (?, ?, ?)", (current_time, what_time, noted))
    con.commit()
    con.close()
    
def delete_reminder(reminder_id):
    """
    Deletes a reminder from the database by its reminder_id.
    """
    con = create_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM Reminder WHERE reminder_id = ?", (reminder_id,))
    con.commit()
    con.close()    
    
def save_query_to_db(query, keyword):
    con = create_connection()  # Connect to your SQLite database
    cur = con.cursor()
    cur.execute("INSERT INTO user_queries (query, command_keyword) VALUES (?, ?)", (query, keyword))
    con.commit()
    con.close()

def get_questions_and_answers():
    con = create_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM question_and_answer")
    return cur.fetchall()


def get_command_for_keyword(keyword):
    con = create_connection()
    cur = con.cursor()
    
    # Fetch any query that has the keyword in it
    cur.execute("SELECT query FROM user_queries WHERE command_keyword=?", (keyword,))
    result = cur.fetchone()
    
    con.close()
    
    if result:
        return result[0]
    else:
        return None


create_table()
