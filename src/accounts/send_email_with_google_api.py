import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError


def send_mail(
    subject: str, message: str, from_email: str | None, recipient_list: list[str]
):
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    flow = InstalledAppFlow.from_client_secrets_file(
        "infra/client_secret_google_cloud_desktop.json", SCOPES
    )
    creds = flow.run_local_server(port=0)
    service = build("gmail", "v1", credentials=creds)
    msg = MIMEText(message)
    msg["to"] = recipient_list[0]
    msg["subject"] = subject
    create_message = {"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}
    try:
        message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )
        print(f'sent message to {msg["to"]} Message Id: {msg["id"]}')
    except HTTPError as error:
        print(f"An error occurred: {error}")
        msg = None
