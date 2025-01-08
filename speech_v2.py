import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time

# Initialize the speech recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Set up voices for TTS (Text-to-Speech) engine
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Index 1 is female, change for male voice

# Set speech rate and volume
engine.setProperty('rate', 150)  # Speed of speech
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
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(f"Command received: {command}")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError:
        print("Sorry, I couldn't connect to the speech recognition service.")
    except Exception as e:
        print(f"Error: {e}")
    return command

# Main function to run Alexa-like assistant
def run_alexa():
    command = take_command()
    if command:
        print(f"Command: {command}")
        
        # Handling different commands
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
            website = command.replace('open', '').replace('website', '').strip()
            pywhatkit.search(f"open {website}")
            talk(f"Opening {website}")
        else:
            talk('Sorry, I didn’t understand that. Please try again.')

# Continuously listen for commands
while True:
    run_alexa()
    time.sleep(2)  # Add a short delay between each command
