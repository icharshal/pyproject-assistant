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
import openai

# Set your OpenAI API key
openai.api_key = " "

# Set Tesseract executable path if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize the speech recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Set up voices for TTS (Text-to-Speech) engine
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change to `voices[0].id` for a male voice
engine.setProperty('rate', 180)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

# Function to speak text
def talk(text):
    print(f"Assistant: {text}")  # Print the response for visibility
    engine.say(text)
    engine.runAndWait()

# Function to capture voice command
def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(voice).lower()
            print(f"Command: {command}")
            return command
    except sr.UnknownValueError:
        return "I couldn't understand that."
    except sr.RequestError:
        return "Error with the speech recognition service."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to process commands with OpenAI
def process_with_openai(command):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful, conversational assistant."},
                {"role": "user", "content": command}
            ],
 #           temperature=0.7
        )
        reply = response['choices'][0]['message']['content']
        return reply
    except Exception as e:
        return f"An error occurred while processing the command: {str(e)}"

#Function to handle predefined commands
def process_command(command):
    if 'play' in command:
        song = command.replace('play', '').strip()
        talk(f"Playing {song} on YouTube.")
        pywhatkit.playonyt(song)
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The current time is {current_time}.")
    elif 'who is' in command or 'what is' in command:
        query = command.replace('who is', '').replace('what is', '').strip()
        try:
            info = wikipedia.summary(query, sentences=2)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk("There are multiple results for that query. Please be more specific.")
        except Exception:
            talk("Sorry, I couldn't find any information on that.")
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
        # Pass the command to OpenAI for handling general queries
        reply = process_with_openai(command)
        talk(reply)
    return True

# Function to open websites
def open_website(command: str):
    try:
        website = command.replace('open website', '').strip().replace(' ', '')
        if not website.startswith('http://') and not website.startswith('https://'):
            website = 'http://' + website
        webbrowser.open(website)
        talk(f"Opening {website}.")
    except Exception as e:
        talk(f"Sorry, I couldn't open the website. Error: {e}")

# Function to open apps
def open_app(command):
    try:
        app_name = command.replace('open app', '').strip()
        pyautogui.hotkey('win', 'r')
        time.sleep(1)
        pyautogui.write(app_name)
        pyautogui.press('enter')
        talk(f"Opening {app_name}.")
    except Exception as e:
        talk(f"Sorry, I couldn't open the application. Error: {e}")

# Main function to run the assistant
def run_assistant():
    talk("Say 'orange' to activate me.")
    while True:
        trigger = take_command()
        if 'orange' in trigger:
            talk("I'm listening. How can I assist you?")
            while True:
                command = take_command()
                if command:
                    if not process_command(command):
                        return
                else:
                    talk("I didn't catch that. Please repeat.")

# Run the assistant
run_assistant()
