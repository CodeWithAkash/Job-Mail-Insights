from datetime import datetime
from bson import ObjectId

class Email:
    def __init__(self, user_email, gmail_id, subject, sender, company, status, date, snippet):
        self.user_email = user_email
        self.gmail_id = gmail_id
        self.subject = subject
        self.sender = sender
        self.company = company
        self.status = status
        self.date = date
        self.snippet = snippet
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'user_email': self.user_email,
            'gmail_id': self.gmail_id,
            'subject': self.subject,
            'sender': self.sender,
            'company': self.company,
            'status': self.status,
            'date': self.date,
            'snippet': self.snippet,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data):
        """Convert MongoDB document to Email object"""
        return {
            'id': str(data.get('_id')),
            'gmail_id': data.get('gmail_id'),
            'subject': data.get('subject'),
            'sender': data.get('sender'),
            'company': data.get('company'),
            'status': data.get('status'),
            'date': data.get('date').strftime('%Y-%m-%d') if isinstance(data.get('date'), datetime) else data.get('date'),
            'snippet': data.get('snippet'),
            'read': data.get('read', False)
        }