from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.utils import parsedate_to_datetime
import base64


class GmailService:
    def __init__(self, credentials_dict):
        self.credentials = Credentials(**credentials_dict)
        self.service = build('gmail', 'v1', credentials=self.credentials)

    def get_user_info(self):
        return self.service.users().getProfile(userId='me').execute()

    def fetch_job_emails(self, max_results=35):
        query = (
            'subject:(application OR interview OR position OR job OR opportunity OR '
            'career OR hiring OR recruitment OR candidate OR role OR offer) '
            'newer_than:6m'
        )

        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            emails = []

            for message in messages:
                full_message = self.service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()

                parsed = self._parse_message(full_message)
                emails.append(parsed)

            return emails

        except Exception as e:
            print("Error fetching emails:", e)
            return []

    def _parse_message(self, message):
        headers = message['payload'].get('headers', [])

        subject = next(
            (h['value'] for h in headers if h['name'].lower() == 'subject'),
            'No Subject'
        )

        sender = next(
            (h['value'] for h in headers if h['name'].lower() == 'from'),
            'Unknown'
        )

        date = next(
            (h['value'] for h in headers if h['name'].lower() == 'date'),
            ''
        )

        body = self._extract_body(message['payload'])

        # Fallback to Gmail snippet if body extraction fails
        if not body:
            body = message.get('snippet', '')

        return {
            'id': message['id'],
            'subject': subject,
            'from': sender,
            'date': date,
            'snippet': body
        }

    def _extract_body(self, payload):
        """
        Recursively extract text/plain content
        """
        if payload.get('mimeType') == 'text/plain':
            data = payload.get('body', {}).get('data')
            if data:
                return base64.urlsafe_b64decode(data).decode(
                    'utf-8',
                    errors='ignore'
                )

        if 'parts' in payload:
            for part in payload['parts']:
                text = self._extract_body(part)
                if text:
                    return text

        return ""