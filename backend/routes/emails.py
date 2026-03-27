from flask import Blueprint, jsonify, session, request
from services.gmail_service import GmailService
from services.classifier import EmailClassifier
from models.email import Email
from database import db
from datetime import datetime
import re

emails_bp = Blueprint('emails', __name__)


def get_gmail_service():
    if not session.get('authenticated'):
        return None

    creds_data = session.get('credentials')
    if not creds_data:
        return None

    return GmailService(creds_data)


# -------- Company Extraction --------

def extract_company(sender):

    # Example: "Google Careers <jobs-noreply@google.com>"
    if "<" in sender:
        name = sender.split("<")[0].strip()
        if name and "@" not in name:
            return name

        email = sender.split("<")[1].split(">")[0]
    else:
        email = sender

    # Extract domain
    match = re.search(r'@([a-zA-Z0-9\-]+)', email)

    if match:
        company = match.group(1)

        # ignore generic email providers
        ignore = ["gmail", "yahoo", "outlook", "hotmail", "mail"]

        if company.lower() not in ignore:
            return company.capitalize()

    return "Unknown"


# -------- EMAIL FETCH ROUTE --------

@emails_bp.route('/emails', methods=['GET'])
def get_emails():

    gmail_service = get_gmail_service()

    if not gmail_service:
        return jsonify({'error': 'Not authenticated'}), 401

    try:

        if db.emails is None:
            return jsonify({'error': 'Database not connected'}), 500

        classifier = EmailClassifier()

        user_info = gmail_service.get_user_info()
        user_email = user_info.get('emailAddress')

        force_refresh = request.args.get('refresh', 'false').lower() == 'true'

        # -------- Cached Emails --------

        if not force_refresh:

            cached = list(
                db.emails
                .find({'user_email': user_email})
                .sort('date', -1)
            )

            if cached:
                return jsonify({
                    'emails': [Email.from_dict(e) for e in cached],
                    'total': len(cached),
                    'cached': True
                })

        # -------- Fetch Gmail --------

        messages = gmail_service.fetch_job_emails(max_results=15)

        emails_data = []

        for msg in messages:

            subject = msg.get('subject', 'No Subject')
            sender = msg.get('from', 'Unknown')
            body = msg.get('snippet', '')
            date_str = msg.get('date', '')

            try:
                email_date = datetime.strptime(date_str[:16], '%a, %d %b %Y')
            except:
                email_date = datetime.utcnow()

            # Classification
            status = classifier.classify(subject, body)

            # Company detection
            company = extract_company(sender)

            email_dict = {
                'user_email': user_email,
                'gmail_id': msg['id'],
                'subject': subject,
                'sender': sender,
                'company': company,
                'status': status,
                'date': email_date,
                'snippet': body[:500],
                'read': False
            }

            # -------- DB UPDATE --------

            if force_refresh:

                db.emails.update_one(
                    {
                        'user_email': user_email,
                        'gmail_id': msg['id']
                    },
                    {'$set': email_dict},
                    upsert=True
                )

            else:

                db.emails.update_one(
                    {
                        'user_email': user_email,
                        'gmail_id': msg['id']
                    },
                    {'$setOnInsert': email_dict},
                    upsert=True
                )

            emails_data.append(Email.from_dict(email_dict))

        return jsonify({
            'emails': emails_data,
            'total': len(emails_data),
            'cached': False
        })

    except Exception as e:

        print("Error in get_emails:", str(e))

        return jsonify({'error': str(e)}), 500


# -------- STATS ROUTE --------

@emails_bp.route('/stats', methods=['GET'])
def get_stats():

    gmail_service = get_gmail_service()

    if not gmail_service:
        return jsonify({'error': 'Not authenticated'}), 401

    try:

        if db.emails is None:
            return jsonify({'error': 'Database not connected'}), 500

        user_info = gmail_service.get_user_info()
        user_email = user_info.get('emailAddress')

        pipeline = [
            {'$match': {'user_email': user_email}},
            {'$group': {'_id': '$status', 'count': {'$sum': 1}}}
        ]

        results = list(db.emails.aggregate(pipeline))

        stats = {
            'total': 0,
            'rejection': 0,
            'selection': 0,
            'pending': 0,
            'unread': 0
        }

        for r in results:

            stats['total'] += r['count']

            if r['_id'] == 'Rejection':
                stats['rejection'] = r['count']

            elif r['_id'] == 'Selection':
                stats['selection'] = r['count']

            elif r['_id'] == 'Pending':
                stats['pending'] = r['count']

        stats['unread'] = db.emails.count_documents({
            'user_email': user_email,
            'read': False
        })

        return jsonify(stats)

    except Exception as e:

        print("Error in get_stats:", str(e))

        return jsonify({'error': str(e)}), 500