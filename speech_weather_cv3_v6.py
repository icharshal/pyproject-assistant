import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import time
import requests
import webbrowser
import pyautogui
import pytesseract
import cv2

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

# Function to capture image from the webcam and perform OCR
def capture_and_read_image():
    cap = cv2.VideoCapture(0)

    time.sleep(2)

    ret, frame = cap.read()

    if ret:
        # Show the image preview (captured frame)
        cv2.imshow("Image Preview", frame)  # Display the captured image in a window
        cv2.waitKey(1)  # Wait for 1 millisecond to display the image

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the image to grayscale for OCR
        extracted_text = pytesseract.image_to_string(gray)

        if extracted_text:
            print("Extracted Text: " + extracted_text)
            talk("I found the following text in the image: " + extracted_text)
        else:
            talk("Sorry, I couldn't extract any text from the image.")

    # Close the preview window after a short delay
    time.sleep(2)
    cv2.destroyAllWindows()  # Close the preview window
    cap.release()  # Release the webcam

# Function to get current weather (using a weather API like OpenWeatherMap)
def get_weather():
    api_key = "cf300cca427a5d4741ba82c0b5ad50fb"  # Replace with your OpenWeatherMap API key
    city = "Nagpur"  # Change to your desired city
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={21.15}&lon={79.1}&appid={api_key}"
#    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        weather_info = data['main']
        temperature = weather_info['temp']
        humidity = weather_info['humidity']
        weather_desc = data['weather'][0]['description']
        talk(f"The weather in {city} is {weather_desc} with a temperature of {temperature}°C and humidity of {humidity}%.")
    else:
        talk("Sorry, I couldn't retrieve the weather information.")

# Function to open websites or apps
def open_website(command):
    if 'open' in command:
        website = command.replace('open', '').strip()
        webbrowser.open(f"http://{website}")
        talk(f"Opening {website}")

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
            elif 'weather' in command:
                talk("Sure! Let me get the weather information for you.")
                get_weather()  # Get weather details
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
