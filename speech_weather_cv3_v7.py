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
    command = ""
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)  # Reduce background noise
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)  # Set timeout and phrase time
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f"Command received: {command}")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError:
        print("Sorry, I couldn't connect to the speech recognition service.")
    except Exception as e:
        print(f"Error: {e}")
    return command

# Function to open websites
def open_website(command):
    if 'open' in command:
        website = command.replace('open', '').strip()
        
        # Ensure the website starts with 'http://' or 'https://'
        if not website.startswith('http://') and not website.startswith('https://'):
            website = 'http://' + website
        
        try:
            # Attempt to open the website
            webbrowser.open(website)
            talk(f"Opening {website}")
        except Exception as e:
            talk(f"Sorry, I couldn't open {website}. Please check the URL or try again later.")

# Function to process commands related to apps
def open_app(command):
    if 'open' in command:
        app_name = command.replace('open', '').replace('app', '').strip()
        pyautogui.hotkey('win', 'r')
        time.sleep(1)
        pyautogui.write(app_name)
        pyautogui.press('enter')
        talk(f"Opening {app_name}")

# Main function to run Alexa-like assistant
def run_alexa():
    command = take_command()

    # Detect the "trigger word" (e.g., "orange")
    if 'orange' in command:
        talk("I am now listening for commands. How can I help?")
        
        while True:
            command = take_command()  # Keep listening for commands

            if 'play' in command:
                song = command.replace('play', '').strip()
                talk(f'Playing {song}')
                pywhatkit.playonyt(song)
            elif 'time' in command:
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                talk(f'The current time is {current_time}')
            elif 'who the heck is' in command:
                person = command.replace('who the heck is', '').strip()
                info = wikipedia.summary(person, 1)
                print(info)
                talk(info)
            elif 'date' in command:
                talk('Sorry, I have a headache today.')
            elif 'are you single' in command:
                talk('I am in a relationship with WiFi.')
            elif 'joke' in command:
                talk(pyjokes.get_joke())
            elif 'open' in command and 'website' in command:
                open_website(command)
            elif 'open' in command and ('app' in command or 'application' in command):
                open_app(command)
            elif 'read image' in command:
                talk("Reading image from the camera now.")
                capture_and_read_image()  # Call the function to capture image and read it
            elif 'exit' in command or 'stop' in command:
                talk("Goodbye!")
                break  # Stop the command loop and return to listening for "orange"
            else:
                talk('Sorry, I didn’t understand that. Please try again.')

# Continuously listen for the trigger word ("orange")
while True:
    run_alexa()
    time.sleep(2)  # Add a short delay between each listening cycle
