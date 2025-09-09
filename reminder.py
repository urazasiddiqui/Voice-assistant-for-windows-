import sqlite3
from datetime import datetime
import threading
import time
import winsound
import tkinter as tk
from tkinter import messagebox
import queue

# Function to set up database connection and create table if not exists
def setup_database():
    conn = sqlite3.connect('pages/memory.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminder (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            when_time TIMESTAMP,
            what_time TIMESTAMP,
            noted TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to add reminder
def add_reminder(noted, what_time_str):
    try:
        what_time = datetime.strptime(what_time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Please enter the time in YYYY-MM-DD HH:MM:SS format.")
        return
    
    if noted and what_time:
        when_time = datetime.now()
        conn = sqlite3.connect('reminder.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reminders (when_time, what_time, noted) VALUES (?, ?, ?)", 
                       (when_time, what_time, noted))
        conn.commit()
        conn.close()
        print("Reminder added successfully!")
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
    else:
        print("Please enter all required fields.")

# Function to show reminders
def show_reminders():
    conn = sqlite3.connect('pages/memory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reminder")
    reminders = cursor.fetchall()
    conn.close()
    
    for reminder in reminders:
        print(f"Reminder: {reminder[3]} | When: {reminder[1]} | What: {reminder[2]}")

# Function to check reminders in the background
def check_reminders(reminder_queue):
    while True:
        now = datetime.now()
        conn = sqlite3.connect('pages/memory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reminder WHERE what_time <= ?", (now,))
        reminders = cursor.fetchall()
        for reminder in reminders:
            reminder_queue.put(reminder)
            cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder[0],))
        conn.commit()
        conn.close()
        time.sleep(60)

def show_reminder_alert(reminder):
    messagebox.showinfo("Reminder Alert", f"Reminder: {reminder[3]}")
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)

# Set up the database
setup_database()

# Create a dummy Tkinter root window to handle message boxes
root = tk.Tk()
root.withdraw()  # Hide the root window

# Create a queue to handle reminders from the background thread
reminder_queue = queue.Queue()

# Start the background thread to check reminders
def start_check_thread():
    check_thread = threading.Thread(target=check_reminders, args=(reminder_queue,), daemon=True)
    check_thread.start()

start_check_thread()

# Periodically check the queue for reminders and show alert
def check_queue():
    while not reminder_queue.empty():
        reminder = reminder_queue.get()
        show_reminder_alert(reminder)
    root.after(1000, check_queue)

check_queue()

# Sample interaction
if __name__ == "__main__":
    while True:
        action = input("Enter 'add' to add a reminder, 'show' to show reminder, or 'exit' to exit: ").lower()
        if action == 'add':
            noted = input("Enter Reminder: ")
            what_time = input("Enter Reminder Time (YYYY-MM-DD HH:MM:SS): ")
            add_reminder(noted, what_time)
        elif action == 'show':
            show_reminders()
        elif action == 'exit':
            break
        else:
            print("Invalid action. Please try again.")
