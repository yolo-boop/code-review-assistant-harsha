# Code Review Assistant 🔍

An AI-powered code review tool that analyzes code quality, identifies bugs, security issues, and provides improvement suggestions using Google Gemini AI.

## Features ✨

- **AI-Powered Analysis**: Uses Google Gemini 1.5 Flash for intelligent code review
- **Multi-Language Support**: JavaScript, Python, Java, C++, Go, Rust, and more
- **Comprehensive Metrics**:
  - Overall code quality score (0-10)
  - Readability analysis
  - Best practices compliance
  - Security vulnerability detection
  - Performance optimization suggestions
  - Bug identification with fixes
- **Interactive Dashboard**: Modern, responsive UI built with React and Vite
- **Review History**: Track and revisit previous code reviews
- **File Upload**: Support for direct file uploads or code paste

## Tech Stack 🛠️

### Backend
- **Flask** - Python web framework
- **Google Gemini API** - AI code analysis
- **Flask-CORS** - Cross-origin resource sharing
- **Python 3.8+**

### Frontend
- **React** - UI library
- **Vite** - Build tool
- **Axios** - HTTP client
- **Lucide React** - Icon library
- **CSS3** - Styling

## Installation 📦

### Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- Google Gemini API key (free tier available)

### Backend Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd code-review-assistant
```

2. Navigate to backend and create virtual environment:
```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
PORT=5000
```

5. Get your Gemini API key:
   - Visit https://aistudio.google.com/app/apikey
   - Create a new API key
   - Copy and paste it in `.env` file

6. Run the backend:
```bash
python app.py
```

Backend will start on `http://localhost:5000`

### Frontend Setup

1. Open a new terminal and navigate to frontend:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

Frontend will start on `http://localhost:5173`

## Usage 🚀

1. Open your browser and go to `http://localhost:5173`
2. Either:
   - **Upload a code file** using the file picker, or
   - **Paste your code** directly into the text area
3. Set the filename and programming language
4. Click **"Review Code"**
5. Wait 5-10 seconds for AI analysis
6. View comprehensive results including:
   - Overall quality score
   - Detailed metrics breakdown
   - Identified bugs and security issues
   - Concrete improvement suggestions with code examples

## API Endpoints 📡

### Health Check
```
GET /api/health
Response: {"status": "healthy", "timestamp": "..."}
```

### Submit Code Review
```
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
```

### Get All Reviews
```
GET /api/reviews
Response: {
  "success": true,
  "count": number,
  "reviews": [...]
}
```

### Get Specific Review
```
GET /api/reviews/:id
Response: {
  "success": true,
  "review": {...}
}
```

### Delete Review
```
DELETE /api/reviews/:id
Response: {
  "success": true,
  "message": "Review deleted"
}
```

## Project Structure 📁

```
code-review-assistant/
├── backend/
│   ├── venv/              # Virtual environment
│   ├── app.py             # Flask application
│   ├── .env               # Environment variables
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main React component
│   │   ├── App.css        # Styles
│   │   └── main.jsx       # Entry point
│   ├── package.json       # Node dependencies
│   └── vite.config.js     # Vite configuration
└── README.md
```

## Screenshots 📸

(Add screenshots of your application here)

## Demo Video 🎥

(Add link to your demo video here)

## Configuration ⚙️

### Backend Configuration (.env)
- `GEMINI_API_KEY`: Your Google Gemini API key
- `FLASK_ENV`: development or production
- `PORT`: Backend port (default: 5000)

### Frontend Configuration
- API URL is set in `src/App.jsx`: `const API_URL = 'http://localhost:5000/api'`
- For production, update this to your deployed backend URL

## Limitations ⚠️

- **Gemini Free Tier Limits**:
  - 15 requests per minute
  - 1,500 requests per day
  - 1 million tokens per day
- Reviews are stored in memory and will be lost on server restart
- For production use, implement a database for persistent storage

## Future Enhancements 🚀

- [ ] Database integration for persistent storage
- [ ] User authentication and multi-user support
- [ ] GitHub integration for direct PR reviews
- [ ] Support for more programming languages
- [ ] Export reports as PDF
- [ ] Real-time collaborative code review
- [ ] CI/CD pipeline integration
- [ ] Code diff comparison
- [ ] Custom review rules and templates

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License.

## Acknowledgments 🙏

- Google Gemini AI for powerful code analysis
- React and Vite communities
- Flask framework
- Lucide for beautiful icons

## Contact 📧

For questions or support, please open an issue in the GitHub repository.

---

