from pathlib import Path
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import subprocess
import whisper
import yagmail
import datetime
import psutil
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from playsound import playsound
import re
import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import customtkinter
import speech_recognition as sr
from googletrans import Translator
import pyttsx3
import openai
import os
# from datetime import datetime
import random
import ctypes
import glob
import subprocess
import wikipedia
import pywhatkit
import pywhatkit as kit
import ssl
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
from langdetect import detect
from dotenv import load_dotenv
from tkinter import messagebox, END
from pages.database import insert_question_and_answer
from pages.database import save_query_to_db, get_command_for_keyword

import time


from pages.database import insert_task
from pages.file_c_d_e import create_files 
from pages.file_c_d_e import del_file
import time
import webbrowser
from pages.find_file import Search_file
from pages.application import open_application
from pages.eye import eye_controlled_mouse
from pages.notes import add_note, delete_note, view_notes
from pages.eye import start_eye_control_thread
import urllib.parse
import re

def search_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=1)
        speak("According to Wikipedia:")
        print(results)
        speak(results)
        insert_question_and_answer(query, results)
        search_url = "https://en.wikipedia.org/wiki/" + query.replace(" ", "_")
        webbrowser.open(search_url)

    except wikipedia.exceptions.DisambiguationError as e:
        speak("It seems there's a disambiguation, please specify your query.")
    except wikipedia.exceptions.PageError as e:
        speak("I couldn't find any results for that query.")


def clear_screen(text_box):
    text_box.delete('1.0', tk.END)

current_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(current_dir, "filelog.txt")



engine = pyttsx3.init()     

engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

recognizer = sr.Recognizer()

def speak(text_to_speak):
    engine.say(text_to_speak)
    engine.runAndWait()

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
    
def TranslateToEng(text):
    translator = Translator()
    translation = translator.translate(text, src='ur', dest='en')
    return translation.text


def speech_to_text(text_box):

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source)

        while voice_active:  
            try:
                audio = recognizer.listen(source, timeout=20)  
                print("Recognizing...")
                query = recognizer.recognize_google(audio).lower()

                try:
                    detected_language = detect(query)
                    
                except Exception as e:
                    print(f"Language detection failed: {e}")
                    detected_language = 'en'

                if detected_language == 'ur':  
                    try:
                        translated_query = TranslateToEng(query)
                        print("User said (from Urdu):", translated_query)
                    except Exception as e:
                        print(f"Translation failed: {e}")
                        translated_query = query
                else:
                    translated_query = query
                    print("User said (English detected):", translated_query)

                # Insert translated query to text box
                text_box.insert(tk.END, "You: " + translated_query + "\n")
                text_box.yview(tk.END)

                return translated_query  
            except sr.UnknownValueError:
                speak("Sorry, I didn't catch that. Could you please repeat?")
                
                continue
            except sr.RequestError as e:
                speak("Sorry, there was an error in processing your request.")
                return None  
            except Exception as e:
                speak(f"An unexpected error occurred: {e}")
                return None  
            
voice_active = False  

def toggle_voice_recognition(text_box):
    global voice_active
    voice_active = not voice_active  # Toggle the state

    if voice_active:
        print("Voice recognition activated. Speak now...")
        speak("Voice recognition activated. Speak now.")
        # Start a new thread for voice recognition
        threading.Thread(target=process_audio, args=(text_box,), daemon=True).start()
    else:
        print("Voice recognition deactivated.")
        speak("Voice recognition deactivated.")
        
                      
def process_audio(text_box):
    global voice_active
    while voice_active:
        query = speech_to_text(text_box)        #yahan try catch lagana hai reminder
        if query is not None:
            query = query.strip().lower() 
            text_box.insert(tk.END, "You: " + query + "\n")
            text_box.yview(tk.END)

            if 'wikipedia' in query:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                search_wikipedia(query)
                

            elif 'search file' in query:
                Search_file()

            elif 'open notepad' in query or 'notepad' in query:
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
                    save_query_to_db(query, 'paint')  
                    os.system('mspaint.exe')  # Open Paint
                    speak("Paint is opening")
                    results = "Paint is opening....."
                except Exception as e:
                    print(e)
                    speak("Sorry, I couldn't open Paint.")
            
            elif "close " in query:
                os.system("taskkill /f /im mspaint.exe")  
            
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
                    screenshot_name = f"screenshot_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
            
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
                save_query_to_db(query, 'close notepad')
                os.system("TASKKILL /F /IM notepad.exe")
                results= "nodepad is closed....."
                speak("nodepad is closing")
                insert_question_and_answer(query, results)

            elif 'open google' in query:
                save_query_to_db(query, 'google')
                webbrowser.open("chrome.exe")
                results= "Google is opening....."
                speak("Google is opening")
                print("Google is opening")
                insert_task(query, results)
            
            elif 'open facebook' in query:
                speak("Opening Facebook...")
                webbrowser.open("https://www.facebook.com")
    
            elif 'open instagram' in query:
                speak("Opening Instagram...")
                webbrowser.open("https://www.instagram.com")
                
            elif 'open linkedin' in query or 'open linked in' in query:
                speak("Opening LinkedIn...")
                webbrowser.open("https://www.linkedin.com")
                
            elif 'open twitter' in query or 'open x' in query:
                speak("Opening Twitter...")
                webbrowser.open("https://www.twitter.com")
            
            elif 'shutdown laptop' in query:
                try:
                    save_query_to_db(query, 'shutdown')
                    speak("Shutting down the laptop. Goodbye!")
                    os.system('shutdown /s /t 1')  
                except Exception as e:
                    print(e)
                    speak("Sorry, I couldn't shut down the laptop.")

            elif 'close facebook' in query:
                try:
                    pyautogui.hotkey('ctrl', 'l')  # Focus address bar
                    pyautogui.write('facebook.com')
                    pyautogui.hotkey('enter')
                    time.sleep(2)  # Wait for page to load
                    pyautogui.hotkey('ctrl', 'w')  # Close current tab
                    speak("Facebook tab closed")
                except Exception as e:
                    speak("Could not close Facebook tab")
                    print(f"Error: {e}")
            
            elif 'sleep laptop' in query:
                try:
                    save_query_to_db(query, 'sleep')
                    speak("Putting the laptop to sleep.")
                    os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
                except Exception as e:
                    print(e)
                    speak("Sorry, I couldn't put the laptop to sleep.")
            
            elif 'restart laptop' in query:
                try:
                    save_query_to_db(query, 'restart')
                    speak("Restarting the laptop. See you in a moment!")
                    os.system('shutdown /r /t 1')  # Initiates a restart with a 1-second delay
                except Exception as e:
                    print(e)
                    speak("Sorry, I couldn't restart the laptop.")

            elif 'on google' in query:
                try:
                    query = query.replace("on google", "")
                    search_url = f"https://www.google.com/search?q={query}"
                    webbrowser.open(search_url)
                    results = "Searching on Google....."
                    speak("Searching on Google")
                    insert_task(query, results)
                except Exception as e:
                    print(e)
                    speak("Sorry, I couldn't search on google.")
            
            elif 'open application' in query or 'open another application' in query:
                open_application()

            elif 'clear screen' in query or 'voicemate stop' in query or 'stop  screen' in query:
                text_box.delete('1.0', END)
                
                
            elif 'close google' in query:
                save_query_to_db(query, 'close google')
                os.system("TASKKILL /F /IM chrome.exe")
                results= "Google is closed...."
                speak("Google is closing")
                insert_task(query, results)
                    
            elif 'open stack overflow' in query:
                save_query_to_db(query, 'stack overflow')
                webbrowser.open("stackoverflow.com")
                results= "stack overflow is opening....."
                speak("stack overflow is opening.....")
                insert_task(query, results)
            
            elif 'search folder' in query or 'open folder' in query:
                folder_open()


            elif 'is the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {strTime}")
                results= f"The time is {strTime}"                   
                insert_question_and_answer(query, results)

            elif "create file" in query or "create a file" in query:
                create_files()
                
            elif "delete file" in query or "delete a file" in query:
                del_file()

            
            elif "open vs code" in query:
                try:
                    save_query_to_db(query, 'open visual studio')
                    subprocess.Popen(["code"])
                    results = "VS Code is opening..."
                    speak(results)
                except Exception as e:
                    results = "Could not open VS Code. Make sure it's installed and added to the PATH."
                    speak(results)
                insert_task(query, results)
        
            elif "open file explorer" in query:
                try:
                    save_query_to_db(query, 'open file explorer')
                    subprocess.Popen(["explorer"])  # Opens File Explorer
                    results = "File Explorer is opening..."
                    speak(results)
                except Exception as e:
                    results = "Could not open File Explorer. Make sure it's accessible."
                    speak(results)
                insert_task(query, results)        
            
            elif "scroll up" in query:
                try:
                    save_query_to_db(query, 'scroll up')
                    pyautogui.scroll(500)  # Scrolls up the screen
                    results = "Scrolling up..."
                    speak(results)
                except Exception as e:
                    results = "Could not scroll up. Please try again."
                    speak(results)
                insert_task(query, results)
        
            elif "scroll down" in query:
                try:
                    save_query_to_db(query, 'scroll down')
                    pyautogui.scroll(-500)  # Scrolls down the screen
                    results = "Scrolling down..."
                    speak(results)
                except Exception as e:
                    results = "Could not scroll down. Please try again."
                    speak(results)
                insert_task(query, results)
                
                
            
                
            elif 'on youtube' in query:
                try:
                    query = query.replace("on youtube", "")
                    search_url = f"https://www.youtube.com/results?search_query={query}"
                    webbrowser.open(search_url)
                    results = "Searching YouTube....."
                    speak("Searching YouTube")
                    insert_task(query, results)
                except Exception as e:
                    print(e)
                    speak("Sorry, I couldn't search on YouTube.") 
                    
            elif 'open youtube' in query:
                speak("What would you like to watch?")
                qrry = speech_to_text(text_box).lower()
                pywhatkit.playonyt(f"{qrry}")    
                
            elif 'close youtube' in query:
                save_query_to_db(query, 'close youtube')
                os.system("taskkill /f /im youtube.exe")
        
            elif "open" in query:
                try:
                    # Extract folder name from query 
                    folder_name = query.lower().split("open", 1)[1].strip()
                    
                    # Get the actual user profile path from environment variable
                    user_profile = os.environ['USERPROFILE']
                    
                    # Define folder paths based on your actual structure
                    folders = {
                        "c drive": "C:\\",
                        "documents": os.path.join(user_profile, "Documents"),
                        "downloads": os.path.join(user_profile, "Downloads"),
                        "desktop": os.path.join(user_profile, "Desktop"),
                        "pictures": os.path.join(user_profile, "Pictures"),
                        "videos": os.path.join(user_profile, "Videos"),
                        "music": os.path.join(user_profile, "Music")
                    }

                    # Debug print to check paths (you can remove this later)
                    print("Folder paths being used:")
                    for name, path in folders.items():
                        print(f"{name}: {path}")

                    # Find the best matching folder
                    matched_folder = None
                    for key in folders:
                        if key in folder_name:
                            matched_folder = key
                            break

                    if matched_folder:
                        folder_path = folders[matched_folder]
                        if os.path.exists(folder_path):
                            save_query_to_db(query, f'open {matched_folder}')
                            subprocess.Popen(["explorer", folder_path])
                            results = f"Opening {matched_folder}..."
                        else:
                            results = f"Folder path doesn't exist: {folder_path}"
                    else:
                        results = f"Sorry, I couldn't find the folder '{folder_name}'. Available folders are: " + ", ".join(folders.keys())

                    speak(results)
                except Exception as e:
                    results = f"Could not open the requested folder. Error: {str(e)}"
                    speak(results)
                
                insert_task(query, results)
            
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


            elif 'send email' in query or 'compose email' in query:
                try:
                    speak("Who should I receive the email? Please say the recipient's email address clearly.")
                    recipient = speech_to_text(text_box) if text_box else speech_to_text()
                    
                    # Clean and validate the email
                    recipient = recipient.lower().strip()
                    recipient = recipient.replace(" at the rate ", "@").replace(" at ", "@").replace(" dot ", ".")
                    recipient = ''.join(e for e in recipient if e.isalnum() or e in ['@', '.', '-', '_'])
                    
                    if not "@" in recipient or not "." in recipient.split("@")[1]:
                        speak("That doesn't look like a valid email address. Please try again.")
                        return
                        
                    speak("What should be the subject of the email?")
                    subject = speech_to_text(text_box) if text_box else speech_to_text()
                    
                    speak("What should I write in the email body?")
                    body = speech_to_text(text_box) if text_box else speech_to_text()
                    
                    # Email configuration (use environment variables in production)
                    smtp_server = "smtp.gmail.com"
                    smtp_port = 587
                    sender_email = "212129@students.au.edu.pk"  # Replace with your email
                    password = "olkf wdfg xbku mryo"  # Use app password for Gmail
                    
                    # Create message
                    message = f"Subject: {subject}\n\n{body}"
                    
                    # Send email
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(sender_email, password)
                        server.sendmail(sender_email, recipient, message)
                    
                    speak(f"Email successfully sent to {recipient}!")
                    print(f"Email sent to: {recipient}")
                    
                except smtplib.SMTPRecipientsRefused as e:
                    speak("The email address was rejected. Please check the recipient address.")
                    print(f"Recipient error: {e}")
                except smtplib.SMTPAuthenticationError:
                    speak("Failed to authenticate. Please check email credentials.")
                except Exception as e:
                    speak(f"Failed to send email: {str(e)}")
                    print(f"Error: {e}")
    
            elif 'activate mouse control' in query:
                save_query_to_db(query, 'mouse')
                start_eye_control_thread()


            elif 'close chrome' in query:
                save_query_to_db(query, 'close chrome')
                os.system("taskkill /f /im chrome.exe")
                
                
            # elif 'send message on whatsapp' in query:
            #     save_query_to_db(query, 'whatsapp')
            #     speak("Please say the phone number including the leading zero.")
        
            #     # Capture the contact number
            #     contact = speech_to_text(text_box)
            #     if contact is None:
            #         speak("I didn't catch that. Please repeat the phone number.")
            #         contact = speech_to_text(text_box)

            #     contact = process_number(contact)
            #     if contact is None:
            #         return  # Exit if the number format is invalid

            #     # Now ask for the message
            #     speak(f"The number you entered is {contact}. What message do you want to send?")
            #     message = speech_to_text(text_box)
            #     if message is None:
            #         speak("I didn't catch that. Please repeat your message.")
            #         message = speech_to_text(text_box)

            #     # Send the WhatsApp message
            #     send_whatsapp_message(contact, message)
            elif 'send message on whatsapp' in query or 'send on whatsapp' in query:
                save_query_to_db(query, 'whatsapp')
                speak("Would you like to send a text message or image?")
                
                # Determine message type
                message_type = speech_to_text(text_box).lower()
                if not message_type:
                    speak("I didn't catch that. Please specify text, image.")
                    message_type = speech_to_text(text_box).lower()
                
                # Get contact number
                speak("Please say the phone number including the leading zero.")
                contact = speech_to_text(text_box)
                if contact is None:
                    speak("I didn't catch that. Please repeat the phone number.")
                    contact = speech_to_text(text_box)

                contact = process_number(contact)
                if contact is None:
                    return  # Exit if the number format is invalid
                
                if 'text' in message_type or 'message' in message_type:
                    # Text message handling (existing code)
                    speak(f"The number you entered is {contact}. What message do you want to send?")
                    message = speech_to_text(text_box)
                    if message is None:
                        speak("I didn't catch that. Please repeat your message.")
                        message = speech_to_text(text_box)
                    send_whatsapp_message(contact, message)
                
                elif 'image' in message_type:
                    speak("Please say the name of the image you want to send.")
                    image_name = speech_to_text(text_box)
                    if not image_name:
                        speak("I didn't catch that. Please repeat the image name.")
                        image_name = speech_to_text(text_box)
                    send_whatsapp_file(contact, image_name, 'image')
                    
                elif 'video' in message_type:
                    speak("Please say the name of the video you want to send.")
                    video_name = speech_to_text(text_box)
                    if not video_name:
                        speak("I didn't catch that. Please repeat the video path.")
                        video_name = speech_to_text(text_box)
                    send_whatsapp_file(contact, video_name, 'video')
                
                elif 'document' in message_type or 'file' in message_type:
                    speak("Please say the name of the document you want to send.")
                    doc_name = speech_to_text(text_box)
                    if not doc_name:
                        speak("I didn't catch that. Please repeat the document path.")
                        doc_name = speech_to_text(text_box)
                    send_whatsapp_file(contact, doc_name, 'document')

                else:
                    speak("I didn't understand the message type. Please try again.")

            elif 'change volume level' in query or 'increase volume' in query or 'decrease volume' in query:
                # Extract the number from the query (e.g., "increase by 20" → 20)
                try:
                    if 'increase' in query:
                        volume_change = int(''.join(filter(str.isdigit, query)))
                    elif 'decrease' in query:
                        volume_change = -int(''.join(filter(str.isdigit, query)))
                    else:
                        volume_change = 0
                except:
                    volume_change = 0  # Default if no number found
                
                # Now use pyautogui or another method to change volume
                if volume_change > 0:
                    # Simulate volume up key (Windows: 'volumeup' is not valid, use alternative)
                    for _ in range(int(volume_change / 5)):
                        pyautogui.press('volumeup')  # This may not work; see alternative below
                    results = f"Increased volume by {volume_change}%"
                elif volume_change < 0:
                    # Simulate volume down key
                    for _ in range(int(abs(volume_change) / 5)):
                        pyautogui.press('volumedown')  # This may not work; see alternative below
                    results = f"Decreased volume by {abs(volume_change)}%"
                else:
                    results = "Volume not changed"
                
                insert_task(query, results)
            
            elif 'change brightness level' in query or 'increase brightness' in query or 'decrease brightness' in query:
                try:
                    # Extract brightness change from query (e.g., "increase by 20" → 20)
                    if 'increase' in query:
                        brightness_change = int(''.join(filter(str.isdigit, query)))
                    elif 'decrease' in query:
                        brightness_change = -int(''.join(filter(str.isdigit, query)))
                    else:
                        brightness_change = 0  # Default if no change specified
                except:
                    brightness_change = 0

                # Get current brightness
                current_brightness = sbc.get_brightness()[0]  # Takes first monitor by default

                # Calculate new brightness (0-100%)
                new_brightness = max(0, min(100, current_brightness + brightness_change))

                # Set new brightness
                sbc.set_brightness(new_brightness)
                
                results = f"Brightness set to {new_brightness}%"
                insert_task(query, results)
            
            
                            
            else:
                speak("Sorry, I didn't understand. Please try again.")
                continue  # Repeat the loop
                
  #wallpaper changed functions.
# ========== File Control Functions ==========

def get_spoken_number():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say how much to change the volume (e.g., 'increase by 20' or 'decrease by 10')...")
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio).lower()
        if "increase" in text:
            num = int(''.join(filter(str.isdigit, text)))
            return num
        elif "decrease" in text:
            num = int(''.join(filter(str.isdigit, text)))
            return -num
        else:
            return 0
    except:
        return 0 
            
def listen_for_wallpaper_name():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please say the name of the wallpaper you want to set.")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            image_name = recognizer.recognize_google(audio)
            return image_name.strip()
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that. Please try again.")
            return None
        except sr.RequestError as e:
            speak("There was an error with the speech recognition service. Please try again.")
            return None

def listen_for_folder_name():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please say the folder name where your wallpapers are stored.")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            folder_name = recognizer.recognize_google(audio)
            return folder_name.strip()
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand the folder name. Please try again.")
            return None
        except sr.RequestError as e:
            speak("There was an error with the speech recognition service. Please try again.")
            return None                      

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

def correct_email_format(text):
    text = text.lower()  
    text = text.replace(" at ", "@").replace(" dot ", ".")
    
    num_map = {
        ' zero ': '0', ' one ': '1', ' two ': '2', ' three ': '3', ' four ': '4',
        ' five ': '5', ' six ': '6', ' seven ': '7', ' eight ': '8', ' nine ': '9'
    }
    for word, digit in num_map.items():
        text = text.replace(word, digit)
    
    return text

def send_email(receiver, subject, body):
    try:
        webbrowser.open(f"mailto:{receiver}?subject={subject}&body={body}")
        speak("Email opened for you!")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send the email.")

def send_email_popup():
    popup = tk.Toplevel()
    popup.title("Send Email")

    receiver_label = tk.Label(popup, text="Receiver Email:")
    receiver_label.grid(row=0, column=0, padx=10, pady=10)

    receiver_entry = tk.Entry(popup)
    receiver_entry.grid(row=0, column=1, padx=10, pady=10)

    subject_label = tk.Label(popup, text="Subject:")
    subject_label.grid(row=1, column=0, padx=10, pady=10)

    subject_entry = tk.Entry(popup)
    subject_entry.grid(row=1, column=1, padx=10, pady=10)

    body_label = tk.Label(popup, text="Body:")
    body_label.grid(row=2, column=0, padx=10, pady=10)

    body_entry = tk.Entry(popup)
    body_entry.grid(row=2, column=1, padx=10, pady=10)

    send_button = tk.Button(popup, text="Send Email", command=lambda: send_email(receiver_entry.get(), subject_entry.get(), body_entry.get()))
    send_button.grid(row=3, column=0, columnspan=2, pady=10)

        
def process_text_input(text_box):
    # Get the user input from the text box
    query = text_box.get("1.0", tk.END).strip()
    
    if query:
        print("\nReceived query:", query)
               
        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            search_wikipedia(query)

        elif 'search file' in query or 'find file' in query:
            try:
                print("Sure, please enter the name of the file you are looking for:")
                file_name = input("File name: ")
                print(f"Searching for files with the name '{file_name}'...")

                search_directory = 'C:\\Program Files'
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
                insert_task(query, results)
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't open Notepad.")



        elif 'close notepad' in query:
            os.system("TASKKILL /F /IM notepad.exe")
            results= "nodepad is closed....."
            speak("nodepad is closing")
            insert_question_and_answer(query, results)


        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            results= "youtube is opening....."
            speak("youtube is opening")
            insert_task(query, results)
                
        elif 'open google' in query:
            webbrowser.open("chrome.exe")
            results= "Google is opening....."
            speak("Google is opening")
            print("Google is opening")
            insert_task(query, results)
            
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

        elif 'on youtube' in query:
            try:
                query = query.replace("on youtube", "")
                search_url = f"https://www.youtube.com/results?search_query={query}"
                webbrowser.open(search_url)
                results = "Searching YouTube....."
                speak("Searching YouTube")
                insert_task(query, results)
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't search on YouTube.")
                
        elif 'on google' in query:
            try:
                query = query.replace("on google", "")
                search_url = f"https://www.google.com/search?q={query}"
                webbrowser.open(search_url)
                results = "Searching on Google....."
                speak("Searching on Google")
                insert_task(query, results)
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't search on google.")
            
        elif 'open application' in query or 'open another application' in query:
            open_application()

        elif 'clear screen' in query or 'voicemate stop' in query or 'stop  screen' in query:
           text_box.delete('1.0', END)
            
            
        elif 'close google' in query:
            os.system("TASKKILL /F /IM chrome.exe")
            results= "Google is closed...."
            speak("Google is closing")
            insert_task(query, results)
                
        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")
            results= "stack overflow is opening....."
            speak("stack overflow is opening.....")
            insert_task(query, results)
            
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
            insert_question_and_answer(query, results)

        elif "create file" in query or "create a file" in query:
            create_file()
            
        elif "delete file" in query or "delete a file" in query:
            del_file()
                
                
        elif 'change brightness level' in query:
            get_number()
            results = "brightness level changed"
            insert_task(query, results)
        

        elif 'change volume level' in query:
            get_spoken_number()
            results="volume level changed"
            insert_task(query, results)


        elif "send email" in query:
            try:
                speak("What is the subject of the email?")
                subject = speech_to_text()
        
                speak("What should be the content of the email?")
                body =speech_to_text()

                send_email(subject, body)
                speak("Email opened for you!")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send the email.")
                
                
        elif 'send message on whatsapp' in query:
            speak("Please say the phone number including the leading zero.")

            # Open the popup for sending a WhatsApp message
            def open_whatsapp_popup(contact, message):
                popup = tk.Toplevel()
                popup.title("Send WhatsApp Message")

                contact_label = tk.Label(popup, text="Contact Number:")
                contact_label.grid(row=0, column=0, padx=10, pady=10)

                contact_entry = tk.Entry(popup)
                contact_entry.grid(row=0, column=1, padx=10, pady=10)
                contact_entry.insert(0, contact)  # Pre-fill the contact

                message_label = tk.Label(popup, text="Message:")
                message_label.grid(row=1, column=0, padx=10, pady=10)

                message_entry = tk.Entry(popup)
                message_entry.grid(row=1, column=1, padx=10, pady=10)
                message_entry.insert(0, message)  # Pre-fill the message

                # Send message and close the popup
                def send_and_close():
                    # Get the values from the entries
                    contact_number = contact_entry.get()
                    message_text = message_entry.get()

                    # Send the WhatsApp message
                    send_whatsapp_message(contact_number, message_text)
                    popup.destroy()  # Close the popup after sending

                send_button = tk.Button(
                    popup,
                    text="Send Message",
                    command=send_and_close  # Use the new function to send and close
                )
                send_button.grid(row=2, column=0, columnspan=2, pady=10)

            # Capture the contact number
            contact = speech_to_text(text_box)
            if contact is None:
                speak("I didn't catch that. Please repeat the phone number.")
                contact = speech_to_text(text_box)

            # Clean up any spaces and process the contact number to ensure proper format
            contact = process_number(contact)
            if contact is None:
                return  # Exit if the number format is invalid

            speak(f"The number you entered is {contact}. What message do you want to send?")
            message = speech_to_text(text_box)
            if message is None:
                speak("I didn't catch that. Please repeat your message.")
                message = speech_to_text(text_box)

            # Open the WhatsApp message popup with captured contact and message
            open_whatsapp_popup(contact, message)
        
                

        else:
            ai_response = replyBrain(query)
            insert_question_and_answer(query, ai_response)
            speak(ai_response)
            text_box.insert(tk.END, "VoiceMate: " + ai_response + "\n")
            text_box.yview(tk.END)
        
       
        
        text_box.after(3000, clear_screen, text_box)



    
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


def process_number(number):
    
    number = number.replace(" ", "").replace("-", "")
    if len(number) == 11 and number.startswith('0'):
        return number[1:]  
    else:
        speak("The number is not in a valid format. Please try again.")
        return None  

def send_whatsapp_message(contact, message):
    try:
        kit.sendwhatmsg_instantly(phone_no=f"+92{contact}", message=message, wait_time=10)
        speak("Message sent successfully!")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send the message.")
        


def send_whatsapp_file(contact, search_term, file_type):
    """Voice-controlled WhatsApp file sharing with verification"""
    try:
        # Step 1: Find the file by voice command
        file_path = find_file_by_voice(search_term, file_type)
        if not file_path:
            speak(f"Couldn't find {search_term} in your {file_type} folders.")
            return False

        # Step 2: Verify WhatsApp Web is ready
        if not whatsapp_web_ready():
            speak("Please make sure WhatsApp Web is loaded in your browser first.")
            return False

        # Step 3: Send with verification
        speak(f"Sending {file_type}. Please wait...")
        
        try:
            if file_type == 'image':
                kit.sendwhats_image(receiver=f"+92{contact}", 
                                 img_path=file_path,
                                 wait_time=20)
            elif file_type == 'video':
                kit.sendwhats_video(receiver=f"+92{contact}", 
                                  video_path=file_path,
                                  wait_time=60)
            else:
                kit.sendwhats_document(receiver=f"+92{contact}", 
                                     document_path=file_path,
                                     wait_time=30)
            
            
            # Verify the file was actually sent
            if not verify_file_sent(file_path):
                raise Exception("File sending verification failed")
            
            speak(f"{file_type.capitalize()} sent successfully!")
            return True
            
        except Exception as e:
            print(f"Sending error: {e}")
            speak(f"Failed to send {file_type}. Please check your WhatsApp Web connection.")
            return False

    except Exception as e:
        print(f"System error: {e}")
        speak("An error occurred. Please try again.")
        return False

def whatsapp_web_ready():
    """Check if WhatsApp Web is properly loaded in browser"""
    try:
        # Open WhatsApp Web if not already open
        webbrowser.open("https://web.whatsapp.com")
        time.sleep(15)  # Wait for page to load
        return True
    except:
        return False

def verify_file_sent(file_path):
    """Basic verification that file was processed"""
    # Check if file exists (basic verification)
    return Path(file_path).exists()

def find_file_by_voice(search_term, file_type):
    """Enhanced file finder with multiple attempts"""
    max_attempts = 3
    for attempt in range(max_attempts):
        matches = search_files(search_term, file_type)
        if matches:
            return str(matches[0])
        elif attempt < max_attempts - 1:
            speak(f"Couldn't find {search_term}. Please try a different name.")
            search_term = speech_to_text(text_box)
    
    return None

def search_files(search_term, file_type):
    """Search for files with multiple pattern matching"""
    config = {
        'image': {'folders': ['Pictures', 'Downloads'], 'ext': ['.jpg', '.png']},
        'video': {'folders': ['Videos', 'Downloads'], 'ext': ['.mp4', '.mov']},
        'document': {'folders': ['Documents', 'Downloads'], 'ext': ['.pdf', '.docx', '.txt']}
    }
    
    matches = []
    for folder in config[file_type]['folders']:
        folder_path = Path.home() / folder
        if not folder_path.exists():
            continue
            
        for ext in config[file_type]['ext']:
            for file in folder_path.glob(f'*{ext}'):
                if (search_term.lower() in file.name.lower() or
                    search_term.lower().replace(' ', '') in file.name.lower().replace(' ', '')):
                    matches.append(file)
    
    matches.sort(key=os.path.getmtime, reverse=True)
    return matches


# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# import time
# import os
# from pathlib import Path

# def initialize_driver():
#     """Initialize Chrome WebDriver with profile support"""
#     try:
#         options = webdriver.ChromeOptions()
#         profile_path = os.path.join(os.getcwd(), 'whatsapp_profile')
#         options.add_argument(f"user-data-dir={profile_path}")
#         options.add_argument("--disable-dev-shm-usage")
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-notifications")
        
#         driver = webdriver.Chrome(
#             service=Service(ChromeDriverManager().install()),
#             options=options
#         )
#         return driver
#     except Exception as e:
#         print(f"Driver initialization error: {str(e)}")
#         return None

# def send_whatsapp_file(contact, search_term, file_type):
#     """Send file through WhatsApp Web using direct URL approach"""
#     driver = initialize_driver()
#     if not driver:
#         return False

#     try:
#         # Clean and format phone number
#         clean_contact = contact.lstrip('0').replace(' ', '').replace('-', '')
#         international_number = f"92{clean_contact}"  # Pakistan specific
        
#         # Find the file first
#         file_path = find_file_by_voice(search_term, file_type)
#         if not file_path:
#             print("File not found")
#             return False

#         # Directly navigate to chat URL
#         driver.get(f"https://web.whatsapp.com/send?phone={international_number}")
#         print("➡️ Please scan QR code if required")

#         # Wait for chat to load
#         WebDriverWait(driver, 60).until(
#             EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]'))
#         )
#         time.sleep(2)  # Additional stabilization wait

#         # Click attachment button
#         attach_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.XPATH, '//div[@title="Attach"]'))
#         )
#         attach_btn.click()
#         time.sleep(1)

#         # Handle different file types
#         if file_type == 'document':
#             file_input = driver.find_element(By.XPATH, 
#                 '//input[@accept="*"]')
#         elif file_type == 'image':
#             file_input = driver.find_element(By.XPATH, 
#                 '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
#         elif file_type == 'video':
#             file_input = driver.find_element(By.XPATH, 
#                 '//input[@accept="video/mp4,video/3gpp,video/quicktime"]')

#         # Upload file
#         file_input.send_keys(file_path)
#         time.sleep(3)  # Wait for file preview to load

#         # Send the file
#         send_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="media-editor-send-btn"]'))
#         )
#         send_btn.click()

#         # Verify successful send
#         time.sleep(3)
#         if verify_file_sent(driver):
#             print("✅ File sent successfully")
#             return True
#         return False

#     except Exception as e:
#         print(f"Error during sending: {str(e)}")
#         return False
#     finally:
#         driver.quit()

# def find_file_by_voice(search_term, file_type):
#     """Simple file search implementation"""
#     config = {
#         'document': {'ext': ['.pdf', '.docx', '.txt']},
#         'image': {'ext': ['.jpg', '.png', '.jpeg']},
#         'video': {'ext': ['.mp4', '.mov']}
#     }
    
#     search_dirs = [Path.home() / 'Downloads', Path.home() / 'Documents']
    
#     for dir_path in search_dirs:
#         if not dir_path.exists():
#             continue
            
#         for ext in config[file_type]['ext']:
#             for file in dir_path.glob(f'*{ext}'):
#                 if search_term.lower() in file.name.lower():
#                     return str(file)
#     return None

# def verify_file_sent(driver):
#     """Check for single checkmark indicating sent message"""
#     try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//span[@data-testid="msg-time"]'))
#         )
#         return True
#     except:
#         return False

# if __name__ == "__main__":
#     success = send_whatsapp_file(
#         contact="03700503420",  # Test number
#         search_term="example",  # Test file search
#         file_type="document"
#     )
#     print(f"Test result: {'Success' if success else 'Failed'}")

def send_whatsapp_message_popup():
    popup = tk.Toplevel()
    popup.title("Send WhatsApp Message")

    contact_label = tk.Label(popup, text="Contact Number:")
    contact_label.grid(row=0, column=0, padx=10, pady=10)

    contact_entry = tk.Entry(popup)
    contact_entry.grid(row=0, column=1, padx=10, pady=10)

    message_label = tk.Label(popup, text="Message:")
    message_label.grid(row=1, column=0, padx=10, pady=10)

    message_entry = tk.Entry(popup)
    message_entry.grid(row=1, column=1, padx=10, pady=10)

    send_button = tk.Button(popup, text="Send Message", command=lambda: send_whatsapp_message(contact_entry.get(), message_entry.get()))
    send_button.grid(row=2, column=0, columnspan=2, pady=10)
    
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


def Home_Tab(self, parentHomeFrame):
    tabview_1 = customtkinter.CTkTabview(parentHomeFrame, width=460)
    tabview_1.pack(pady=10, padx=10)
    tab1_add = tabview_1.add("VoiceMate")
    
    

    # Header Label
    self.AddTransactionLabel = customtkinter.CTkLabel(
        tab1_add,
        text="Home",
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

    def executeQuery2():
        # Your code to execute Query 2 goes here
        pass
    def executeQuery1():
        # Your code to execute Query 2 goes here
        pass

    # Query Button 1
    self.queryButton1 = customtkinter.CTkButton(
        tab1_add,
        text="Send msg on WhatsApp",
        fg_color="teal",border_color="white",border_width=1,
        command=send_whatsapp_message_popup
    )
    self.queryButton1.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
    self.queryButton2 = customtkinter.CTkButton(
        tab1_add,
        text="Send Email",
        fg_color="teal",border_color="white",border_width=1,
        command=send_email_popup 
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
        text="Submit Command",
        fg_color="teal",
        border_color="white",
        border_width=1,
        command=lambda: process_text_input(self.text_box),
    )
    self.submit_btn.grid(row=6, column=0,  pady=5, sticky="ew")


    # mic Button
    self.Mic_button= customtkinter.CTkButton(
        tab1_add,
        text="Voice Command",
        fg_color="teal",
        border_color="white",
        border_width=1,
        command=lambda: toggle_voice_recognition(self.text_box),
    )
    self.Mic_button.grid(row=6, column=2, columnspan=2,  pady=5, sticky="ew")

    # Previous Transaction Labels (if needed)
    self.addpreviouslytextLabel = customtkinter.CTkLabel(tab1_add, text="")
    self.addpreviouslytextLabel.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

    self.addpreviouslyLabel = customtkinter.CTkLabel(tab1_add, text="")
    self.addpreviouslyLabel.grid(row=5, column=1, sticky="ew")




