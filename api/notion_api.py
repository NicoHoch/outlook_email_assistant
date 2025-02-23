import os
import requests


def get_leads():
    notion_api_secret = os.environ["NOTION_API_SECRET"]
    notion_crm_db_id = os.environ["NOTION_CRM_DB_ID"]

    url = f"https://api.notion.com/v1/databases/{notion_crm_db_id}/query"
    headers = {
        "Authorization": f"Bearer {notion_api_secret}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    response = requests.post(url, headers=headers)
    return response.json()


def add_lead_to_crm(name, company, email_category, email_subject):
    notion_api_secret = os.environ["NOTION_API_SECRET"]
    notion_crm_db_id = os.environ["NOTION_CRM_DB_ID"]

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {notion_api_secret}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    data = {
        "parent": {"database_id": notion_crm_db_id},
        "icon": {"emoji": "🤖"},
        "properties": {
            "Name": {"title": [{"text": {"content": name}}]},
            "Company": {"rich_text": [{"text": {"content": company}}]},
            "Status": {"status": {"name": "Lead"}},
        },
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": name}}]
                },
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"Kontakt automatisch aufgenommen durch Personal-Email-Assistant. E-Mail Kategorie ist '{email_category}', Betreff ist '{email_subject}'",
                            },
                        }
                    ]
                },
            },
        ],
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()
