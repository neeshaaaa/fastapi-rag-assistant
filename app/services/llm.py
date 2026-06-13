import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in .env"
    )

client = genai.Client(
    api_key=api_key
)


from sqlalchemy.orm import Session
from app.db.models import Booking
from google.genai import types

def generate_answer(context: str, question: str, db: Session):

    prompt = f"""
You are a helpful assistant. Use the provided context to answer questions.
If the user wants to book an interview, you MUST collect their name, email, date, and time.
Once you have all 4 pieces of information, you MUST call the `book_interview` tool.
If you are missing any of these 4 pieces of information, ask the user for them.

Context:
{context}

Question:
{question}
"""

    def book_interview(name: str, email: str, date: str, time: str):
        """Book an interview with the user. Only call this when you have name, email, date, and time."""
        pass # We will handle this manually via function_calls

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[book_interview],
            temperature=0.0
        )
    )

    if response.function_calls:
        for fc in response.function_calls:
            if fc.name == "book_interview":
                args = fc.args
                # Save to db
                booking = Booking(
                    name=args.get("name", ""),
                    email=args.get("email", ""),
                    date=args.get("date", ""),
                    time=args.get("time", "")
                )
                db.add(booking)
                db.commit()
                return f"Great! Your interview is booked for {booking.date} at {booking.time}. A confirmation will be sent to {booking.email}."

    return response.text