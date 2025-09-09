
import json
import subprocess
import speech_recognition as sr



def speak(text_to_speak):
    engine.say(text_to_speak)
    engine.runAndWait()

def open_application_by_voice_command(user_input, mapping_file="pages/mapping.json"):
    try:
        with open(mapping_file, "r") as file:
            application_mapping = json.load(file)

        normalized_input = user_input.lower()

        matched_application = application_mapping.get(normalized_input)

        if matched_application:
            subprocess.Popen([matched_application], shell=True)
            return f"Opened {matched_application} successfully."
        else:
            return f"No matching application found for '{user_input}'."

    except Exception as e:
        return f"Error opening application: {e}"

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for voice command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        user_input = recognizer.recognize_google(audio).strip()
        print("You said:", user_input)
        return user_input
    except sr.UnknownValueError:
        return "Sorry, I could not understand what you said."
    except sr.RequestError as e:
        return f"Sorry, could not request results from Google Speech Recognition service: {e}"

def open_application():
    user_input = get_voice_input()
    result = open_application_by_voice_command(user_input)
    print(result)

if __name__ == "__main__":
    open_application()
