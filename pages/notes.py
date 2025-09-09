
import sqlite3
import pyttsx3
import datetime
import threading
import speech_recognition as sr
from pages.database import insert_note, insert_reminder

engine = pyttsx3.init()

def speak(text_to_speak):
    engine.say(text_to_speak)
    engine.runAndWait()

notes = {}

def get_voice_input(prompt):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text.strip()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError:
        print("Sorry, there was an error with the speech recognition service.")
        return ""

def add_note():
    speak("Please say the title of the note")
    title = get_voice_input("Please say the title of the note:")
    speak("Please say the note:")
    note = get_voice_input("Please say the note")
    
    
    if title and note:
        notes[title] = note
        print("Note added successfully!")
        speak("Note added successfully")
        insert_note(title, note)
    else:
        print("Please provide both title and note.")
        speak("Please provide both title and note.")

def view_notes():
    try:
        conn = sqlite3.connect('pages/memory.db')
        c = conn.cursor()
        c.execute("SELECT title, note FROM note")
        rows = c.fetchall()
        if rows:
            return rows  # Return the notes if they exist
        else:
            print("No notes found!")
            return []  # Return an empty list if no notes are found
    except sqlite3.Error as e:
        print("Error:", e)
        return []  # Return an empty list if there's an error
    finally:
        conn.close()



def delete_note():
    try:
        conn = sqlite3.connect('pages/memory.db')
        c = conn.cursor()
        speak("Speak note title to delete")
        title = get_voice_input("speak note title to delete: ")
        c.execute("DELETE FROM note WHERE title=?", (title,))
        conn.commit()
        print("Note deleted successfully!")
        speak("Note deleted successfully")
    except Exception as e:
        print("Error:", e)
        print("An error occurred while deleting the note.")


def add_reminder():
    title = input("Enter reminder note: ")
    reminder_date = input("Enter reminder date (YYYY-MM-DD): ")
    reminder_time = input("Enter reminder time (HH:MM): ")
    
    try:
        reminder_datetime = datetime.datetime.strptime(reminder_date + " " + reminder_time, "%Y-%m-%d %H:%M")
        current_datetime = datetime.datetime.now()
        
        if reminder_datetime < current_datetime:
            print("Please enter a future date and time for the reminder.")
            return
        
        insert_reminder(title, reminder_datetime)
        print("Reminder set successfully!")
    except ValueError:
        print("Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time.")

def check_reminders():
    conn = sqlite3.connect('pages/memory.db')
    c = conn.cursor()
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # Fetch upcoming reminders from the database
    c.execute("SELECT * FROM reminder WHERE what_time > ? ORDER BY what_time ASC", (current_datetime,))
    reminders = c.fetchall()

    if reminders:
        print("Upcoming Reminders:")
        for reminder in reminders:
            reminder_id, reminder_text, reminder_time = reminder
            print(f"Reminder: {reminder_text} at {reminder_time}")

            # Calculate time difference to schedule alert
            reminder_datetime = datetime.datetime.strptime(reminder_time, "%Y-%m-%d %H:%M")
            time_diff_seconds = (reminder_datetime - datetime.datetime.now()).total_seconds()

            # Schedule alert using threading.Timer
            if time_diff_seconds > 0:
                timer = threading.Timer(time_diff_seconds, alert_reminder, args=[reminder_text])
                timer.start()

    conn.close()
def show_reminder():
    try:
        conn = sqlite3.connect('pages/memory.db')
        c = conn.cursor()
        c.execute("SELECT when_time,what_time, noted FROM reminder")
        rows = c.fetchall()
        if rows:
            return rows  # Return the notes if they exist
        else:
            print("No notes found!")
            return []  # Return an empty list if no notes are found
    except sqlite3.Error as e:
        print("Error:", e)
        return []  # Return an empty list if there's an error
    finally:
        conn.close()
# Function to alert the user when the reminder time is reached
def alert_reminder(reminder_text):
    print(f"ALERT: {reminder_text}")

if __name__ == "__main__": 
    # add_note()
    view_notes()
    # delete_note()
    # add_reminder()
    # check_reminders()
    # time.sleep(60)
