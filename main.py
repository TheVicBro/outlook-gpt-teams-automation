import requests
import os
import openai
import imaplib
import email
import re
from openai import error
from base import CompletionResponse
from dotenv import load_dotenv

load_dotenv()

openai.organization = os.getenv("OPENAI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")
email_address = os.getenv("GMAIL_ADDRESS")
email_app_password = os.getenv("GMAIL_APP_PASSWORD")
target_address = os.getenv("TARGET_ADDRESS")
teams_webhook_url = os.getenv("TEAMS_WEBHOOK_URL")

def main():
    emails = get_all_unread_emails(email_address, email_app_password, target_address)
    if emails:
        for email_content in emails:
            response = get_completion(f"Given this email, write a reply:\n{email_content}")
            original_msg = "**Original Email:**\n\n" + email_content.replace('\n', '\n\n')
            if response.err:
                response_msg = "\n\n---\n\n**Response Error:**\n\n" + response.message.replace('\n', '\n\n')
            else:
                response_msg = "\n\n---\n\n**Reply:**\n\n" + response.payload.replace('\n', '\n\n')
            send_to_teams(original_msg + response_msg)
    else:
        print("No emails found")

def get_all_unread_emails(email_address, app_password, target_address):
    # Connect and login
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_address, app_password)
    mail.select('inbox')

    # Search for unread emails from the target address
    result, data = mail.search(None, '(UNSEEN FROM "{}")'.format(target_address))
    if result != 'OK':
        print(f"Error searching for emails: {result}")
        return None
    
    if not data or not data[0]:
        return []
    
    email_ids = data[0].split()
    email_bodies = []

    for email_id in email_ids:
        result, email_data = mail.fetch(email_id, '(RFC822)')
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        msg = email.message_from_string(raw_email_string)
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    email_bodies.append(clean_string(part.get_payload(decode=True).decode()))
        else:
            email_bodies.append(clean_string(msg.get_payload(decode=True).decode()))

        # Mark the email as read
        mail.store(email_id, '+FLAGS', '\\Seen')

    return email_bodies

def clean_string(s):
    # Remove non-alphanumeric characters except for newlines and spaces
    cleaned = re.sub(r'[^a-zA-Z0-9 \n]', '', s)
    
    # Remove extra consecutive newlines
    cleaned = re.sub(r'\n+', '\n', cleaned).strip()
    
    return cleaned

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

    print("\nTeams message sent\n")
    return response.status_code

if __name__ == "__main__":
    main()