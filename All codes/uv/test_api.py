import requests

GEMINI_API_KEY = "YOUR_API_KEY"
url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
headers = {
    "Authorization": f"Bearer {GEMINI_API_KEY}",
    "Content-Type": "application/json"
}
data = {
    "model": "gemini-1.5-flash",
    "messages": [{"role": "user", "content": "Say hello"}]
}
response = requests.post(url, headers=headers, json=data)
print(response.status_code, response.text)