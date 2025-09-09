import os
import glob
import speech_recognition as sr
import pyttsx3

# Initialize speech recognition and text-to-speech synthesis
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Function to convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Function to listen for voice commands and return the recognized text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, could not understand your command.")
        return ""
    except sr.RequestError:
        print("Could not request results; please check your internet connection.")
        return ""

def create_files():
    """Create a new file based on user input."""
    speak("What should be the name of the file?")
    filename = listen()

    if filename:
        speak("What should be the extension of the file?")
        extension = listen()

        if extension:
            filename_with_extension = f"{filename.strip()}.{extension.strip()}"
            speak(f"Please speak the content of the file {filename_with_extension}.")
            content = listen()

            if content:
                try:
                    with open(filename_with_extension, 'w') as f:
                        f.write(content)
                    speak(f"File '{filename_with_extension}' created successfully.")
                except Exception as e:
                    speak(f"Error creating file '{filename_with_extension}': {e}")
            else:
                speak("Content not recognized. File creation cancelled.")
        else:
            speak("Extension not recognized. File creation cancelled.")
    else:
        speak("Filename not recognized. File creation cancelled.")


def delete_file(filename):
    """Delete an existing file using the specified filename."""
    files = glob.glob(f"{filename}*")  # Search for files starting with the provided filename
    if files:
        try:
            for file in files:
                os.remove(file)
            speak(f"Files starting with name'{filename}' deleted successfully.")
        except Exception as e:
            speak(f"Error deleting files starting with '{filename}': {e}")
    else:
        speak(f"No files found starting with '{filename}'.")

def del_file():
    speak("Please specify the name of the file to delete.")
    filename = listen()
    if filename:
        delete_file(filename.strip())
    else:
        speak("Filename not recognized. File deletion cancelled.")

# Main interaction loop
if __name__ == "__main__":
    speak("Hello! How can I assist you today?")

    while True:
        speak("What would you like me to do?")
        command = listen()

        if "create a file" in command:
            create_files()
        elif "delete a file" in command:
            del_file()
        elif "exit" in command:
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I didn't understand that command. Can you repeat?")
