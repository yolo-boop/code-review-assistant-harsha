# Code Review Assistant

An AI-powered code review tool that analyzes code quality, identifies bugs, security issues, and provides improvement suggestions using Google Gemini AI.

## Features

- AI-Powered Analysis: Uses Google Gemini 1.5 Flash for intelligent code review
- Multi-Language Support: JavaScript, Python, Java, C++, Go, Rust, and more
- Comprehensive Metrics:
  - Overall code quality score (0-10)
  - Readability analysis
  - Best practices compliance
  - Security vulnerability detection
  - Performance optimization suggestions
  - Bug identification with fixes
- Interactive Dashboard: Modern, responsive UI built with React and Vite
- Review History: Track and revisit previous code reviews
- File Upload: Support for direct file uploads or code paste

## Tech Stack

### Backend
- Flask
- Google Gemini API
- Flask-CORS
- Python 3.8+

### Frontend
- React
- Vite
- Axios
- Lucide React
- CSS3

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- Google Gemini API key

### Backend Setup
1. Clone the repository:
```bash
git clone <repo-url>
cd code-review-assistant
Navigate to backend and create virtual environment:

bash
Copy code
cd backend
python -m venv venv
Activate virtual environment:

Windows: venv\Scripts\activate

Mac/Linux: source venv/bin/activate

Install dependencies:

bash
Copy code
pip install -r requirements.txt
Create .env file:

text
Copy code
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
PORT=5000
Run the backend:

bash
Copy code
python app.py
Backend will start on http://localhost:5000

Frontend Setup
Open a new terminal and navigate to frontend:

bash
Copy code
cd frontend
Install dependencies:

bash
Copy code
npm install
Start the development server:

bash
Copy code
npm run dev
Frontend will start on http://localhost:5173

Usage
Open your browser and go to http://localhost:5173

Either:

Upload a code file, or

Paste your code directly

Set filename and programming language

Click "Review Code"

Wait 5-10 seconds for AI analysis

View results including:

Overall quality score

Detailed metrics breakdown

Identified bugs and security issues

Concrete improvement suggestions with code examples

API Endpoints
Health Check
bash
Copy code
GET /api/health
Response: {"status": "healthy", "timestamp": "..."}
Submit Code Review
css
Copy code
POST /api/review
Body: {
  "code": "string",
  "filename": "string",
  "language": "string"
}
Response: {
  "success": true,
  "reviewId": number,
  "analysis": {...}
}
Get All Reviews
bash
Copy code
GET /api/reviews
Response: {
  "success": true,
  "count": number,
  "reviews": [...]
}
Get Specific Review
bash
Copy code
GET /api/reviews/:id
Response: {
  "success": true,
  "review": {...}
}
Delete Review
bash
Copy code
DELETE /api/reviews/:id
Response: {
  "success": true,
  "message": "Review deleted"
}
Project Structure
css
Copy code
code-review-assistant/
├── backend/
│   ├── venv/
│   ├── app.py
│   ├── .env
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
Configuration
Backend .env:

GEMINI_API_KEY: Google Gemini API key

FLASK_ENV: development/production

PORT: backend port

Frontend:

API URL set in src/App.jsx as http://localhost:5000/api (update for production)

Limitations
Gemini Free Tier Limits:

15 requests per minute

1,500 requests per day

Reviews are stored in memory and will be lost on server restart

Use a database for persistent storage in production

Future Enhancements
Database integration

User authentication and multi-user support

GitHub integration for direct PR reviews

More language support

Export reports as PDF

Real-time collaborative code review

CI/CD pipeline integration

Code diff comparison

Custom review rules


#License
MIT License

#Acknowledgments
Google Gemini AI

React and Vite communities

Flask framework

Lucide icon library