import os   # system files open close etc...
import subprocess  # for subprocess 
from vosk import Model, KaldiRecognizer
from pages.database import insert_task
import pyaudio
import webbrowser
import pyttsx3
import datetime
import random
import ctypes
import sys


engine = pyttsx3.init()  

def speak(text_to_speak):
    engine.say(text_to_speak)
    engine.runAndWait()

engine = pyttsx3.init()

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
        

def listen():
    model = Model("C:\\Users\\ThinkPad\\Desktop\\vosk-model-small-en-us-0.15\\vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model, 16000)

    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("Listening...")
    try:
        while True:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data):
                text = recognizer.Result()
                query = text[14:-3]
                print(f"You Said : {query}")

                if len(query) > 0:
                    return query

    except Exception as e:
        print(f"Error: {e}")

    finally:
        stream.stop_stream()
        stream.close()
        mic.terminate()

def words_to_numbers(words):
    number_dict = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10
        
    }
    return number_dict.get(words, -1)
    
def Search_file():
    try:
            
            print("Sure, please tell me the name of the file you are looking for.")
            speak("Sure, please tell me the name of the file you are looking for.")
            file_name = listen()
            print(f"Searching for files with the name '{file_name}'...")
            speak(f"Searching for files with the name '{file_name}'...")

            search_directory = 'C://Program Files'
            files = find_files(search_directory, file_name)

            if files:
                print(f"Voice Mate found {len(files)} files:")
                for i, file_path in enumerate(files, 1):
                    print(f"{i}. {file_path}")

                print("Do you want to open any of these files?")
                speak("Do you want to open any of these files?")
                response = listen().lower()

                if "open" in response:
                    print("Sure, please tell me the number of the file you want to open.")
                    speak("Sure, please tell me the number of the file you want to open.")
                    try:
                        file_number_words = listen().lower()
                        file_number = words_to_numbers(file_number_words)

                        if file_number != -1 and 1 <= file_number <= len(files):
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


if __name__ == "__main__":
      Search_file()



