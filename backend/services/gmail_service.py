from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.utils import parsedate_to_datetime
import base64

class GmailService:
    def __init__(self, credentials_dict):
        self.credentials = Credentials(**credentials_dict)
        self.service = build('gmail', 'v1', credentials=self.credentials)
    
    def get_user_info(self):
        """Get user's Gmail profile information"""
        return self.service.users().getProfile(userId='me').execute()
    
    def fetch_job_emails(self, max_results=50):
        """Fetch job-related emails from Gmail"""
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
                msg = self.service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()
                
                email_data = self._parse_message(msg)
                emails.append(email_data)
            
            return emails
            
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []
    
    def _parse_message(self, message):
        """Parse Gmail message into structured format"""
        headers = message['payload']['headers']
        
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'].lower() == 'date'), '')
        
        snippet = message.get('snippet', '')
        
        # Try to get body
        body = self._get_body(message['payload'])
        
        return {
            'id': message['id'],
            'subject': subject,
            'from': sender,
            'date': date,
            'snippet': body or snippet
        }
    
    def _get_body(self, payload):
        """Extract email body from payload"""
        if 'body' in payload and 'data' in payload['body']:
            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                elif 'parts' in part:
                    body = self._get_body(part)
                    if body:
                        return body
        
        return ''