import datetime
import customtkinter
from PIL import Image
import os
import sqlite3

# Database setup
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table(conn):
    if conn is None:
        print("Error: No connection to the database.")
        return
    try:
        sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        password text NOT NULL
                                    );"""
        cursor = conn.cursor()
        cursor.execute(sql_create_users_table)
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def load_image(path, width, height):
    try:
        return customtkinter.CTkImage(
            light_image=Image.open(path).resize((width, height), Image.ANTIALIAS),
            size=(width, height),
        )
    except FileNotFoundError:
        print(f"Error: Image file not found at path: {path}")
        return None
    except Exception as e:
        print(f"Error opening image: {e}")
        return None

def change_password(conn):
    # Functionality to change the password
    current_password = current_password_entry.get()
    new_password = new_password_entry.get()
    confirm_password = confirm_password_entry.get()

    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE id=1")  # Assuming single user with id=1
    stored_password = cursor.fetchone()

    if stored_password and stored_password[0] == current_password:
        if new_password == confirm_password:
            cursor.execute("UPDATE users SET password = ? WHERE id = 1", (new_password,))
            conn.commit()
            print("Password changed successfully")
        else:
            print("New passwords do not match")
    else:
        print("Current password is incorrect")

def change_username(conn):
    # Functionality to change the username
    new_username = new_username_entry.get()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = ? WHERE id = 1", (new_username,))
    conn.commit()
    print("Username changed successfully")

def helpTab(parentFourth_Frame):
    tabview_4 = customtkinter.CTkTabview(parentFourth_Frame, width=900)
    tabview_4.pack(pady=10, padx=10)
    LicenceTab = tabview_4.add("User profile")
    HelpTab = tabview_4.add("Help")
    DeveloperTab = tabview_4.add("Developer")

    # ? Help Tab - Information about Software

    customtkinter.CTkLabel(
        HelpTab,
        text="Voice based Virtual Assistance for Windows ",
        font=customtkinter.CTkFont("Times new roman", size=22, weight="bold"),
    ).pack(pady=10)

    customtkinter.CTkLabel(
        HelpTab,
        text="""The Voice Based Virtual Assistant for Window  is an enormous improvement ahead in the field of professional productivity. Its voice-based personal assistant integrates quickly into workplace environments, offering users with a powerful tool for tasks like searching, making reminders, and taking notes, all using natural voice commands. The assistant comprehends freeform interactions, deducing user intent from verbal or written input and precisely carrying out their instructions. It transforms human-computer interaction and improves company efficiency by bridging the gap between users and their digital tasks. The deep learning-based approach of the Window Assistant not only streamlines daily operations, but also creates a dynamic and inclusive environment in which users can seamlessly navigate their digital workplace, ultimately changing the user experience in computer environments..""",
    ).pack(pady=5)

    # Software Holders informations
    customtkinter.CTkLabel(
        HelpTab,
        text="Software Holders",
        font=customtkinter.CTkFont(size=12, weight="bold"),
    ).pack(pady=5)

    # stakeholder
    linkedin_label = customtkinter.CTkLabel(HelpTab, text="Stakeholder: Air University")
    linkedin_label.pack(pady=2)

    # author
    name_label = customtkinter.CTkLabel(HelpTab, text="Author/developer: Umair Raza, Sharjeel Amir, Nehal Salman")
    name_label.pack(pady=2)

   
    
    customtkinter.CTkLabel(
        LicenceTab,
        text=f"Welcome!",
        font=customtkinter.CTkFont("Times new roman", size=22, weight="bold"),
    ).pack(pady=10)
    # get current year
    currentyear = datetime.date.today().year
    

    # Add Change Username functionality
    customtkinter.CTkLabel(
        LicenceTab,
        text="Change Username",
        font=customtkinter.CTkFont("Times new roman", size=18, weight="bold"),
    ).pack(pady=10)
    global new_username_entry
    new_username_entry = customtkinter.CTkEntry(LicenceTab, placeholder_text="New Username")
    new_username_entry.pack(pady=5)
    change_username_button = customtkinter.CTkButton(LicenceTab,fg_color="teal", text="Change Username", command=lambda: change_username(conn))
    change_username_button.pack(pady=5)

    # Add Change Password functionality
    customtkinter.CTkLabel(
        LicenceTab,
        text="Change Password",
        font=customtkinter.CTkFont("Times new roman", size=18, weight="bold"),
    ).pack(pady=10)
    global current_password_entry, new_password_entry, confirm_password_entry
    current_password_entry = customtkinter.CTkEntry(LicenceTab, placeholder_text="Current Password", show="*")
    current_password_entry.pack(pady=5)
    new_password_entry = customtkinter.CTkEntry(LicenceTab, placeholder_text="New Password", show="*")
    new_password_entry.pack(pady=5)
    confirm_password_entry = customtkinter.CTkEntry(LicenceTab, placeholder_text="Confirm New Password", show="*")
    confirm_password_entry.pack(pady=5)
    change_password_button = customtkinter.CTkButton(LicenceTab,fg_color="teal", text="Change Password", command=lambda: change_password(conn))
    change_password_button.pack(pady=5)

    # ? Developer Tab - Information
    customtkinter.CTkLabel(
        DeveloperTab,
        text="Developer Profile",
        font=customtkinter.CTkFont("Times new roman", size=15, weight="bold"),
    ).pack(pady=10)

    customtkinter.CTkLabel(DeveloperTab, text="Name: Umair Raza, Sharjeel Amir, Nehal Salman - (Developers)").pack(
        pady=5
    )



# Database initialization
database = os.path.join(os.path.dirname(__file__), "memory.db")
print(f"Database path: {database}")  # Debugging line to check the path
conn = create_connection(database)
if conn:
    create_table(conn)
else:
    print("Error: Unable to establish a database connection.")
