# 📧 JobMail Insight

JobMail Insight is a full-stack AI-powered web application that connects to your Gmail account and automatically analyzes job application emails.  

It classifies emails into:

- ✅ Selection
- ❌ Rejection
- ⏳ Pending

The system uses Google OAuth for secure authentication, MongoDB Atlas for cloud storage, and an NLP-based Machine Learning classifier built with Scikit-learn.

---

## 🚀 Live Demo

Frontend: https://jobmail.akash-codes.space  
Backend API: https://api.akash-codes.space

---

## 🏗️ Tech Stack

### Frontend
- React.js
- Tailwind CSS
- Axios
- React Router

### Backend
- Flask
- Gunicorn
- Flask-CORS
- Google OAuth 2.0
- MongoDB Atlas
- Scikit-learn (TF-IDF + Logistic Regression)

### Deployment
- Frontend: Netlify
- Backend: Render
- Database: MongoDB Atlas

---

## 🔐 Authentication Flow

1. User clicks **Connect Gmail**
2. Redirected to Google OAuth
3. Backend receives authorization code
4. Access + refresh token stored in Flask session
5. Gmail API used to fetch job-related emails

---

## 🧠 Machine Learning Model

The email classification model uses:

- TF-IDF Vectorization
- Logistic Regression
- 300 labeled training samples
- Balanced class weighting

The model is trained offline and saved as:
