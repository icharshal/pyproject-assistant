import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time
import webbrowser
import pyautogui
import pytesseract
import cv2
import openai

# Set your OpenAI API key
openai.api_key = " "

# Set Tesseract executable path if it's not in PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize the speech recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Set up voices for TTS (Text-to-Speech) engine
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Index 1 is female, change for male voice

# Set speech rate and volume
engine.setProperty('rate', 180)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

# Function to speak text
def talk(text):
    engine.say(text)
    engine.runAndWait()

# Function to capture voice command
def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)  # Reduce background noise
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)  # Set timeout and phrase time
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f"Command received: {command}")
            return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError:
        print("Sorry, I couldn't connect to the speech recognition service.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to open websites
def open_website(command: str):
    try:
        website = command.replace('open', '').strip().replace(' ', '')
        if not website.startswith('http://') and not website.startswith('https://'):
            website = 'http://' + website
        webbrowser.open(website)
        talk(f"Opening {website}")
    except Exception as e:
        talk(f"Sorry, I couldn't open the website. Error: {e}")

# Function to open apps
def open_app(command):
    try:
        app_name = command.replace('open', '').replace('app', '').strip()
        pyautogui.hotkey('win', 'r')
        time.sleep(1)
        pyautogui.write(app_name)
        pyautogui.press('enter')
        talk(f"Opening {app_name}")
    except Exception as e:
        talk(f"Sorry, I couldn't open the application. Error: {e}")

# Function to process commands using OpenAI
def process_command_with_openai(command):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful virtual assistant."},
                {"role": "user", "content": command}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return reply
    except Exception as e:
        return f"Sorry, I couldn't process your request. Error: {e}"

# Function to process voice commands
def process_command(command):
    if 'play' in command:
        song = command.replace('play', '').strip()
        talk(f'Playing {song}')
        pywhatkit.playonyt(song)
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f'The current time is {current_time}')
    elif 'who is' in command or 'what is' in command:
        try:
            query = command.replace('who is', '').replace('what is', '').strip()
            info = wikipedia.summary(query, sentences=2)
            talk(info)
        except Exception as e:
            talk(f"Sorry, I couldn't find information on that. Error: {e}")
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'open website' in command:
        open_website(command)
    elif 'open app' in command or 'open application' in command:
        open_app(command)
    elif 'exit' in command or 'stop' in command:
        talk("Goodbye!")
        return False
    else:
        # Use OpenAI for other natural language commands
        reply = process_command_with_openai(command)
        talk(reply)
    return True

# Main function to run the assistant
def run_assistant():
    while True:
        talk("Say the trigger word to activate me.")
        trigger = take_command()
        if trigger and 'orange' in trigger:
            talk("I am now listening for commands. How can I help?")
            while True:
                command = take_command()
                if command:
                    if not process_command(command):
                        return
                else:
                    talk("I didn't catch that. Please repeat.")

# Run the assistant
run_assistant()
