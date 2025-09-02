import os
from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv()

# Get your Gemini key
gemini_key = os.getenv("GEMINI_KEY")
if not gemini_key:
    raise ValueError("GEMINI_KEY not found in .env file")

# Initialize Gemini client
client = genai.Client(api_key=gemini_key)

def ask_ai(question: str) -> str:
    """
    Ask Gemini AI a question and get a short, clean answer for speech.
    Guruji is a wise and friendly assistant who speaks in simple Hinglish.
    """
    prompt = (
        "You are Guruji, a wise and friendly assistant. "
        "Answer questions briefly and clearly. "
        "Use simple language. "
        "Do not use commas, hyphens, or long sentences. "
        "Keep answers ready to speak aloud. "
        "Give answers in Hinglish (Hindi + English) and add a warm, helpful tone. "
        f"Question: {question}"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt  # just a string
        )
        return response.text.strip()
    except Exception as e:
        return f"Error connecting to Gemini AI: {e}"