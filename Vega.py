import pyttsx3
import speech_recognition as sr
import wikipedia
import datetime
import pywhatkit
import os

# Initialize text-to-speech engine
engine = pyttsx3.init()


def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()


def take_command():
    """Listen for user commands and return as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce noise
        try:
            audio = recognizer.listen(source, timeout=5)  # Timeout after 5 seconds
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            print("Network error. Please check your internet connection.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None


def process_command(command):
    """Process user commands."""
    if command is None:
        return

    if "who is" in command:
        person = command.replace("who is", "").strip()
        speak(f"Searching Wikipedia for {person}")
        try:
            info = wikipedia.summary(person, sentences=2)
            speak(info)
            print(info)
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"Multiple results found. {e.options[:3]}. Please specify more clearly.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find any information on that topic.")

    elif "time" in command or "what is the time now" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
        print(f"The time is {current_time}")

    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {current_date}")
        print(f"Today's date is {current_date}")

    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")

    elif "search google for" in command or "google" in command:
        query = command.replace("search google for", "").replace("google", "").strip()
        speak(f"Searching Google for {query}")
        os.system(f"start https://www.google.com/search?q={query}")

    elif "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)

    elif "exit" in command or "stop" in command:
        speak("Goodbye! Have a great day.")
        exit()

    else:
        speak("Sorry, I didn't understand that command.")


def main():
    speak("Hello! I am VEGA, your AI assistant. How can I assist you?")

    while True:
        command = take_command()
        if command:
            process_command(command)


if __name__ == "__main__":
    main()
