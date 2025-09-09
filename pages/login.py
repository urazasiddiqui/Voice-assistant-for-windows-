import sqlite3
import customtkinter
import face_recognition
from tkinter import messagebox
import cv2  # For face detection and image capture
import numpy as np  # For image processing

class LoginPage(customtkinter.CTkFrame):
    def __init__(self, parent, db_connection, on_login_success):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.parent = parent
        self.db_connection = db_connection  # Save the db_connection for later use
        self.on_login_success = on_login_success
        self.captured_face = None  # Placeholder for storing the captured face

        # Create a frame for login widgets
        login_frame = customtkinter.CTkFrame(self)
        login_frame.pack(expand=True, padx=(580, 10), pady=200)  # Adjust pady for vertical centering

        # Username Label and Entry (positioned on the right side)
        self.username_label = customtkinter.CTkLabel(login_frame, text="Username")
        self.username_label.grid(row=0, column=0, pady=10, padx=10, sticky="e")
        self.username_entry = customtkinter.CTkEntry(login_frame, show="")
        self.username_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # Password Label and Entry (positioned on the right side)
        self.password_label = customtkinter.CTkLabel(login_frame, text="Password")
        self.password_label.grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.password_entry = customtkinter.CTkEntry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        # Login Button (centered)
        self.login_button = customtkinter.CTkButton(
            login_frame, text="Login", corner_radius=5, command=self.login
        )
        self.login_button.grid(row=2, column=0, columnspan=2, pady=20)

        # Face Recognition Button
        self.face_recognition_button = customtkinter.CTkButton(
            login_frame, text="Login with Face", corner_radius=5, command=self.login_with_face, fg_color="teal"
        )
        self.face_recognition_button.grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            self.on_login_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

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

            cv2.imshow('Face Capture', frame)  # Display the frame

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
            print("Retrieved users:", users)
            captured_encoding = face_recognition.face_encodings(self.captured_face)[0]
            for user in users:  
                stored_face_encoding = np.frombuffer(user[1], dtype=np.uint8)
                stored_face_image = cv2.imdecode(stored_face_encoding, cv2.IMREAD_COLOR)
                stored_encoding = face_recognition.face_encodings(stored_face_image)[0]

                results = face_recognition.compare_faces([stored_encoding], captured_encoding)
                if results[0]:
                    messagebox.showinfo("Success", f"Login successful! Welcome {user[0]}")
                    self.on_login_success()  # Log the user in
                    return
            messagebox.showerror("Login Failed", "Face not recognized. Please try again.")

class LoginApp(customtkinter.CTk):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.login_page = None
        self.show_login_page()

    def show_login_page(self):
        self.login_page = LoginPage(self, self.db_connection, self.on_login_success)
        self.login_page.pack(expand=True, fill="both")

    def on_login_success(self):
        if self.login_page:
            self.login_page.pack_forget()  # Hide the login page
            self.login_page = None
        # Proceed with the rest of your application logic after successful login

def login():
    db_connection = sqlite3.connect("./pages/memory.db")  # Load the database
    login_app = LoginApp(db_connection)  # Instantiate LoginApp
    login_app._set_appearance_mode("System")  # Set appearance mode
    customtkinter.set_default_color_theme("blue")  # Set default color theme
    login_app.title("VoiceMate2")  # Set window title
    login_app.geometry("880x600")  # Set window size
    login_app.minsize(880, 460)  # Set minimum window size
    login_app.state("zoomed")  # Maximize window
    login_app.mainloop()  # Start main event loop
    db_connection.close()

if __name__ == "__main__":
    login()  # Call the login function to start the application
