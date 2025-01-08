import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time
import cv2
import pytesseract

# Set Tesseract executable path if it's not in PATH
# Example for Windows:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

# Function to capture image from the webcam and perform OCR
def capture_and_read_image():
    # Open the webcam (use the default camera)
    cap = cv2.VideoCapture(0)

    # Give the camera a moment to warm up
    time.sleep(2)

    # Capture a single frame
    ret, frame = cap.read()

    if ret:
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Use pytesseract to extract text
        extracted_text = pytesseract.image_to_string(gray)

        if extracted_text:
            print("Extracted Text: " + extracted_text)
            talk("I found the following text in the image: " + extracted_text)
        else:
            talk("Sorry, I couldn't extract any text from the image.")

    # Release the camera after use
    cap.release()
    cv2.destroyAllWindows()

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
        elif 'read image' in command:
            talk("Reading image from the camera now.")
            capture_and_read_image()  # Call the function to capture image and read it
        else:
            talk('Sorry, I didn’t understand that. Please try again.')

# Continuously listen for commands
while True:
    run_alexa()
    time.sleep(2)  # Add a short delay between each command
