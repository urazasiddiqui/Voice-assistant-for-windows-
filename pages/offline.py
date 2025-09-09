import customtkinter
import speech_recognition as sr
from googletrans import Translator
import pyttsx3
import vosk
from vosk import Model, KaldiRecognizer
import os
import glob
import subprocess
import datetime
import ssl
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
from langdetect import detect
from dotenv import load_dotenv
from tkinter import messagebox, END
import time
from pages.application import open_application
import json
import sounddevice as sd
import queue
import tkinter as tk
from tkinter import messagebox, filedialog, END
from dotenv import load_dotenv
from pathlib import Path
import ctypes
import glob
import subprocess
from pages.database import save_query_to_db, get_command_for_keyword
import random
import pyautogui
import customtkinter
import speech_recognition as sr
import pyttsx3
import vosk
from pages.eye import start_eye_control_thread
from vosk import Model, KaldiRecognizer
from pages.eye import eye_controlled_mouse
import os
import subprocess
import datetime
import sys
import tkinter as tk
from tkinter import messagebox, filedialog, END
import time
import json
import sounddevice as sd
import queue
from pages.database import insert_task
from pages.file_c_d_e import del_file
from pages.notes import add_note, delete_note, view_notes

def clear_screen(text_box):
    text_box.delete('1.0', tk.END)




engine = pyttsx3.init()     

engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

recognizer = sr.Recognizer()


def speak(text_to_speak):
    engine.say(text_to_speak)
    engine.runAndWait()

engine = pyttsx3.init()

class StdoutRedirector:
    def __init__(self, text_widget, query_response_text=None):
        self.text_widget = text_widget
        self.query_response_text = query_response_text

    def write(self, text):
        sys.__stdout__.write(text)
        self.text_widget.insert(END, text)
        self.text_widget.update_idletasks()  
        self.text_widget.yview(END)

        if self.query_response_text and hasattr(self.query_response_text, 'insert'):
            self.query_response_text.insert(END, text)
            self.query_response_text.update_idletasks()  
            self.query_response_text.yview(END)

    def flush(self):
        pass

# Initialize Vosk model
vosk_model_path = "C:\\Users\\ThinkPad\\Desktop\\vosk-model-small-en-in-0.4\\vosk-model-small-en-in-0.4"  # Specify the path to your Vosk model
model = vosk.Model(vosk_model_path)
q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))
def speech_to_text(text_box):
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        recognizer = vosk.KaldiRecognizer(model, 16000)
        print("\nListening...")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                query = result['text'].strip()
                if query:
                    print(f"User said: {query}")
                    text_box.insert(tk.END, "You: " + query + "\n")
                    text_box.yview(tk.END)
                    return query
                else:
                    print("Could not understand audio.")
                    speak("Sorry, I didn't get that. Can you please repeat?")
                    return None

def process_audio(text_box):
    query = speech_to_text(text_box)
    if query is not None:
        # # Update text box with recognized query
        # text_box.insert(tk.END, "You: " + query + "\n")
        # text_box.yview(tk.END)
        
       
        # if 'wikipedia' in query:
        #     speak("Searching Wikipedia...")
        #     query = query.replace("wikipedia", "")
        #     search_wikipedia(query)

        # elif 'search file' in query:
        #     Search_file()

        if 'open notepad' in query or 'notepad' in query:
            try:
                save_query_to_db(query, 'notepad')
                os.system('start notepad.exe')
                speak("Notepad is opening")
                print("Notepad is opening")
                time.sleep(2)  
                
                while True:
                    speak("Please provide the name of the file.")
                    print("Please provide the name of the file.")
                    file_name = speech_to_text(text_box)

            
                    if file_name != "none" and file_name != "":
                       file_path = f"{file_name}.txt"
                       break
                    else:
                      speak("I didn't hear a valid name. Using 'default_note.txt' as the file name.")
                      print("Using 'default_note.txt' as the file name.")
                      file_name = "default_note"
                      file_path = f"{file_name}.txt"
                      break
                
                # Ask what to write
                while True:
                    speak("What would you like to write in Notepad?")
                    print("What would you like to write in Notepad?")
                    text_to_write = speech_to_text(text_box)
                    
                    if 'close notepad' in text_to_write:
                        speak("Closing Notepad.")
                        print("Closing Notepad.")
                        os.system('taskkill /f /im notepad.exe')  # Force close Notepad
                        break
        
                    if text_to_write != "None":
                        with open(file_path, 'a') as file:
            
                            file.write(text_to_write + "\n")
            
            
                    subprocess.Popen(['notepad.exe', file_path])

        # Record task completion
                results = "Notepad is opening and writing the text..."
                insert_task(query, results)

            except Exception as e:
                print(e)
                speak("Sorry, I couldn't open Notepad.")

        elif 'calculator' in query:
            try:
                save_query_to_db(query, 'calulator')
                os.system('calc.exe')
                speak("Calculator is opening")
                results = "Calculatoris opening....."
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't open Calculator.")
                
        elif "close calculator" in query:
            save_query_to_db(query, 'close calulator')
            os.system("taskkill /f /im calc.exe")
            
        elif 'paint' in query:
            try:
                save_query_to_db(query, 'open paint')
                os.system('mspaint.exe')
                speak("Paint is opening")
                results = "Paintis opening....."
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't open Paint.")
        
        elif 'word' in query or 'ms word' in query:
            try:
        # Open word
                save_query_to_db(query, 'word')
                os.system('start WINWORD.EXE')
                speak("word is opening")
                print("word is opening")
                time.sleep(2)  
                
                while True:
                    speak("Please provide the name of the file.")
                    print("Please provide the name of the file.")
                    file_name = speech_to_text(text_box)

            
                    if file_name != "none" and file_name != "":
                       file_path = f"{file_name}.docx"
                       break
                    else:
                      speak("I didn't hear a valid name. Using 'default_note.txt' as the file name.")
                      print("Using 'default_doc.docx' as the file name.")
                      file_name = "default_doc"
                      file_path = f"{file_name}.docx"
                      break
                
                # Ask what to write
                while True:
                    speak("What would you like to write in word?")
                    print("What would you like to write in word?")
                    text_to_write = speech_to_text(text_box)
                    
                    if 'close word' in text_to_write:
                        speak("Closing Word.")
                        print("Closing Word.")
                        os.system('taskkill /f /im WINWORD.EXE')  # Force close word
                        break
        
                    if text_to_write != "None":
                        with open(file_path, 'a') as file:
            
                            file.write(text_to_write + "\n")
            
            
                    subprocess.Popen(['WINWORD.EXE', file_path])

        # Record task completion
                results = "word is opening and writing the text..."
                insert_task(query, results)

            except Exception as e:
                print(e)
                speak("Sorry, I couldn't open Word.")

        elif 'snipping tool' in query:
            try:
                save_query_to_db(query, 'snipping tool')
                os.system('SnippingTool.exe')
                speak("Snipping tool is opening")
                results = "Snipping tool is opening....."
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't open Snipping tool.")
        elif 'take screenshot' in query:
            try:
                save_query_to_db(query, 'screenshot')
        # Generate a file name based on the current time
                screenshot_name = f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
        
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", screenshot_name)
        
                screenshot = pyautogui.screenshot()
                screenshot.save(desktop_path)
        
                speak("Screenshot taken and saved on the desktop.")
                results = f"Screenshot saved as {screenshot_name} on the desktop."
                print(results)  # Print or handle the result as needed

            except Exception as e:
                print(e)
                speak("Sorry, I couldn't take a screenshot.")
        
        elif 'close notepad' in query:
            os.system("TASKKILL /F /IM notepad.exe")
            results= "nodepad is closed....."
            speak("nodepad is closing")
          
        elif 'activate eyes control' in query:
            save_query_to_db(query, 'eyes')
            start_eye_control_thread()
    
            
        elif 'shutdown laptop' in query:
            try:
                speak("Shutting down the laptop. Goodbye!")
                os.system('shutdown /s /t 1')  # Initiates a shutdown with a 1-second delay
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't shut down the laptop.")

        elif 'sleep laptop' in query:
            try:
                speak("Putting the laptop to sleep.")
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't put the laptop to sleep.")
            
        elif 'restart laptop' in query:
            try:
                speak("Restarting the laptop. See you in a moment!")
                os.system('shutdown /r /t 1')  # Initiates a restart with a 1-second delay
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't restart the laptop.")
            
        elif 'open application' in query or 'open another application' in query:
            open_application()

        elif 'clear screen' in query or 'voicemate stop' in query or 'stop  screen' in query:
           text_box.delete('1.0', END)
            
            
        elif 'search folder' in query or 'open folder' in query:
            folder_open()

        elif 'add notes' in query or 'add note' in query:
            add_note()

        elif 'view notes' in query or 'view note' in query:
            view_notes()

        elif 'delete notes' in query or 'delete note' in query:
            delete_note()

        elif 'is the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
            results= f"The time is {strTime}"                   
            

        elif "create file" in query or "create a file" in query:
            create_file()
            
        elif "delete file" in query or "delete a file" in query:
            del_file()

        elif "open vs code" in query:
            codePath = "C:\\Users\\ThinkPad\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code.exe"
            os.startfile(codePath)
            results= "vs code is opening....."
            speak("vs code is opening.....")
           
                
        elif "change wallpaper" in query or "change background" in query:
            save_query_to_db(query, 'wallpaper')
            user_pictures_folder = Path.home() / 'Pictures'
            
            if user_pictures_folder.exists() and any(user_pictures_folder.iterdir()):
                wallpapers = os.listdir(user_pictures_folder)
                
                # Filter for only image files (optional step)
                wallpapers = [f for f in wallpapers if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
                
                if wallpapers:
                    selected_wallpaper = random.choice(wallpapers)
                    wallpaper_path = os.path.join(user_pictures_folder, selected_wallpaper)
                    
                    # Change the wallpaper
                    SPI_SETDESKWALLPAPER = 20
                    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpaper_path, 3)
                    
                    results = "Wallpaper/background changed."
                    speak("Wallpaper background changed.")
                    insert_task(query, results)
                else:
                    speak("No wallpapers found in your Pictures folder.")  
            else:
                speak("Pictures folder not found or it's empty.")
            
                
        elif 'change brightness level' in query:
            get_number()
            results = "brightness level changed"
            
        

        elif 'change volume level' in query:
            get_spoken_number()
            results="volume level changed"
            


        # elif "send email" in query:
        #     try:
        #         speak("What is the subject of the email?")
        #         subject = speech_to_text()
        
        #         speak("What should be the content of the email?")
        #         body =speech_to_text()

        #         send_email(subject, body)
        #         speak("Email opened for you!")
        #     except Exception as e:
        #         print(e)
        #         speak("Sorry, I am not able to send the email.")
                
        # elif 'send message on whatsapp' in query:
        #     speak("Whom do you want to send the message to?")
        #     contact = speech_to_text().lower()  
        #     speak("What message do you want to send?")
        #     message = speech_to_text()
        #     sendWhatsappMessage(contact, message)

        
        # text_box.after(3000, clear_screen, text_box)

def find_files(directory, file_name):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file_name.lower() in file.lower():
                file_list.append(os.path.join(root, file))
    return file_list

def open_file(file_path):
    try:
        os.system(f'"{file_path}"')
        print(f"Opening file: {file_path}")
        
    except Exception as e:
        print(f"Error opening file: {e}")

def open_application(application):
    try:
        if application == "Notepad":
            subprocess.Popen(["notepad.exe"])
        elif application == "Calculator":
            subprocess.Popen(["calc.exe"])
        elif application == "Paint":
            subprocess.Popen(["mspaint.exe"])
        elif application =="Wordpad":
            subprocess.Popen(["write.exe"])
        elif application =="Snipping tool":
            subprocess.Popen(["SnippingTool.exe"])

    except Exception as e:
        print(f"Error opening {application}: {e}")

def open_applications_menu():
    popup = tk.Toplevel()
    popup.title("Open Application")

    label = tk.Label(popup, text="Choose an application to open:")
    label.grid(row=0, column=0, padx=10, pady=10)

    options = ["Notepad", "Calculator", "Paint","Snipping tool","Wordpad"]  # Add more options as needed

    selected_option = tk.StringVar()
    selected_option.set(options[0])  # Set default selected option

    option_menu = tk.OptionMenu(popup, selected_option, *options)
    option_menu.grid(row=0, column=1, padx=10, pady=10)

    open_button = tk.Button(popup, text="Open Application", command=lambda: open_application(selected_option.get()))
    open_button.grid(row=1, column=0, columnspan=2, pady=10)


# def send_email(receiver, subject, body):
#     try:
#         webbrowser.open(f"mailto:{receiver}?subject={subject}&body={body}")
#         speak("Email opened for you!")
#     except Exception as e:
#         print(e)
#         speak("Sorry, I am not able to send the email.")

# def send_email_popup():
#     popup = tk.Toplevel()
#     popup.title("Send Email")

#     receiver_label = tk.Label(popup, text="Receiver Email:")
#     receiver_label.grid(row=0, column=0, padx=10, pady=10)

#     receiver_entry = tk.Entry(popup)
#     receiver_entry.grid(row=0, column=1, padx=10, pady=10)

#     subject_label = tk.Label(popup, text="Subject:")
#     subject_label.grid(row=1, column=0, padx=10, pady=10)

#     subject_entry = tk.Entry(popup)
#     subject_entry.grid(row=1, column=1, padx=10, pady=10)

#     body_label = tk.Label(popup, text="Body:")
#     body_label.grid(row=2, column=0, padx=10, pady=10)

#     body_entry = tk.Entry(popup)
#     body_entry.grid(row=2, column=1, padx=10, pady=10)

#     send_button = tk.Button(popup, text="Send Email", command=lambda: send_email(receiver_entry.get(), subject_entry.get(), body_entry.get()))
#     send_button.grid(row=3, column=0, columnspan=2, pady=10)

        
def process_text_input(text_box):
    # Get the user input from the text box
    query = text_box.get("1.0", tk.END).strip()
    
    if query:
        print("\nReceived query:", query)
               
        # if 'wikipedia' in query:
        #     speak("Searching Wikipedia...")
        #     query = query.replace("wikipedia", "")
        #     search_wikipedia(query)

        if 'search file' in query or 'find file' in query:
            try:
                print("Sure, please enter the name of the file you are looking for:")
                file_name = input("File name: ")
                print(f"Searching for files with the name '{file_name}'...")

                search_directory = 'This PC'
                files = find_files(search_directory, file_name)

                if files:
                    print(f"Voice Mate found {len(files)} files:")
                    for i, file_path in enumerate(files, 1):
                        print(f"{i}. {file_path}")

                    response = input("Do you want to open any of these files? (yes/no): ").lower()

                    if response == "yes":
                        print("Sure, please enter the number of the file you want to open:")
                        try:
                            file_number = int(input("File number: "))
                            if 1 <= file_number <= len(files):
                                selected_file = files[file_number - 1]
                                open_file(selected_file)
                            else:
                                print("Invalid file number.")
                        except ValueError:
                            print("Invalid input for file number.")
                    else:
                        print("Okay, let me know if you need anything else.")

                else:
                    print(f"No files found with the name '{file_name}'.")

            except Exception as e:
                print(f"Error: {e}")


        elif 'open notepad' in query:
            try:
                os.system('start notepad.exe')
                speak("Notepad is opening")
                print("Notepad is opening")
                results = "nodepad is opening....."
               
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't open Notepad.")



        elif 'close notepad' in query:
            os.system("TASKKILL /F /IM notepad.exe")
            results= "nodepad is closed....."
            speak("nodepad is closing")
            


        # elif 'open youtube' in query:
        #     webbrowser.open("youtube.com")
        #     results= "youtube is opening....."
        #     speak("youtube is opening")
          
                
        # elif 'open google' in query:
        #     webbrowser.open("chrome.exe")
        #     results= "Google is opening....."
        #     speak("Google is opening")
        #     print("Google is opening")
           
            
        elif 'shutdown laptop' in query:
            try:
                speak("Shutting down the laptop. Goodbye!")
                os.system('shutdown /s /t 1')  # Initiates a shutdown with a 1-second delay
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't shut down the laptop.")

        elif 'sleep laptop' in query:
            try:
                speak("Putting the laptop to sleep.")
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't put the laptop to sleep.")
            
        elif 'restart laptop' in query:
            try:
                speak("Restarting the laptop. See you in a moment!")
                os.system('shutdown /r /t 1')  # Initiates a restart with a 1-second delay
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't restart the laptop.")

        # elif 'on youtube' in query:
        #     try:
        #         query = query.replace("on youtube", "")
        #         search_url = f"https://www.youtube.com/results?search_query={query}"
        #         webbrowser.open(search_url)
        #         results = "Searching YouTube....."
        #         speak("Searching YouTube")
                
        #     except Exception as e:
        #         print(e)
        #         speak("Sorry, I couldn't search on YouTube.")
                
        # elif 'on google' in query:
        #     try:
        #         query = query.replace("on google", "")
        #         search_url = f"https://www.google.com/search?q={query}"
        #         webbrowser.open(search_url)
        #         results = "Searching on Google....."
        #         speak("Searching on Google")
              
        #     except Exception as e:
        #         print(e)
        #         speak("Sorry, I couldn't search on YouTube.")
            
        # elif 'open application' in query or 'open another application' in query:
        #     open_application()

        # elif 'clear screen' in query or 'voicemate stop' in query or 'stop  screen' in query:
        #    text_box.delete('1.0', END)
            
            
        # elif 'close google' in query:
        #     os.system("TASKKILL /F /IM chrome.exe")
        #     results= "Google is closed...."
        #     speak("Google is closing")
           
                
        # elif 'open stack overflow' in query:
        #     webbrowser.open("stackoverflow.com")
        #     results= "stack overflow is opening....."
        #     speak("stack overflow is opening.....")
        
            
        elif 'search folder' in query or 'open folder' in query:
            folder_open()

        elif 'add notes' in query or 'add note' in query:
            add_note()

        elif 'view notes' in query or 'view note' in query:
            view_notes()

        elif 'delete notes' in query or 'delete note' in query:
            delete_note()

        elif 'is the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
            results= f"The time is {strTime}"                   
           

        elif "create file" in query or "create a file" in query:
            create_file()
            
        elif "delete file" in query or "delete a file" in query:
            del_file()

        elif "open vs code" in query:
            codePath = "C:\\Users\\ThinkPad\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code.exe"
            os.startfile(codePath)
            results= "vs code is opening....."
            speak("vs code is opening.....")
         
                
        elif "change wallpaper" in query or "change background" in query:
            wallpaper_folder = 'D:\\Course\\7th_sems\\Fyp\\fyp\\img'  
            wallpapers = os.listdir(wallpaper_folder)
            selected_wallpaper = random.choice(wallpapers)
            wallpaper_path = os.path.join(wallpaper_folder, selected_wallpaper)
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpaper_path, 3)
            results= "wallpaper/ background changed...."
            speak("wallpaper background changed....")
           
                
        elif 'change brightness level' in query:
            get_number()
            results = "brightness level changed"
         
        

        elif 'change volume level' in query:
            get_spoken_number()
            results="volume level changed"
           


        # elif "send email" in query:
        #     try:
        #         speak("What is the subject of the email?")
        #         subject = speech_to_text()
        
        #         speak("What should be the content of the email?")
        #         body =speech_to_text()

        #         send_email(subject, body)
        #         speak("Email opened for you!")
        #     except Exception as e:
        #         print(e)
        #         speak("Sorry, I am not able to send the email.")
                
        # elif 'send message on whatsapp' in query:
        #     speak("Whom do you want to send the message to?")
        #     contact = speech_to_text().lower()  
        #     speak("What message do you want to send?")
        #     message = speech_to_text()
        #     sendWhatsappMessage(contact, message)

        # else:
        #     ai_response = replyBrain(query)
            
        #     speak(ai_response)
        #     text_box.insert(tk.END, "VoiceMate: " + ai_response + "\n")
        #     text_box.yview(tk.END)
        
       
        
        # text_box.after(3000, clear_screen, text_box)


def create_folder(foldername, directory):
    """Create a new folder with the specified name in the specified directory."""
    if foldername and directory:
        folder_path = os.path.join(directory, foldername)
        try:
            os.mkdir(folder_path)
            messagebox.showinfo("Folder Created", f"Folder '{foldername}' created successfully in '{directory}'")
        except Exception as e:
            messagebox.showerror("Error", f"Error creating folder '{foldername}': {e}")
    else:
        messagebox.showerror("Error", "Folder name and directory must be provided.")

def create_folder_popup():
    popup = tk.Toplevel()
    popup.title("Create Folder")

    foldername_label = tk.Label(popup, text="Folder Name:")
    foldername_label.grid(row=0, column=0, padx=10, pady=10)

    foldername_entry = tk.Entry(popup)
    foldername_entry.grid(row=0, column=1, padx=10, pady=10)

    directory_label = tk.Label(popup, text="Directory:")
    directory_label.grid(row=1, column=0, padx=10, pady=10)

    directory_entry = tk.Entry(popup)
    directory_entry.grid(row=1, column=1, padx=10, pady=10)

    def select_directory():
        directory = filedialog.askdirectory()
        if directory:
            directory_entry.delete(0, tk.END)
            directory_entry.insert(0, directory)

    browse_button = tk.Button(popup, text="Browse...", command=select_directory)
    browse_button.grid(row=1, column=2, padx=10, pady=10)

    create_button = tk.Button(popup, text="Create Folder", command=lambda: create_folder(foldername_entry.get(), directory_entry.get()))
    create_button.grid(row=2, column=0, columnspan=3, pady=10)


def delete_file(filename, directory):
    """Delete an existing file using the specified filename in the specified directory."""
    if filename and directory:
        files = glob.glob(os.path.join(directory, f"{filename}*"))  # Search for files starting with the provided filename
        if files:
            try:
                for file in files:
                    os.remove(file)
                messagebox.showinfo("Files Deleted", f"Files starting with name '{filename}' deleted successfully from '{directory}'.")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting files starting with '{filename}': {e}")
        else:
            messagebox.showinfo("No Files Found", f"No files found starting with '{filename}' in '{directory}'.")
    else:
        messagebox.showerror("Error", "Filename and directory must be provided.")

def delete_file_popup():
    popup = tk.Toplevel()
    popup.title("Delete File")

    filename_label = tk.Label(popup, text="File Name:")
    filename_label.grid(row=0, column=0, padx=10, pady=10)

    filename_entry = tk.Entry(popup)
    filename_entry.grid(row=0, column=1, padx=10, pady=10)

    directory_label = tk.Label(popup, text="Directory:")
    directory_label.grid(row=1, column=0, padx=10, pady=10)

    directory_entry = tk.Entry(popup)
    directory_entry.grid(row=1, column=1, padx=10, pady=10)

    def select_directory():
        directory = filedialog.askdirectory()
        if directory:
            directory_entry.delete(0, tk.END)
            directory_entry.insert(0, directory)

    browse_button = tk.Button(popup, text="Browse...", command=select_directory)
    browse_button.grid(row=1, column=2, padx=10, pady=10)

    delete_button = tk.Button(popup, text="Delete File", command=lambda: delete_file(filename_entry.get(), directory_entry.get()))
    delete_button.grid(row=2, column=0, columnspan=3, pady=10)

#crete file
def create_file_popup():
    popup = tk.Toplevel()
    popup.title("Create File")

    # Labels and entry fields for file name, extension, and content
    filename_label = tk.Label(popup, text="File Name:")
    filename_label.grid(row=0, column=0, padx=10, pady=10)

    filename_entry = tk.Entry(popup)
    filename_entry.grid(row=0, column=1, padx=10, pady=10)

    extension_label = tk.Label(popup, text="Extension:")
    extension_label.grid(row=1, column=0, padx=10, pady=10)

    extension_entry = tk.Entry(popup)
    extension_entry.grid(row=1, column=1, padx=10, pady=10)

    content_label = tk.Label(popup, text="Content:")
    content_label.grid(row=2, column=0, padx=10, pady=10)

    content_entry = tk.Entry(popup)
    content_entry.grid(row=2, column=1, padx=10, pady=10)

    # Label and entry for directory path
    directory_label = tk.Label(popup, text="Directory:")
    directory_label.grid(row=3, column=0, padx=10, pady=10)

    directory_entry = tk.Entry(popup)
    directory_entry.grid(row=3, column=1, padx=10, pady=10)

    # Button to open file dialog for directory selection
    def select_directory():
        directory = filedialog.askdirectory()
        if directory:
            directory_entry.delete(0, tk.END)
            directory_entry.insert(0, directory)

    browse_button = tk.Button(popup, text="Browse...", command=select_directory)
    browse_button.grid(row=3, column=2, padx=10, pady=10)

    # Button to confirm file creation
    create_button = tk.Button(popup, text="Create File", command=lambda: create_file(filename_entry.get(), extension_entry.get(), content_entry.get(), directory_entry.get()))
    create_button.grid(row=4, column=0, columnspan=3, pady=10)

def create_file(filename, extension, content, directory):
    """Create a new file based on user input."""
    if filename and extension and content and directory:
        filename_with_extension = f"{filename.strip()}.{extension.strip()}"
        filepath = f"{directory.strip()}/{filename_with_extension}"
        try:
            with open(filepath, 'w') as f:
                f.write(content)
                messagebox.showinfo("File Created", f"File '{filename_with_extension}' created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create file: {e}")
    else:
        messagebox.showerror("Error", "All fields must be filled out.")
def open_file_popup():
    popup = tk.Toplevel()
    popup.title("Open File")

    # Label and entry for file path
    file_label = tk.Label(popup, text="File Path:")
    file_label.grid(row=0, column=0, padx=10, pady=10)

    file_entry = tk.Entry(popup)
    file_entry.grid(row=0, column=1, padx=10, pady=10)

    # Button to open file dialog for file selection
    def select_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            file_entry.delete(0, tk.END)
            file_entry.insert(0, file_path)

    browse_button = tk.Button(popup, text="Browse...", command=select_file)
    browse_button.grid(row=0, column=2, padx=10, pady=10)

    # Button to confirm file opening
    open_button = tk.Button(popup, text="Open File", command=lambda: open_selected_file(file_entry.get()))
    open_button.grid(row=1, column=0, columnspan=3, pady=10)

def open_selected_file(file_path):
    """Open the selected file."""
    if file_path:
        try:
            os.startfile(file_path)
            messagebox.showinfo("File Opened", f"File '{file_path}' opened successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")
    else:
        messagebox.showerror("Error", "Please select a file to open.")
def open_folder_popup():
    popup = tk.Toplevel()
    popup.title("Open Folder")

    # Label and entry for folder path
    folder_label = tk.Label(popup, text="Folder Path:")
    folder_label.grid(row=0, column=0, padx=10, pady=10)

    folder_entry = tk.Entry(popup)
    folder_entry.grid(row=0, column=1, padx=10, pady=10)

    # Button to open file dialog for folder selection
    def select_folder():
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_entry.delete(0, tk.END)
            folder_entry.insert(0, folder_path)

    browse_button = tk.Button(popup, text="Browse...", command=select_folder)
    browse_button.grid(row=0, column=2, padx=10, pady=10)

    # Button to confirm folder opening
    open_button = tk.Button(popup, text="Open Folder", command=lambda: open_selected_folder(folder_entry.get()))
    open_button.grid(row=1, column=0, columnspan=3, pady=10)

def open_selected_folder(folder_path):
    """Open the selected folder."""
    if folder_path:
        try:
            os.startfile(folder_path)
            messagebox.showinfo("Folder Opened", f"Folder '{folder_path}' opened successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {e}")
    else:
        messagebox.showerror("Error", "Please select a folder to open.")

class Offline_class:  
    def __init__(self, parentHomeFrame):
        self.parentHomeFrame = parentHomeFrame
        self.Offlinetab()

    def Offlinetab(self):
        tabview_1 = customtkinter.CTkTabview(self.parentHomeFrame, width=460)
        tabview_1.pack(pady=10, padx=10)
        tab1_add = tabview_1.add("VoiceMate")


        self.AddTransactionLabel = customtkinter.CTkLabel(
            tab1_add,
            text="Offline Mode",
            compound="left",
            font=customtkinter.CTkFont("Times new roman", size=18, weight="bold"),
        )
        self.AddTransactionLabel.grid(row=0, column=0, columnspan=5, padx=20, pady=20, sticky="ew")

        def sleep_lap():
            try:
                speak("Putting the laptop to sleep.")
                print("Putting the laptop to sleep.")
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't put the laptop to sleep.")
        def restart_lap():
            try:
                speak("Restarting the laptop. See you in a moment!")
                print("Restarting the laptop. See you in a moment!")
                os.system('shutdown /r /t 1')  # Initiates a restart with a 1-second delay
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't restart the laptop.")

        def shutdown_lap():
            try:
                speak("Shutting down the laptop. Goodbye!")
                print("Shutting down the laptop. Goodbye!")
                os.system('shutdown /s /t 1')  # Initiates a shutdown with a 1-second delay
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't shut down the laptop.")

        # Query Button 1
        self.queryButton1 = customtkinter.CTkButton(
            tab1_add,
            text="Open file",
            fg_color="teal",border_color="white",border_width=1,
            command=open_file_popup
        )
        self.queryButton1.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.queryButton2 = customtkinter.CTkButton(
            tab1_add,
            text="Open folder",
            fg_color="teal",border_color="white",border_width=1,
            command=open_folder_popup
        )
        self.queryButton2.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.queryButton3 = customtkinter.CTkButton(
            tab1_add,
            text="Open Application",
            fg_color="teal",border_color="white",border_width=1,
            command=open_applications_menu
        )
        self.queryButton3.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

        # Query Button 2
        self.queryButton4 = customtkinter.CTkButton(
            tab1_add,
            text="Create File",
            fg_color="teal",border_color="white",border_width=1,
            command=create_file_popup # Replace with the actual function to execute Query 2
        )
        self.queryButton4.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.queryButton5 = customtkinter.CTkButton(
            tab1_add,
            text="Delete File",
            fg_color="teal",border_color="white",border_width=1,
            command=delete_file_popup 
        )
        self.queryButton5.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.queryButton6 = customtkinter.CTkButton(
            tab1_add,
            text="Create folder",
            fg_color="teal",border_color="white",border_width=1,
            command=create_folder_popup
        )
        self.queryButton6.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
    
        self.queryButton7 = customtkinter.CTkButton(
            tab1_add,
            text="Shutdown System",
            fg_color="teal",border_color="white",border_width=1,
            command=shutdown_lap
        )
        self.queryButton7.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        self.queryButton8 = customtkinter.CTkButton(
            tab1_add,
            text="Restart System",
            fg_color="teal",border_color="white",border_width=1,
            command=restart_lap 
        )
        self.queryButton8.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.queryButton9 = customtkinter.CTkButton(
            tab1_add,
            text="Sleep System",
            fg_color="teal",border_color="white",border_width=1,
            command=sleep_lap 
        )
        self.queryButton9.grid(row=3, column=2, padx=5, pady=5, sticky="ew")
        # Query Entry Field 2
        # self.queryEntry2 = customtkinter.CTkEntry(tab1_add, placeholder_text="Enter Query 2", height=140, width=480)
        # self.queryEntry2.grid(row=4, column=0, columnspan=3, padx=5, pady=20, sticky="ew")

        # Define text_box
        self.text_box = tk.Text(tab1_add, height=10, width=80)  # Example definition, adjust as needed
        self.text_box.grid(row=4, column=0, columnspan=3, padx=5, pady=20, sticky="ew")
        sys.stdout = StdoutRedirector(self.text_box)

        self.submit_btn = customtkinter.CTkButton(
            tab1_add,
            text="Text Submit",
            fg_color="teal",
            border_color="white",
            border_width=1,
            command=lambda: process_text_input(self.text_box),
        )
        self.submit_btn.grid(row=6, column=0,  pady=5, sticky="ew")


        # mic Button
        self.Mic_button= customtkinter.CTkButton(
            tab1_add,
            text="Voice Input",
            fg_color="teal",
            border_color="white",
            border_width=1,
            command=lambda: process_audio(self.text_box),
        )
        self.Mic_button.grid(row=6, column=2, columnspan=2,  pady=5, sticky="ew")

        # Previous Transaction Labels (if needed)
        self.addpreviouslytextLabel = customtkinter.CTkLabel(tab1_add, text="")
        self.addpreviouslytextLabel.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

        self.addpreviouslyLabel = customtkinter.CTkLabel(tab1_add, text="")
        self.addpreviouslyLabel.grid(row=5, column=1, sticky="ew")

  
def offline_interface():
    app = tk.Tk()  # Assuming you have imported tkinter as tk
    app.title("VoiceMate")
    app = Offline_class(app)
    app.mainloop()


if __name__ == "__main__":
    offline_interface()
    
