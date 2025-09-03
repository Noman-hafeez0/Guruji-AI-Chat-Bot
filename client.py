import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")

# Store last 10 conversations
conversation_history = [
    {
        "role": "system",
        "content": (
            "You are Guruji, a wise and friendly assistant. "
            "Answer questions briefly and clearly. "
            "Use simple language. "
            "Do not use commas, hyphens, or long sentences. "
            "Keep answers ready to speak aloud. "
            "Give answers in Hinglish (Hindi + English) with a warm, helpful tone."
        )
    }
]

def ask_ai(question: str) -> str:
    global conversation_history

    # Add user question to history
    conversation_history.append({"role": "user", "content": question})

    # Keep only last 10 turns (system + 9 messages)
    if len(conversation_history) > 11:
        conversation_history = [conversation_history[0]] + conversation_history[-10:]

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Or whichever Groq model you want
            messages=conversation_history
        )

        answer = response.choices[0].message.content.strip()

        # Add AI reply to history
        conversation_history.append({"role": "assistant", "content": answer})

        return answer
    except Exception as e:
        return f"Groq API error: {e}"








# import os
# from dotenv import load_dotenv
# from google import genai

# # Load .env file
# load_dotenv()

# # Get your Gemini key
# gemini_key = os.getenv("GEMINI_KEY")
# if not gemini_key:
#     raise ValueError("GEMINI_KEY not found in .env file")

# # Initialize Gemini client
# client = genai.Client(api_key=gemini_key)

# def ask_ai(question: str) -> str:
#     """
#     Ask Gemini AI a question and get a short, clean answer for speech.
#     Guruji is a wise and friendly assistant who speaks in simple Hinglish.
#     """
#     prompt = (
#         "You are Guruji, a wise and friendly assistant. "
#         "Answer questions briefly and clearly. "
#         "Use simple language. "
#         "Do not use commas, hyphens, or long sentences. "
#         "Keep answers ready to speak aloud. "
#         "Give answers in Hinglish (Hindi + English) and add a warm, helpful tone. "
#         f"Question: {question}"
#     )

#     try:
#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=prompt  # just a string
#         )
#         return response.text.strip()
#     except Exception as e:
#         return f"Error connecting to Gemini AI: {e}"