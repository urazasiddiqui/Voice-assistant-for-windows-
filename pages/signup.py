import customtkinter
import sqlite3
import re
from tkinter import messagebox
import cv2  
import numpy as np  
from pages.login import LoginPage
import io  

class SignupPage(customtkinter.CTkFrame):
    def __init__(self, parent, db_connection, on_login_success):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.parent = parent
        self.db_connection = db_connection
        self.on_login_success = on_login_success
        self.captured_face = None  

        
        title_text_label = customtkinter.CTkLabel(self, text="VoiceMate", font=("Arial", 20), text_color="black")
        title_text_label.grid(row=0, column=0, sticky="nw", padx=(60, 0), pady=(20, 0))

        
        self.logup_frame = customtkinter.CTkFrame(self, fg_color="teal")
        self.logup_frame.grid(row=0, column=0, padx=(150, 0), pady=150, sticky="nsew")
        
        
        self.new_username_label = customtkinter.CTkLabel(self.logup_frame, text="Welcome to Sign Up", font=('Arial Black', 24), text_color="white")
        self.new_username_label.grid(row=1, column=0, padx=25, pady=(80, 20), sticky="e")

        
        self.new_password_label = customtkinter.CTkLabel(self.logup_frame, text="Yours VoiceMate", font=('Arial', 24), text_color="white")
        self.new_password_label.grid(row=2, column=0, padx=15, pady=10, sticky="e")
        
        

        # Signup details frame
        self.signup_frame = customtkinter.CTkFrame(self)
        self.signup_frame.grid(row=0, column=1, padx=(0, 150), pady=150, sticky="nsew")

        # Title label
        self.title_label = customtkinter.CTkLabel(self.signup_frame, text="Sign Up", font=('Arial Black', 20), text_color="black")
        self.title_label.grid(row=0, column=0, padx=(10, 100), pady=(20, 3), sticky="e")

        # Label and Entry for First Name
        self.first_name_label = customtkinter.CTkLabel(self.signup_frame, text="First Name:", text_color="black")
        self.first_name_label.grid(row=1, column=0, pady=3, padx=10, sticky="w")
        self.first_name_entry = customtkinter.CTkEntry(self.signup_frame)
        self.first_name_entry.grid(row=1, column=1, pady=3, padx=(0, 10))
        self.set_placeholder(self.first_name_entry, "Enter First Name")
        
        # Label and Entry for Last Name
        self.last_name_label = customtkinter.CTkLabel(self.signup_frame, text="Last Name:", text_color="black")
        self.last_name_label.grid(row=2, column=0, pady=3, padx=10, sticky="w")
        self.last_name_entry = customtkinter.CTkEntry(self.signup_frame)
        self.last_name_entry.grid(row=2, column=1, pady=3, padx=(0, 10))
        self.set_placeholder(self.last_name_entry, "Enter Last Name")

        # Label and Entry for Username
        self.username_label = customtkinter.CTkLabel(self.signup_frame, text="Username:", text_color="black")
        self.username_label.grid(row=3, column=0, pady=3, padx=10, sticky="w")
        self.username_entry = customtkinter.CTkEntry(self.signup_frame)
        self.username_entry.grid(row=3, column=1, pady=3, padx=(0, 10))
        self.set_placeholder(self.username_entry, "Enter Username")

        # Label and Entry for Email
        self.email_label = customtkinter.CTkLabel(self.signup_frame, text="Email:", text_color="black")
        self.email_label.grid(row=4, column=0, pady=3, padx=10, sticky="w")
        self.email_entry = customtkinter.CTkEntry(self.signup_frame)
        self.email_entry.grid(row=4, column=1, pady=3, padx=(0, 10))
        self.set_placeholder(self.email_entry, "Enter Email")

        # Label and Entry for Password
        self.password_label = customtkinter.CTkLabel(self.signup_frame, text="Password:", text_color="black")
        self.password_label.grid(row=5, column=0, pady=3, padx=10, sticky="w")
        self.password_entry = customtkinter.CTkEntry(self.signup_frame, show="*")
        self.password_entry.grid(row=5, column=1, pady=3, padx=(0, 10))
        self.set_placeholder(self.password_entry, "Enter Password", show="*")

        # Label and Entry for Confirm Password
        self.confirm_password_label = customtkinter.CTkLabel(self.signup_frame, text="Confirm Password:", text_color="black")
        self.confirm_password_label.grid(row=6, column=0, pady=3, padx=10, sticky="w")
        self.confirm_password_entry = customtkinter.CTkEntry(self.signup_frame, show="*")
        self.confirm_password_entry.grid(row=6, column=1, pady=3, padx=(0, 10))
        self.set_placeholder(self.confirm_password_entry, "Confirm Password", show="*")

        # Capture Face Button
        self.capture_face_button = customtkinter.CTkButton(self.signup_frame, text="Capture Face", corner_radius=5, command=self.capture_face, fg_color="teal")
        self.capture_face_button.grid(row=7, column=0, columnspan=2, pady=(10, 10))

        # Signup Button
        self.signup_button = customtkinter.CTkButton(self.signup_frame, text="Signup", corner_radius=5, command=self.signup, fg_color="teal")
        self.signup_button.grid(row=8, column=0, columnspan=2, pady=(10, 20))

    def set_placeholder(self, entry, placeholder_text, show=None):
        
        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, "end")
                if show:
                    entry.configure(show=show)
                entry.configure(fg_color="white")
        
        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder_text)
                if show:
                    entry.configure(show="")
                entry.configure(fg_color="white")

        entry.insert(0, placeholder_text)
        entry.configure(fg_color="white")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def capture_face(self):

        cap = cv2.VideoCapture(0)  

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        while True:
            ret, frame = cap.read()  
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw rectangle 
                face = frame[y:y + h, x:x + w]  

            cv2.imshow('Press q to Face Capture', frame)  

            if cv2.waitKey(1) & 0xFF == ord('q'):
                if faces is not None and len(faces) > 0:
                    self.captured_face = cv2.resize(face, (150, 150))  
                break

        cap.release()
        cv2.destroyAllWindows()

        if self.captured_face is not None:
            messagebox.showinfo("Success", "Face captured successfully!")
        else:
            messagebox.showerror("Error", "No face captured. Please try again.")

    def signup(self):
        """Inserts the user details along with the captured face into the database."""
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        
        if not first_name or not last_name or not username or not email or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required!")
            return

        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            messagebox.showerror("Error", "Invalid email format!")
            return


        
        if self.captured_face is None:
            messagebox.showerror("Error", "No face captured. Please capture your face.")
            return

        
        face_encoding = cv2.imencode('.JPEG', self.captured_face)[1].tobytes()

    
        try:
            with self.db_connection:
            
                cursor = self.db_connection.cursor()
                cursor.execute("""
                    INSERT INTO users (first_name, last_name, username, email, password, face_encoding)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (first_name, last_name, username, email, password, face_encoding))

            self.db_connection.commit()

            messagebox.showinfo("Success", "Signup successful!")
            self.winfo_toplevel().destroy()
            

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username or email already exists!")
            
def signup_main():
    db_connection = sqlite3.connect("./pages/memory.db")  
    db_connection.execute(
        """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                face_encoding BLOB
            )
        """)

    app = customtkinter.CTk()
    
    def show_signup_page():
        signup_page.pack(fill="both", expand=True)
        login_page.pack_forget()

    # Function to show the login page
    def show_login_page():
        login_page.pack(fill="both", expand=True)
        signup_page.pack_forget()
        
    signup_page = SignupPage(app, db_connection, show_login_page)
    login_page = LoginPage(app, db_connection, show_signup_page)
    show_signup_page()
    # signup_page.pack(expand=True, fill="both")

    app._set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")
    app.title("Signup Page")
    app.geometry("880x600")
    app.mainloop()
    db_connection.close()

if __name__ == "__main__":
    signup_main()
