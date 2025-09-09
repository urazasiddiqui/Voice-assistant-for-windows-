import customtkinter
from CTkMessagebox import CTkMessagebox
import sqlite3


def show_info():
    # Default messagebox for showing some information
    CTkMessagebox(title="Info", message="This is a CTkMessagebox!")


def show_thanks(title, msg):
    CTkMessagebox(
        title=title,
        message=msg,
        icon="check",
        option_1="Thanks",
    )


def show_error(title, msg):
    # Show some error message
    CTkMessagebox(
        title=title,
        message=msg,
        icon="cancel",
    )


def show_delete_warning(msg):
    # Show some retry/cancel warnings
    msg = CTkMessagebox(
        title="Warning: Deleting Record!",
        message=msg,
        icon="warning",
        option_1="Cancel",
        option_2="No",
        option_3="Yes",
    )

    if msg.get() == "Yes":
        return True
    elif msg.get() == "No":
        return False
    else:
        return None


def exit_application(app):
    # Get yes/no answers
    msg = CTkMessagebox(
        title="Logout",
        message="Are you sure you want to logout?",
        icon="question",
        option_1="Cancel",
        option_2="No",
        option_3="Yes",
    )
    response = msg.get()

    if response == "Yes":
        # Close SQLite3 Database Connection
        if hasattr(app, "dbConnection"):  # Ensure dbConnection exists
            app.dbConnection.close()
        # Close GUI Application
        app.destroy()
    else:
        print("Click 'Yes' to logout!")


# Main application class
class MyApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Initialize the database connection
        self.dbConnection = sqlite3.connect("my_database.db")
        self.setup_ui()

    def setup_ui(self):
        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.columnconfigure(0, weight=1)
        self.minsize(200, 250)

        customtkinter.CTkLabel(self, text="CTk Messagebox Examples").grid(padx=20)
        customtkinter.CTkButton(self, text="Show Info", command=show_info).grid(
            padx=20, pady=10, sticky="news"
        )
        customtkinter.CTkButton(
            self, text="Logout", command=lambda: exit_application(self)
        ).grid(padx=20, pady=10, sticky="news")


# Run the application
if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
