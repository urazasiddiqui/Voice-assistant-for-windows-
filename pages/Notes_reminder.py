import customtkinter
from pages.notes import view_notes, add_note, delete_note, show_reminder, insert_reminder
import winsound
import os
import time
from datetime import datetime
import pyttsx3
from playsound import playsound
import threading
import tkinter as tk
from tkinter import messagebox
from pages.database import insert_reminder

def ViewTab(self, parentThirdFrame):
    tabview_3 = customtkinter.CTkTabview(parentThirdFrame, width=900)
    tabview_3.pack(pady=10, padx=10)
    viewAll = tabview_3.add("View All Notes")
    viewReport = tabview_3.add("View All Reminders")

    # View All Notes Tab
    self.ViewTransactionTabLabel = customtkinter.CTkLabel(
        viewAll,
        text="View All Notes",
        compound="left",
        font=customtkinter.CTkFont("Times new roman", size=18, weight="bold"),
    ).grid(row=0, column=0, padx=50, pady=15)

    self.ViewTotalTransactionsLabel = customtkinter.CTkLabel(
        viewAll,
        text="Notes ",
        compound="left",
        font=customtkinter.CTkFont("Times new roman", size=18, weight="bold"),
    )
    self.ViewTotalTransactionsLabel.grid(row=1, column=0, padx=20, pady=5)

    self.viewallScrollFrame = customtkinter.CTkScrollableFrame(
        viewAll,
        corner_radius=25,
        width=760,
        height=600,
        border_width=5,
        fg_color="lightgray",
    )
    self.viewallScrollFrame.grid(row=2, column=0, padx=30, pady=0, sticky="new")

    viewallRefresh(self)

    # View All Reminder Tab
    self.ViewTransactionReportTabLabel = customtkinter.CTkLabel(
        viewReport,
        text="View All Reminders",
        compound="left",
        font=customtkinter.CTkFont("Times new roman", size=18, weight="bold"),
    ).grid(row=0, column=0, padx=50, pady=15)

    self.ViewTotalRemindersLabel = customtkinter.CTkLabel(
        viewReport,
        text="Reminders ",
        compound="left",
        font=customtkinter.CTkFont("Times new roman", size=18, weight="bold"),
    )
    self.ViewTotalRemindersLabel.grid(row=1, column=0, padx=20, pady=5)

    self.viewReminderScrollFrame = customtkinter.CTkScrollableFrame(
        viewReport,
        corner_radius=25,
        width=760,
        height=600,
        border_width=5,
        fg_color="lightgray",
    )
    self.viewReminderScrollFrame.grid(row=2, column=0, padx=30, pady=0, sticky="new")

    viewReminderRefresh(self)
    
    
# refresh reminder
def viewReminderRefresh(self):
    reminders = show_reminder()

    if reminders:  
        for widget in self.viewReminderScrollFrame.winfo_children():
            widget.destroy()

        # Display reminders on the scrollable frame
        for i, (when_time, what_time, noted) in enumerate(reminders):
            # Create labels for reminder details
            when_label = customtkinter.CTkLabel(
                self.viewReminderScrollFrame,
                text=f"When: {when_time}",
                compound="left",
                text_color="black",
                font=customtkinter.CTkFont("Times new roman", size=16)
            )
            when_label.grid(row=i*3, column=0, padx=10, pady=5, sticky="w")

            what_label = customtkinter.CTkLabel(
                self.viewReminderScrollFrame,
                text=f"What: {what_time}",
                compound="left",
                text_color="black",
                font=customtkinter.CTkFont("Times new roman", size=16)
            )
            what_label.grid(row=i*3+1, column=0, padx=10, pady=5, sticky="w")

            time_label = customtkinter.CTkLabel(
                self.viewReminderScrollFrame,
                text=f"At: {noted}",
                compound="left",
                text_color="black",
                font=customtkinter.CTkFont("Times new roman", size=18, weight="bold")
            )
            time_label.grid(row=i*3+2, column=0, padx=10, pady=(5, 20), sticky="w")

        # Update the total reminders label
        self.ViewTotalRemindersLabel.configure(text=f"Total Reminders: {len(reminders)}")

    else:
        print("No reminders found!")
    
    add_button = customtkinter.CTkButton(
            self.viewReminderScrollFrame,
            text="Add reminder",
            command=lambda: add_reminder(self),  # Pass self to access the instance
            fg_color="teal"
        )
    add_button.grid(row=0, column=1, padx=10, pady=10)
    
    delete_button = customtkinter.CTkButton(
            self.viewReminderScrollFrame,
            text="Delete Reminder",
            command=lambda: delete_reminder(self),
            fg_color="teal"
        )
    delete_button.grid(row=0, column=2, padx=10, pady=10)
    
    
    refresh_button = customtkinter.CTkButton(
            self.viewReminderScrollFrame,
            text="Refresh",
            command=lambda: viewReminderRefresh(self),
            fg_color="teal"
        )
    refresh_button.grid(row=0, column=3, padx=10, pady=10)

def viewallRefresh(self):
    # Retrieve notes from the database using view_notes function
    notes = view_notes()

    if notes is not None:  # Check if notes is not None
        # Clear existing labels
        for widget in self.viewallScrollFrame.winfo_children():
            widget.destroy()

        # Display notes on the scrollable frame
        for i, (title, note) in enumerate(notes):
            # Create labels for title and note content
            title_label = customtkinter.CTkLabel(
                self.viewallScrollFrame,
                text=f"Title: {title}",
                compound="left",
                text_color="black",
                font=customtkinter.CTkFont("Times new roman", size=18, weight="bold")
            )
            title_label.grid(row=i*2, column=0, padx=10, pady=5, sticky="w")

            note_label = customtkinter.CTkLabel(
                self.viewallScrollFrame,
                text=f"Note: {note}",
                compound="left",
                text_color="black",
                font=customtkinter.CTkFont("Times new roman", size=18)
            )
            note_label.grid(row=i*2+1, column=0, padx=10, pady=5, sticky="w")

        # Update the total notes label
        self.ViewTotalTransactionsLabel.configure(text=f"Total Notes: {len(notes)}")

    else:
        print("No notes found!")
    
    add_button = customtkinter.CTkButton(
            self.viewallScrollFrame,
            text="Add note",
            command=add_note,
            fg_color="teal"
        )
    add_button.grid(row=0, column=1, padx=10, pady=10)
    del_button = customtkinter.CTkButton(
            self.viewallScrollFrame,
            text="Delete notes",
            command=delete_note,
            fg_color="teal"
        )
    del_button.grid(row=0, column=2, padx=10, pady=10)
    refresh_button = customtkinter.CTkButton(
            self.viewallScrollFrame,
            text="Refresh",
            command=lambda: viewallRefresh(self),
            fg_color="teal"
        )
    refresh_button.grid(row=0, column=3, padx=10, pady=10)
    
    
    


def add_reminder(self):
    def submit_reminder():
        title = title_entry.get()
        reminder_date = date_entry.get()
        reminder_time = time_entry.get()

        try:
            reminder_datetime = datetime.strptime(reminder_date + " " + reminder_time, "%Y-%m-%d %H:%M")
            current_datetime = datetime.now()

            if reminder_datetime < current_datetime:
                messagebox.showerror("Error", "Please enter a future date and time for the reminder.")
                return

            insert_reminder( reminder_datetime,title)
            messagebox.showinfo("Success", "Reminder set successfully!")
            reminder_popup.destroy()
            viewReminderRefresh(self)
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time.")

    reminder_popup = tk.Toplevel()
    reminder_popup.title("Add Reminder")

    title_label = tk.Label(reminder_popup, text="Reminder Note:")
    title_label.grid(row=0, column=0, padx=10, pady=10)
    title_entry = tk.Entry(reminder_popup)
    title_entry.grid(row=0, column=1, padx=10, pady=10)

    date_label = tk.Label(reminder_popup, text="Reminder Date (YYYY-MM-DD):")
    date_label.grid(row=1, column=0, padx=10, pady=10)
    date_entry = tk.Entry(reminder_popup)
    date_entry.grid(row=1, column=1, padx=10, pady=10)

    time_label = tk.Label(reminder_popup, text="Reminder Time (HH:MM):")
    time_label.grid(row=2, column=0, padx=10, pady=10)
    time_entry = tk.Entry(reminder_popup)
    time_entry.grid(row=2, column=1, padx=10, pady=10)

    submit_button = tk.Button(reminder_popup, text="Submit", command=submit_reminder)
    submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

def delete_reminder(self):
    def submit_delete():
        reminder_id = delete_id_entry.get()

        try:
            reminder_id = int(reminder_id)
            delete_reminder(reminder_id)  
            messagebox.showinfo("Success", f"Reminder with ID {reminder_id} deleted successfully!")
            delete_popup.destroy()
            viewReminderRefresh(self)  
        except ValueError:
            messagebox.showerror("Error", "Invalid Reminder ID. Please enter a numeric ID.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete reminder: {e}")

    delete_popup = tk.Toplevel()
    delete_popup.title("Delete Reminder")

    delete_id_label = tk.Label(delete_popup, text="Enter Reminder ID to Delete:")
    delete_id_label.grid(row=0, column=0, padx=10, pady=10)
    delete_id_entry = tk.Entry(delete_popup)
    delete_id_entry.grid(row=0, column=1, padx=10, pady=10)

    submit_button = tk.Button(delete_popup, text="Delete", command=submit_delete)
    submit_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)