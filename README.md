# power-apps-openai-teams-automation

## Overview

This tool provides an automated solution for generating responses to IT tickets originating from York's Halo system. Utilizing advanced natural language processing capabilities, it assesses the content of each ticket and crafts a relevant and helpful response, allowing for quick and efficient handling of IT queries.

## Features

- **Email Integration**: Directly fetches unread IT ticket emails from the specified Gmail account.
- **Intelligent Response Generation**: Uses OpenAI's GPT model to analyze ticket content and generate appropriate replies.
- **Microsoft Teams Integration**: Sends both the original ticket details and generated responses to a designated Microsoft Teams channel for easy review and further action.

## How It Works

1. **Ticket Forwarding via Power Apps**: When an IT ticket is received in the York Halo system, Power Apps automatically forwards this ticket email to a designated personal Gmail account. This step ensures that the tool can access the ticket details without directly interfacing with the York email system.
2. **Email Retrieval**: The tool connects to the personal Gmail account via IMAP, looking specifically for the forwarded IT ticket emails.
3. **Ticket Analysis**: Each retrieved email is cleaned and preprocessed to extract the main content of the IT ticket.
4. **Response Creation**: The cleaned ticket content is fed into the OpenAI GPT model, which generates a relevant response based on its training on a vast array of IT-related conversations.
5. **Teams Notification**: Both the original ticket content and the generated response are sent to a specified Microsoft Teams channel using Incoming Webhooks. This allows the IT team to review and take further action if needed.
