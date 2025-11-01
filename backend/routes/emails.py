from flask import Blueprint, jsonify, session, request
from services.gmail_service import GmailService
from services.classifier import EmailClassifier
from models.email import Email
from database import db
from datetime import datetime
import re

emails_bp = Blueprint('emails', __name__)

@emails_bp.route('/emails', methods=['GET'])
def get_emails():
    if 'credentials' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        gmail_service = GmailService(session['credentials'])
        classifier = EmailClassifier()
        
        # Get user email
        user_info = gmail_service.get_user_info()
        user_email = user_info.get('emailAddress')
        
        # Check if we should force refresh
        force_refresh = request.args.get('refresh', 'false').lower() == 'true'
        
        if not force_refresh:
            # Check if we have cached emails
            cached_emails = list(db.emails.find({'user_email': user_email}).sort('date', -1))
            if cached_emails:
                return jsonify({
                    'emails': [Email.from_dict(e) for e in cached_emails],
                    'total': len(cached_emails),
                    'cached': True
                })
        
        # Fetch fresh emails from Gmail
        messages = gmail_service.fetch_job_emails(max_results=100)
        
        emails_data = []
        for msg in messages:
            # Check if email already exists
            existing = db.emails.find_one({
                'user_email': user_email,
                'gmail_id': msg['id']
            })
            
            if existing and not force_refresh:
                emails_data.append(Email.from_dict(existing))
                continue
            
            # Parse email details
            subject = msg.get('subject', 'No Subject')
            sender = msg.get('from', 'Unknown')
            body = msg.get('snippet', '')
            date_str = msg.get('date', '')
            
            # Extract company name
            company = extract_company(sender)
            
            # Classify email
            status = classifier.classify(subject, body)
            
            # Parse date
            try:
                email_date = datetime.strptime(date_str[:16], '%a, %d %b %Y')
            except:
                email_date = datetime.utcnow()
            
            # Create email object
            email_obj = Email(
                user_email=user_email,
                gmail_id=msg['id'],
                subject=subject,
                sender=sender,
                company=company,
                status=status,
                date=email_date,
                snippet=body[:500]
            )
            
            # Upsert to database
            db.emails.update_one(
                {'user_email': user_email, 'gmail_id': msg['id']},
                {'$set': email_obj.to_dict()},
                upsert=True
            )
            
            email_dict = email_obj.to_dict()
            email_dict['id'] = msg['id']
            emails_data.append(Email.from_dict(email_dict))
        
        return jsonify({
            'emails': emails_data,
            'total': len(emails_data),
            'cached': False
        })
        
    except Exception as e:
        print(f"Error in get_emails: {str(e)}")
        return jsonify({'error': str(e)}), 500

@emails_bp.route('/stats', methods=['GET'])
def get_stats():
    if 'credentials' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        gmail_service = GmailService(session['credentials'])
        user_info = gmail_service.get_user_info()
        user_email = user_info.get('emailAddress')
        
        # Aggregate stats from MongoDB
        pipeline = [
            {'$match': {'user_email': user_email}},
            {'$group': {
                '_id': '$status',
                'count': {'$sum': 1}
            }}
        ]
        
        results = list(db.emails.aggregate(pipeline))
        
        stats = {
            'total': 0,
            'rejection': 0,
            'selection': 0,
            'pending': 0,
            'unread': 0
        }
        
        for result in results:
            status = result['_id']
            count = result['count']
            stats['total'] += count
            if status == 'Rejection':
                stats['rejection'] = count
            elif status == 'Selection':
                stats['selection'] = count
            elif status == 'Pending':
                stats['pending'] = count
        
        # Count unread
        stats['unread'] = db.emails.count_documents({
            'user_email': user_email,
            'read': False
        })
        
        return jsonify(stats)
        
    except Exception as e:
        print(f"Error in get_stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@emails_bp.route('/emails/<email_id>/read', methods=['POST'])
def mark_as_read(email_id):
    if 'credentials' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        gmail_service = GmailService(session['credentials'])
        user_info = gmail_service.get_user_info()
        user_email = user_info.get('emailAddress')
        
        db.emails.update_one(
            {'user_email': user_email, 'gmail_id': email_id},
            {'$set': {'read': True}}
        )
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_company(sender):
    """Extract company name from email sender"""
    # Try to extract from email format "Company Name <email@company.com>"
    if '<' in sender and '>' in sender:
        company_name = sender.split('<')[0].strip()
        if company_name and not '@' in company_name:
            return company_name
        
        # Extract from email domain
        email = sender.split('<')[1].split('>')[0]
        domain = email.split('@')[1] if '@' in email else ''
        company = domain.split('.')[0] if domain else 'Unknown'
        
        # Clean up common email domains
        if company.lower() in ['gmail', 'yahoo', 'outlook', 'hotmail', 'mail']:
            return 'Unknown'
        
        return company.capitalize()
    
    # Try to extract from plain email
    if '@' in sender:
        domain = sender.split('@')[1].split('.')[0]
        if domain.lower() not in ['gmail', 'yahoo', 'outlook', 'hotmail', 'mail']:
            return domain.capitalize()
    
    return 'Unknown'