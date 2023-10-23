import requests
import os
import openai
from openai import error
from base import CompletionResponse
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
teams_webhook_url = os.getenv("TEAMS_WEBHOOK_URL")

def main():
    response = get_completion("what is 1+1")
    if response.err:
        print(response.message)
        send_to_teams(response.message)
    else:
        print(response.payload)
        send_to_teams(response.payload)

def get_completion(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )  
    except error.OpenAIError as e:
        return CompletionResponse(message=e.args[0], err=type(e).__name__)
    return CompletionResponse(
        payload=response.choices[0].message["content"],
        message="OK",
        err="",
    )

def send_to_teams(message):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "@type": "MessageCard",
        "text": message
    }
    response = requests.post(teams_webhook_url, headers=headers, json=data)

    print("finished")
    return response.status_code

if __name__ == "__main__":
    main()