import customtkinter
from components.MessageBox import (
    exit_application,
    show_thanks,
    show_error,
    show_delete_warning,
)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import cv2
import face_recognition
import numpy as np
import tkinter.font as tkFont
import os
import sqlite3
import datetime
import json
from tkinter import messagebox,PhotoImage
from reminder import start_check_thread,check_queue
import ssl
import string
import random
from pages.helpTab import helpTab
from customtkinter import StringVar
from customtkinter import CTkCheckBox
from pages.Notes_reminder import ViewTab, viewallRefresh
from pages.home import Home_Tab
from pages.signup import signup_main
from pages.login import LoginApp
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from pages.offline import offline_interface
from pages.summary_rephase import (
   SummaryTab
)

from DatabaseHandler import DatabaseHandler

class LoginPage(customtkinter.CTkFrame):
    
    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.config(show="*")

    def __init__(self, parent, db_connection, on_login_success):    #changes
        super().__init__(parent)
        self.parent = parent
        self.db_connection = db_connection
        self.on_login_success = on_login_success
        self.username_placeholder = "Enter Username"
        self.password_placeholder = "Enter Password"
        
    
        title_text_label = customtkinter.CTkLabel(self, text="VoiceMate", font=("Arial", 20), text_color="black")
        title_text_label.grid(row=0, column=0, sticky="nw", padx=(60, 0), pady=(20, 0))

    
        # Login frame on the left side
        self.login_frame = customtkinter.CTkFrame(self)
        self.login_frame.grid(row=0, column=0, padx=(150, 0), pady=150, sticky="nsew")

        # Login frame title
        label_font = ('Arial Black', 20)
        self.title_label = customtkinter.CTkLabel(self.login_frame, text="Sign In", text_color="black",font=label_font)
        self.title_label.grid(row=0, column=0, padx=(10, 200), pady=(20,3), sticky="e")

        # Username Label in login frame
        self.username_label = customtkinter.CTkLabel(self.login_frame, text="Username:",text_color="black")
        self.username_label.grid(row=1, column=0, padx=(20, 200), pady=3, sticky="e")

        # Username Entry in login frame (on the next row)
        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=180)
        self.username_entry.grid(row=2, column=0, padx=(20, 30), pady=3, sticky="ew")
        self.username_entry.insert(0, self.username_placeholder)
        self.username_entry.bind("<FocusIn>", self.clear_placeholder)
        self.username_entry.bind("<FocusOut>", self.add_placeholder)

        # Password Label and Entry in login frame
        self.password_label = customtkinter.CTkLabel(self.login_frame, text="Password:", text_color="black")
        self.password_label.grid(row=3, column=0, padx=(20, 200), pady=3, sticky="e")
        self.password_entry = customtkinter.CTkEntry(self.login_frame, show="*", width=180)
        self.password_entry.grid(row=4, column=0, padx=(20, 30), pady=3, sticky="ew")
        self.password_entry.insert(0, self.password_placeholder)
        self.password_entry.bind("<FocusIn>", self.clear_placeholder)
        self.password_entry.bind("<FocusOut>", self.add_placeholder)

   

        # Login Button in login frame
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login,fg_color="teal",border_color="white",border_width=1)
        self.login_button.grid(row=5, column=0, columnspan=2, pady=20)

        # Face Recognition Button
        self.face_recognition_button = customtkinter.CTkButton(
            self.login_frame, text="Login with Face", corner_radius=5, command=self.login_with_face, fg_color="teal"
        )
        self.face_recognition_button.grid(row=6, column=0, columnspan=2, pady=10)
        
        # self.forget_password = customtkinter.CTkButton(self.login_frame, text="forget Password", command=self.forget_password,fg_color="teal",border_color="white",border_width=1)
        # self.forget_password.grid(row=7, column=0, columnspan=2, pady=20)
        self.forget_password_link = customtkinter.CTkLabel(self.login_frame, text="Forgot Password", text_color="black", cursor="hand2", fg_color=None, font=('Arial', 10))
        self.forget_password_link.grid(row=7, column=0, columnspan=2, pady=(1,50),padx=(130,10))
        self.forget_password_link.bind("<Button-1>", self.forget_password)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        # Signup frame on the right side
        self.logup_frame = customtkinter.CTkFrame(self, fg_color="teal")
        self.logup_frame.grid(row=0, column=1, padx=(0,150), pady=150, sticky="nsew")
        
        # New Username Label and Entry in signup frame
        self.new_username_label = customtkinter.CTkLabel(self.logup_frame, text="Welcome to login",font=('Arial Black', 24),text_color="white")
        self.new_username_label.grid(row=1, column=0, padx=25, pady=(80,20), sticky="e")
        

        # New Password Label and Entry in signup frame
        self.new_password_label = customtkinter.CTkLabel(self.logup_frame, text="Don't have an account?",font=('Arial', 18),text_color="white")
        self.new_password_label.grid(row=2, column=0, padx=(10,40), pady=10, sticky="e")
        
        # Signup Button in signup frame

        self.signup_button = customtkinter.CTkButton(self.logup_frame, text="Sign Up", command=signup_main,fg_color="teal",border_color="white",border_width=1)
        self.signup_button.grid(row=3, column=0, columnspan=2, pady=(20,10))

        
        # offline button
    #     self.Offline_button = customtkinter.CTkLabel(
    #         self.logup_frame,
    #         # text="swtich to Offline mode",
    #         text_color="white",
    #         cursor="hand2",
    #         fg_color=None,  
    #         font=('Arial', 10)
    #     )
    #     self.Offline_button.grid(row=4, column=0, pady=(1,50),padx=(20,10))
    #     self.Offline_button.bind("<Button-1>", self.switch_to_offline_mode)
        
    # def switch_to_offline_mode(self, event=None):
    #     """Switches to the offline mode interface."""
    #     self.parent.destroy()  # Close the current login window
    #     offline_interface()     
       

    def forget_password(self, event=None):
        reset_window = customtkinter.CTkToplevel(self)
        reset_window.title("Forget Password")

        title_text_label = customtkinter.CTkLabel(
            reset_window, text="VoiceMate", font=("Arial", 20), text_color="black"
        )
        title_text_label.grid(row=0, column=0, columnspan=2, sticky="nw", padx=20, pady=15)

    # Reset password frame
        self.reset_password = customtkinter.CTkFrame(reset_window, fg_color="teal")
        self.reset_password.grid(row=0, column=1, padx=80, pady=70, sticky="nsew")

        forget_label = customtkinter.CTkLabel(
            self.reset_password, text="Forget Password", font=('Arial', 20), text_color="white"
        )
        forget_label.grid(row=1, column=0, columnspan=2, padx=(10, 70), pady=10)

        username_label = customtkinter.CTkLabel(
            self.reset_password, text="Username:", text_color="white"
        )
        username_label.grid(row=2, column=0, padx=(10, 0), pady=10)

        # Username Entry
        username_entry = customtkinter.CTkEntry(self.reset_password)
        username_entry.grid(row=2, column=1, padx=(10, 10), pady=10)

        email_label = customtkinter.CTkLabel(
            self.reset_password, text="Email:", text_color="white"
        )
        email_label.grid(row=3, column=0, padx=10, pady=10)

        # Email Entry
        email_entry = customtkinter.CTkEntry(self.reset_password)
        email_entry.grid(row=3, column=1, padx=10, pady=10)

        ssl._create_default_https_context = ssl._create_unverified_context

        # Function to generate a random password
        def generate_password(length=8):
            characters = string.ascii_letters + string.digits + string.punctuation
            return ''.join(random.choice(characters) for _ in range(length))

        # Function to update the user's password in the database
        def update_password_in_database(username, new_password):
            conn = sqlite3.connect('pages/memory.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
            conn.commit()
            conn.close()

        # Function to send email using Gmail SMTP
        def send_mail_using_smtp(username, to_email, new_password):
            conn = sqlite3.connect('pages/memory.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND email = ?", (username, to_email))
            user = cursor.fetchone()

            if user:
                sender_email = "212129@students.au.edu.pk"  
                sender_password = "olkf wdfg xbku mryo"  
                subject = "Password Reset for VoiceMate"
                body = f"Hello {username},\n\nYour new password is: {new_password}\n\nPlease log in and change your password."

                # Create the email
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = to_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                try:
                    # Connect to the Gmail SMTP server
                    with smtplib.SMTP('smtp.gmail.com', 587) as server:
                        server.starttls()
                        server.login(sender_email, sender_password)
                        server.send_message(msg)
                        print("Email sent successfully!")
                except Exception as e:
                    print("Failed to send email:", str(e))
            else:
                print("Username and/or email not found in the database.")

            conn.close()

        # Function to reset password
        def reset_password(username, email):
            conn = sqlite3.connect('pages/memory.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND email = ?", (username, email))
            user = cursor.fetchone()

            if user:
                new_password = generate_password()
                update_password_in_database(username, new_password)
                send_mail_using_smtp(username, email, new_password)
                messagebox.showinfo("Success", "Password reset instructions sent to your email.")
            else:
                messagebox.showerror("Error", "Username or email not found.")

            conn.close()

        # Submit action
        def submit_action():
            reset_password(username_entry.get(), email_entry.get())

        # Reset Button
        reset_button = customtkinter.CTkButton(
            self.reset_password,
            text="Reset Password",
            fg_color="teal",
            border_color="white",
            border_width=1,
            command=submit_action
        )
        reset_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


    def clear_placeholder(self, event):
        widget = event.widget
        if widget.get() in [self.username_placeholder, self.password_placeholder]:
            widget.delete(0, 'end')
            if widget == self.password_entry:
                widget.config(show="*")

    def add_placeholder(self, event):
        widget = event.widget
        if widget == self.username_entry and not widget.get():
            widget.insert(0, self.username_placeholder)
        elif widget == self.password_entry and not widget.get():
            widget.insert(0, self.password_placeholder)
            widget.config(show="")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            # Establish database connection
            DB_PATH = os.path.join(os.path.dirname(__file__), "pages/memory.db")
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
                user_data = cursor.fetchone()

            if user_data:
                
                self.on_login_success()
            else:
                
                messagebox.showerror("Login Failed", "Invalid username or password")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error accessing the database: {e}")
        if username == self.username_placeholder or password == self.password_placeholder:
            show_error("Login Failed","Please enter valid credentials.")
        else:
            # Replace with actual login logic
            print(f"Logging in with username: {username}, password: {password}")
            # self.on_login_success()


    def capture_face(self):
        """Captures a face image from the webcam for face recognition login."""
        cap = cv2.VideoCapture(0)  # Start the webcam

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        while True:
            ret, frame = cap.read()  # Read frame from webcam
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw rectangle around face
                face = frame[y:y + h, x:x + w]  # Crop the face region

            cv2.imshow('Press q to Face Capture', frame)  # Display the frame

            # Press 'q' to capture the face
            if cv2.waitKey(1) & 0xFF == ord('q'):
                if faces is not None and len(faces) > 0:
                    self.captured_face = cv2.resize(face, (150, 150))  # Resize the captured face to a fixed size
                break

        cap.release()
        cv2.destroyAllWindows()

        if self.captured_face is None:
            messagebox.showerror("Error", "No face captured. Please try again.")
        else:
            messagebox.showinfo("Success", "Face captured successfully!")

    def login_with_face(self):
        """Logs in the user by recognizing their face from the database."""
        self.capture_face()

        if self.captured_face is not None:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT username, face_encoding FROM users")

            users = cursor.fetchall()
            print("Retrieved users:", users)    #changes
            captured_encoding = face_recognition.face_encodings(self.captured_face)[0]
            for user in users:  
                stored_face_encoding = np.frombuffer(user[1], dtype=np.uint8)
                stored_face_image = cv2.imdecode(stored_face_encoding, cv2.IMREAD_COLOR)
                stored_encoding = face_recognition.face_encodings(stored_face_image)[0]
                
                # Compare using face_recognition's compare_faces
                results = face_recognition.compare_faces([stored_encoding], captured_encoding)
                if results[0]:
                    messagebox.showinfo("Success", f"Login successful! Welcome {user[0]}")
                    self.on_login_success()  # Log the user in
                    return        

            messagebox.showerror("Login Failed", "Face not recognized. Please try again.")
           
    
class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        
        # self.database()
        # Visible Application Frame
        self.AppFrame()

    # def database(self):
    #     # Sqlite3 Database Connection
    #     try:
    #         DB_PATH = os.path.join(
    #             os.path.dirname(__file__), "./database/Transactions.db"
    #         )

    #         if os.path.exists(DB_PATH):
    #             self.dbConnection = DatabaseHandler.DatabaseConnect(DB_PATH)
    #             print("Database connected already exists!")
    #         else:
    #             self.dbConnection = DatabaseHandler.DatabaseConnect(DB_PATH)
    #             print("Database created and connected!")
    #         # Create Transactions Table
    #         DatabaseHandler.createTransactionTable(self.dbConnection)
    #     except sqlite3.Error as e:
    #         print(f"Error connecting to the database: {e}")

    def AppFrame(self):
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # *############################################################################################
        # ? left-side navigation frame
        # *############################################################################################
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="VoiceMate",
            compound="left",
            font=customtkinter.CTkFont("Times new roman", size=18, weight="bold"),
        )
        self.navigation_frame_label.grid(
            row=0, column=0, padx=20, pady=20, sticky="new"
        )


        self.seperator = customtkinter.CTkLabel(
            self.navigation_frame,
            text="======================================",
            corner_radius=10,
            font=customtkinter.CTkFont("Times new roman", size=12, weight="bold"),
        )
        self.seperator.grid(row=2, column=0)

        self.home_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=5,
            height=40,
            border_spacing=10,
            text="Home",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.home_button_event,
        )
        self.home_button.grid(row=3, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=5,
            height=40,
            border_spacing=10,
            text="Summary / Rephrase",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.frame_2_button_event,
        )
        self.frame_2_button.grid(row=4, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=5,
            height=40,
            border_spacing=10,
            text="Notes/Reminder",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.frame_3_button_event,
        )
        self.frame_3_button.grid(row=5, column=0, sticky="new")

        self.frame_4_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=5,
            height=40,
            border_spacing=10,
            text="Help",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.frame_4_button_event,
        )
        self.frame_4_button.grid(row=6, column=0, sticky="new")



        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.navigation_frame,
            fg_color="teal",
            values=[ "Light", "Dark"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=20, sticky="s")
        

        # logout Button
        self.btnExitApplication = customtkinter.CTkButton(
            self.navigation_frame,
            text="Logout",          
            fg_color="teal",
            hover_color="#FF0000",
            command=self.exit_application,
        )
        self.btnExitApplication.grid(column=0, padx=20, pady=20, sticky="s")

        # *############################################################################################
        # ? create Navigation Frame 1 - Home
        # *############################################################################################
        self.home_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.home_frame.grid_columnconfigure(0, weight=1)

        # Home_Tab.py - (Add , Delete Transactions)
        Home_Tab(self, self.home_frame)

        # *############################################################################################
        # ? Navigation Frame 2 - SummaryTab
        # *############################################################################################
        self.second_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.second_frame.grid_columnconfigure(0, weight=1)

        # SummaryTab.py - 
        SummaryTab(self, self.second_frame)
        # *############################################################################################
        # ? Navigation Frame 3 - View
        # *############################################################################################
        self.third_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.third_frame.grid_columnconfigure(0, weight=1)

        # ViewTab.py - View Transactions
        ViewTab(self, self.third_frame)

        # *############################################################################################
        # ? Navigation Frame 4 - Help
        # *############################################################################################
        self.fourth_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.fourth_frame.grid_columnconfigure(0, weight=1)

        # helpTab.py - (Help, Licence, Developer)
        helpTab(self.fourth_frame)

        # *############################################################################################
        # ? Navigation Frama 5 -
        # *############################################################################################
        # self.fifth_frame = customtkinter.CTkFrame(
        #     self, corner_radius=0, fg_color="transparent"
        # )
        # self.fifth_frame.grid_columnconfigure(0, weight=1)

        # select default frame
        self.select_frame_by_name("home")

    # *############################################################################################
    # ? Frame Selecting Function
    # *############################################################################################
    def select_frame_by_name(self, name):
        # set button color for selected button
        # Add / Delete
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent"
        )
        # SummaryTab
        self.frame_2_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_2" else "transparent"
        )
        # View
        self.frame_3_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_3" else "transparent"
        )
        # Help
        self.frame_4_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_4" else "transparent"
        )

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def exit_application(self):
        print(">>>: Logout Application!")
        exit_application(self)

    def validate_Number(self, input_string):
        try:
            float(input_string)
            return True
        except ValueError:
            return False

    def validate_String(self, input_string):
        # if all(char.isalnum() or char.isspace() for char in input_string):
        if all(
            char.isalnum() or char.isspace() or not char.isprintable()
            for char in input_string
        ):
            print(input_string)
            return True
        else:
            return False


class LoginApp(customtkinter.CTk):
    def __init__(self, db_connection):  #changes
        super().__init__()
        self.db_connection = db_connection      #changes
        self.show_login_page()
        self.title("Login Page")


    def show_login_page(self):
        login_page = LoginPage(self, db_connection, self.on_login_success)     #changes
        login_page.pack(expand=True, fill="both")
        
    
    def on_login_success(self):
        self.destroy()  # Destroy the login window
        self.initialize_main_application()               

    def initialize_main_application(self):
        app = App()  # Initialize the main application
        app._set_appearance_mode("System")  # Set appearance mode
        customtkinter.set_default_color_theme("green")  # Set default color theme
        app.title("VoiceMate")  # Set window title
        app.geometry("880x600")  # Set window size
        app.minsize(940, 460)  # Set minimum window size
        app.state("zoomed")  # Maximize window
        app.mainloop()  # Start main event loop
        start_check_thread()
        check_queue()

    def signup(self):
        """Redirect to the signup page to allow new users to register with face capture."""
        signup_main()
    

if __name__ == "__main__":
    db_connection = sqlite3.connect("./pages/memory.db")  #changes
    app = LoginApp(db_connection)     #changes
    app.mainloop() 
    db_connection.close()   #changes 