import speech_recognition as sr
import pyttsx3
import webbrowser
import time
import musiclibrary
from client import ask_ai

recognizer = sr.Recognizer()

def speak(text):
    print(f"Guruji says: {text}")  # <-- print what Guruji speaks
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def listen(timeout=5, phrase_limit=5):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Heard: {text}")  # <-- print recognized speech
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""

def handle_command(command: str):
    command = command.lower()
    print(f"Processing command: {command}")  # <-- print the command

    # Music
    if "play" in command:
        played = False
        for genre in musiclibrary.songs:
            if genre in command:
                for song_name in musiclibrary.songs[genre]:
                    if song_name in command:
                        url = musiclibrary.songs[genre][song_name]
                        print(f"Playing {song_name} ({genre})")
                        speak(f"Playing {song_name}")
                        webbrowser.open(url)
                        played = True
                        break
                if not played:
                    first_song = list(musiclibrary.songs[genre].values())[0]
                    print(f"Playing a {genre} song")
                    speak(f"Playing a {genre} song")
                    webbrowser.open(first_song)
                    played = True
        if not played:
            print("Song not found")
            speak("Song not found")
        return

    # Web
    if "youtube" in command:
        print("Opening YouTube")
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com/")
        return
    if "google" in command:
        print("Opening Google")
        speak("Opening Google")
        webbrowser.open("https://www.google.com/")
        return
    if "linkedin" in command:
        print("Opening LinkedIn")
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com/")
        return

    # AI query
    print(f"Asking AI: {command}")
    speak("Let me think...")
    answer = ask_ai(command)
    print(f"AI answered: {answer}")
    speak(answer)

if __name__ == "__main__":
    speak("Initializing Guruji... Say 'Guruji' to wake me up.")

    while True:
        try:
            word = listen(timeout=5, phrase_limit=3).lower()
            if "guruji" in word:
                print("Wake word detected.")
                speak("Yes, it's Guruji. How can I help you?")
                time.sleep(0.3)

                # Continuous conversation mode until user says "stop" or "sleep"
                while True:
                    command = listen()
                    if any(x in command.lower() for x in ["stop", "sleep", "bye"]):
                        print("Sleep command detected. Going back to sleep mode.")
                        speak("Going back to sleep mode.")
                        break
                    handle_command(command)

        except sr.WaitTimeoutError:
            print("⏳ No speech detected, retrying...")
            continue
        except sr.UnknownValueError:
            print("❌ Speech unintelligible")
            speak("Sorry, I didn't catch that.")
        except Exception as e:
            print(f"Unexpected Error: {e}")
