import os
from groq import Groq
from dotenv import load_dotenv

# 1. Load API Key
load_dotenv(override=True)
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

# 2. Initialize Groq client
client = Groq(api_key=api_key)

def run_translation(text):
    try:
        # 3. Translate using Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful translator. Always translate English sentences into clear, simple, and accurate Urdu. Output only the Urdu translation, no extra explanations."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        urdu_translation = response.choices[0].message.content
        
        # Print output in Urdu
        print(f"input: {text}")
        print(f"Outut: {urdu_translation}")

    except Exception as e:
        if "429" in str(e) or "rate limit" in str(e).lower():
            print("\n❌ حد عبور ہوگئی: آپ نے گروک کی مفت حد استعمال کر لی ہے۔")
            print("مزید معلومات: https://console.groq.com")
        else:
            print(f"خرابی پیش آگئی: {e}")

if __name__ == "__main__":
    run_translation("My name is khizar khattak . i am live in karachi")