## Personal E-Mail Assistant
This repository is a workflow for automatically categorizing and processing emails from an Outlook E-Mail inbox.

### How to set up the Authentication
1. Log in to entra.microsoft.com
2. Go to Applications - Enterprise applications - New application - Create your own application - Enter the application name and select "Register an application to integrate with Microsoft Entra ID (App you're developing)"
3. In your application go to "API permissions" and add from Microsoft Graph "Application.Read.All and Mail.Read" and give Administration consent for both permissions
5. In your application go to "Certificates & secrets" and add a new client secret. Add the value within the .env file as AZURE_CLIENT_SECRET.

## Prerequisites
- python installed (I'm useing version 3.9)
- pip package manager installed

### Setup
1. Clone the code from this repository
2. Copy the env.template file and change the name to ".venv"
3. Add your own credentials. The Credentials can be found on entra.microsoft.com in the Home-Tab and within your Enterprise Application
4. Run `pip install -r .\requirements.txt`
5. Run the assistant.py
