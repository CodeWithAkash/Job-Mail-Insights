A powerful web application that connects to Gmail via OAuth2, fetches job-related emails, and classifies them into Rejection, Selection, and Pending categories with beautiful analytics and insights.

![JobMail Insight Dashboard](https://via.placeholder.com/800x400/4F46E5/FFFFFF?text=JobMail+Insight+Dashboard)

## ✨ Features

- 🔐 **Gmail OAuth2 Authentication** - Secure login with Google
- 📊 **Smart Email Classification** - AI-powered categorization (Rejection/Selection/Pending)
- 📈 **Beautiful Analytics Dashboard** - Interactive charts and graphs
- 🎨 **Modern UI/UX** - Sleek, responsive design with dark/light mode
- 💾 **MongoDB Database** - Persistent storage for email data
- 🔍 **Search & Filter** - Find emails quickly by company or status
- 📥 **CSV Export** - Download your data anytime
- ⚡ **Fast & Efficient** - Optimized performance with caching

## 🏗️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **MongoDB** - Database
- **Google Gmail API** - Email fetching
- **PyMongo** - MongoDB driver

### Frontend
- **React 18** - UI framework
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Lucide React** - Icons
- **Axios** - HTTP client

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**
- **Node.js 16 or higher**
- **MongoDB** (local or Atlas)
- **Google Cloud Project** with Gmail API enabled

## 🚀 Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/jobmail-insight.git
cd jobmail-insight
```

### 2️⃣ Setup MongoDB

#### Option A: Local MongoDB
```bash
# Install MongoDB (Ubuntu/Debian)
sudo apt-get install mongodb

# Start MongoDB service
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Verify MongoDB is running
sudo systemctl status mongodb
```

#### Option B: MongoDB Atlas (Cloud)
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Get your connection string (e.g., `mongodb+srv://username:password@cluster.mongodb.net/`)

### 3️⃣ Setup Google OAuth2 Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Gmail API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Gmail API"
   - Click "Enable"

4. Create OAuth2 Credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Choose "Web application"
   - Add authorized redirect URIs:
     - `http://localhost:5000/api/auth/callback` (for local development)
   - Download the JSON credentials

5. Configure OAuth Consent Screen:
   - Go to "APIs & Services" → "OAuth consent screen"
   - Add test users (your Gmail account)
   - Add scopes: `https://www.googleapis.com/auth/gmail.readonly`

### 4️⃣ Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env file with your credentials
nano .env  # or use any text editor
```

**Edit `backend/.env`:**
```env
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
REDIRECT_URI=http://localhost:5000/api/auth/callback
SECRET_KEY=your-super-secret-key-change-this-in-production
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=jobmail_insight
FRONTEND_URL=http://localhost:3000
```

**Run the backend:**
```bash
python app.py
```

Backend should now be running on `http://localhost:5000`

### 5️⃣ Frontend Setup

Open a new terminal window:
```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Edit .env file
nano .env  # or use any text editor
```

**Edit `frontend/.env`:**
```env
REACT_APP_API_URL=http://localhost:5000/api
```

**Run the frontend:**
```bash
npm start
```

Frontend should now be running on `http://localhost:3000`

### 6️⃣ Access the Application

1. Open your browser and go to `http://localhost:3000`
2. Click "Connect Gmail Account"
3. Sign in with your Google account
4. Grant permissions to read Gmail
5. Wait for emails to be fetched and classified
6. Explore your job application insights!

## 📁 Project Structure
```
jobmail-insight/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Configuration management
│   ├── database.py            # MongoDB connection
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment variables template
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentication routes
│   │   └── emails.py         # Email management routes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gmail_service.py  # Gmail API integration
│   │   └── classifier.py     # Email classification logic
│   └── models/
│       ├── __init__.py
│       └── email.py          # Email data model
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── StatsCards.jsx
│   │   │   ├── Charts.jsx
│   │   │   └── EmailTable.jsx
│   │   ├── context/
│   │   │   └── ThemeContext.jsx
│   │   ├── utils/
│   │   │   ├── api.js
│   │   │   └── exportCSV.js
│   │   ├── App.jsx
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   ├── tailwind.config.js
│   └── .env.example
└── README.md
```

## 🔧 Configuration

### Email Classification Keywords

Edit `backend/services/classifier.py` to customize classification:
```python
self.rejection_keywords = [
    'regret', 'unfortunately', 'not selected',
    # Add more keywords...
]

self.selection_keywords = [
    'congratulations', 'selected', 'interview',
    # Add more keywords...
]
```

### MongoDB Indexes

The application automatically creates indexes for optimal performance:
- Compound index on `user_email` and `gmail_id`
- Index on `user_email` and `date`
- Index on `user_email` and `status`

## 🚀 Deployment

### Backend Deployment (Render/Railway/Heroku)

#### Render Deployment

1. Create a `render.yaml` file in the backend directory:
```yaml
services:
  - type: web
    name: jobmail-insight-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:create_app()
    envVars:
      - key: GOOGLE_CLIENT_ID
        sync: false
      - key: GOOGLE_CLIENT_SECRET
        sync: false
      - key: MONGODB_URI
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: FRONTEND_URL
        value: https://your-frontend-url.vercel.app
```

2. Add `gunicorn` to `requirements.txt`:
```txt
gunicorn==21.2.0
```

3. Push to GitHub and connect to Render
4. Set environment variables in Render dashboard

#### Railway Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd backend
railway init

# Deploy
railway up
```

#### Heroku Deployment

1. Create `Procfile` in backend directory:
```
web: gunicorn app:create_app()
```

2. Deploy:
```bash
heroku create jobmail-insight-api
heroku config:set GOOGLE_CLIENT_ID=your_id
heroku config:set GOOGLE_CLIENT_SECRET=your_secret
# Set other environment variables...
git push heroku main
```

### Frontend Netlify Deployment
```bash
cd frontend

# Install Netlify CLI
npm install -g netlify-cli

# Build the project
npm run build

# Deploy
netlify deploy --prod
```

Add environment variables in Netlify dashboard.

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🐛 Troubleshooting

### MongoDB Connection Issues
```bash
# Check MongoDB status
sudo systemctl status mongodb

# Check MongoDB logs
sudo journalctl -u mongodb

# Test connection
mongo --eval "db.version()"
```

### Gmail API Issues

1. **"Access blocked" error**: Add your email as a test user in Google Cloud Console
2. **"Redirect URI mismatch"**: Verify the URI in Google Cloud Console matches your `.env` file
3. **Rate limiting**: Gmail API has quotas - check your usage in Google Cloud Console

### CORS Issues

Make sure both frontend and backend URLs are correctly set in `.env` files and CORS is properly configured.

## 📚 API Documentation

### Authentication Endpoints

#### `GET /api/auth/login`
Initiate Gmail OAuth2 flow
```json
Response: {
  "auth_url": "https://accounts.google.com/o/oauth2/auth?..."
}
```

#### `GET /api/auth/callback`
OAuth2 callback handler (redirects to frontend)

#### `GET /api/auth/status`
Check authentication status
```json
Response: {
  "authenticated": true
}
```

#### `POST /api/auth/logout`
Logout user
```json
Response: {
  "message": "Logged out successfully"
}
```

### Email Endpoints

#### `GET /api/emails?refresh=false`
Fetch classified emails
```json
Response: {
  "emails": [...],
  "total": 50,
  "cached": true
}
```

#### `GET /api/stats`
Get email statistics
```json
Response: {
  "total": 50,
  "rejection": 20,
  "selection": 15,
  "pending": 15,
  "unread": 5
}
```

#### `POST /api/emails/<email_id>/read`
Mark email as read
```json
Response: {
  "success": true
}
```

## 🔐 Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use strong SECRET_KEY** in production
3. **Enable HTTPS** in production
4. **Restrict MongoDB access** with authentication
5. **Use environment variables** for all sensitive data
6. **Regularly rotate credentials**
7. **Implement rate limiting** on API endpoints

## 🎨 Customization

### Change Theme Colors

Edit `frontend/tailwind.config.js`:
```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#4F46E5',  // Your primary color
        secondary: '#7C3AED', // Your secondary color
      }
    }
  }
}
```

### Add More Classification Categories

1. Edit `backend/services/classifier.py`
2. Add new keyword lists
3. Update classification logic
4. Update frontend components to handle new categories

### Improve ML Classification

Replace rule-based classifier with ML model:
```python
# In classifier.py
from transformers import pipeline

class EmailClassifier:
    def __init__(self):
        self.classifier = pipeline("text-classification", 
                                   model="your-model-name")
    
    def classify(self, subject, body):
        result = self.classifier(f"{subject} {body}")
        return result[0]['label']
```

## 📈 Performance Optimization

1. **Enable caching** for repeated email fetches
2. **Implement pagination** for large email lists
3. **Use indexes** in MongoDB for faster queries
4. **Lazy load** email content
5. **Compress API responses** with gzip

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gmail API for email access
- MongoDB for database
- React and Flask communities
- All contributors and supporters

## 📧 Contact

For questions or support, please open an issue or contact:
- Email: your.email@example.com
- Twitter: [@yourhandle](https://twitter.com/yourhandle)

## 🗺️ Roadmap

- [ ] Add email sentiment analysis
- [ ] Implement email response templates
- [ ] Add calendar integration for interview scheduling
- [ ] Create mobile app (React Native)
- [ ] Add machine learning model training
- [ ] Support for multiple email accounts
- [ ] Email notifications for new responses
- [ ] Advanced analytics and insights
- [ ] Export to PDF reports
- [ ] Integration with job boards

---

**Made with ❤️ by Akash**

⭐ Star this repo if you find it helpful!