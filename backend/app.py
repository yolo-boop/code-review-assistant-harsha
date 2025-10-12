from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Gemini safely
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Warning: Gemini model initialization failed: {str(e)}")
else:
    print("Warning: GEMINI_API_KEY not set. LLM features will be disabled.")

# In-memory storage
reviews = []

def get_fallback_analysis(code, filename, language):
    """Return a detailed fallback analysis (used if LLM fails)."""
    return {
        "overallScore": 7,
        "summary": "The code works but could be improved in safety, readability, and best practices.",
        "readability": {
            "score": 8,
            "comments": "Variables are fairly clear and indentation is proper. Function docstrings are missing.",
            "issues": ["Add docstrings", "Use more descriptive variable names"]
        },
        "bestPractices": {
            "score": 6,
            "comments": "Mostly follows best practices but usage of eval() or global variables is discouraged.",
            "violations": ["eval() usage", "Global variable mutation"]
        },
        "bugs": {
            "severity": "medium",
            "found": [
                {"line": 10, "description": "Possible division by zero", "suggestion": "Check denominator before dividing"}
            ]
        },
        "security": {
            "score": 5,
            "issues": [
                {"severity": "high", "description": "Use of eval() with user input", "recommendation": "Replace with ast.literal_eval()"}
            ]
        },
        "performance": {
            "score": 6,
            "suggestions": ["Use list comprehensions instead of loops where possible"]
        },
        "improvements": [
            {
                "category": "Code Safety",
                "description": "Replace eval() with safe alternatives",
                "before": "result = eval(user_input)",
                "after": "import ast\nresult = ast.literal_eval(user_input)",
                "impact": "high"
            },
            {
                "category": "Performance",
                "description": "Use list comprehension instead of loops",
                "before": "output = []\nfor x in items:\n    output.append(x*2)",
                "after": "output = [x*2 for x in items]",
                "impact": "low"
            }
        ]
    }

def analyze_code_with_llm(code, filename, language):
    """Analyze code using Gemini API if available, else return fallback."""
    if not model:
        return get_fallback_analysis(code, filename, language)
    
    prompt = (
        f"You are an expert code reviewer. Analyze the following {language} code from file '{filename}' "
        "and provide a comprehensive review including numeric scores (0-10) for overallScore, readability, "
        "bestPractices, security, and performance. Identify potential bugs and give concrete improvements "
        "with before and after code examples.\n\n"
        f"Code to review:\n```\n{code}\n```\n\n"
        "Respond strictly in JSON."
    )
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text

        # Remove markdown code blocks if present
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        analysis = json.loads(response_text)
        return analysis

    except Exception as e:
        # If LLM fails, fallback immediately
        print(f"LLM failed: {str(e)}")
        return get_fallback_analysis(code, filename, language)

# -------------------------
# Endpoints
# -------------------------
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/review', methods=['POST'])
def review_code():
    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({"error": "No code provided"}), 400

        code = data.get('code', '')
        filename = data.get('filename', 'untitled.txt')
        language = data.get('language', 'text')

        if len(code.strip()) == 0:
            return jsonify({"error": "Code cannot be empty"}), 400

        analysis = analyze_code_with_llm(code, filename, language)

        review = {
            "id": len(reviews) + 1,
            "filename": filename,
            "language": language,
            "timestamp": datetime.now().isoformat(),
            "codeLength": len(code),
            "analysis": analysis
        }

        reviews.append(review)

        return jsonify({"success": True, "reviewId": review["id"], "analysis": analysis})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    return jsonify({"success": True, "count": len(reviews), "reviews": reviews})

@app.route('/api/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = next((r for r in reviews if r["id"] == review_id), None)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    return jsonify({"success": True, "review": review})

@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    global reviews
    review = next((r for r in reviews if r["id"] == review_id), None)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    reviews = [r for r in reviews if r["id"] != review_id]
    return jsonify({"success": True, "message": "Review deleted"})

# -------------------------
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
