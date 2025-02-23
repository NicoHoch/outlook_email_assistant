from api.openai_api import OpenAIClient


def summarize_email(email_content):
    messages = [
        {
            "role": "system",
            "content": "You are an email summarizer. Summarize this email to the most important points. Keep it short and concise.",
        },
        {"role": "user", "content": email_content},
    ]

    openai_client = OpenAIClient()

    result = openai_client.call_openai(messages, model="gpt-4o-mini")

    return result
