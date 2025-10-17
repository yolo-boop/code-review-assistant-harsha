from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from datetime import datetime
import json
import traceback
import re

# Optional: import the Gemini SDK if available
try:
    import google.generativeai as genai
except Exception:
    genai = None

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Gemini (best-effort)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
model = None
if genai and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            print("✅ Gemini model object initialized (GenerativeModel)")
        except Exception:
            model = None
            print("⚠️  GenerativeModel initialization failed; genai SDK available.")
    except Exception as e:
        print(f"❌ genai.configure failed: {e}")
        model = None
elif genai and not GEMINI_API_KEY:
    print("⚠️  genai SDK available but GEMINI_API_KEY not set in environment")
else:
    print("⚠️  genai library not installed or failed to import; running in fallback mode")

reviews = []

def extract_json_from_text(text):
    if not text or not isinstance(text, str):
        return None, text
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    if not m:
        m = re.search(r"```\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    if m:
        candidate = m.group(1).strip()
        try:
            return json.loads(candidate), candidate
        except Exception:
            pass
    start = text.find("{")
    if start != -1:
        stack = []
        for i in range(start, len(text)):
            ch = text[i]
            if ch == "{":
                stack.append("{")
            elif ch == "}":
                if stack:
                    stack.pop()
                    if not stack:
                        candidate = text[start:i+1]
                        try:
                            return json.loads(candidate), candidate
                        except Exception:
                            break
    try:
        return json.loads(text), text
    except Exception:
        return None, text

def analyze_code_with_llm(code, filename, language):
    if not isinstance(code, str):
        raise ValueError("code must be a string")
    if not genai:
        return {
            "overallScore": 7,
            "summary": "Fallback: genai library not installed.",
            "readability": {"score": 7, "comments": "Code appears readable", "issues": []},
            "bestPractices": {"score": 6, "comments": "Generally follows good practices", "violations": []},
            "bugs": {"severity": "low", "found": []},
            "security": {"score": 7, "issues": []},
            "performance": {"score": 7, "suggestions": []},
            "improvements": []
        }
    prompt = f"""You are an expert code reviewer. Analyze this {language} code named '{filename}'.
Return ONLY valid JSON with this exact structure:
{{
  "overallScore": 0,
  "summary": "brief summary",
  "readability": {{"score": 0, "comments": "text", "issues": []}},
  "bestPractices": {{"score": 0, "comments": "text", "violations": []}},
  "bugs": {{"severity": "low", "found": []}},
  "security": {{"score": 0, "issues": []}},
  "performance": {{"score": 0, "suggestions": []}},
  "improvements": []
}}
Be concise. Return only JSON (no extra commentary)."""
    snippet = code
    MAX_SNIPPET_CHARS = 20000
    if len(snippet) > MAX_SNIPPET_CHARS:
        snippet = snippet[:8000] + "\n\n/*...snipped...*/\n\n" + snippet[-8000:]
    full_prompt = prompt + "\n\nCode:\n```" + language + "\n" + snippet + "\n```\n"
    try:
        response_text = None
        if model is not None and hasattr(model, "generate_content"):
            try:
                resp = model.generate_content(full_prompt)
                if hasattr(resp, "text") and isinstance(resp.text, str):
                    response_text = resp.text
                elif isinstance(resp, dict) and "output" in resp:
                    try:
                        response_text = json.dumps(resp)
                    except Exception:
                        response_text = str(resp)
                else:
                    response_text = str(resp)
            except Exception as e:
                print("⚠️ model.generate_content raised:", e)
        if response_text is None:
            if hasattr(genai, "generate"):
                try:
                    resp = genai.generate(model="gemini-1.5-flash", prompt=full_prompt)
                    if isinstance(resp, dict) and "output" in resp:
                        out = resp.get("output")
                        if isinstance(out, list):
                            response_text = " ".join([str(item.get("content", "")) if isinstance(item, dict) else str(item) for item in out])
                        else:
                            response_text = str(out)
                    else:
                        response_text = str(resp)
                except Exception as e:
                    print("⚠️ genai.generate failed:", e)
        if response_text is None and hasattr(genai, "chat"):
            try:
                resp = genai.chat.create(model="gemini-1.5-flash", messages=[{"role":"user","content":full_prompt}])
                if isinstance(resp, dict):
                    if "candidates" in resp and len(resp["candidates"]) > 0:
                        response_text = resp["candidates"][0].get("content", "")
                    elif "output" in resp:
                        response_text = str(resp["output"])
                    else:
                        response_text = str(resp)
                else:
                    response_text = str(resp)
            except Exception as e:
                print("⚠️ genai.chat.create failed:", e)
        if not response_text:
            raise RuntimeError("No text response received from genai SDK (tried multiple call patterns).")
        analysis_obj, raw_json = extract_json_from_text(response_text)
        if analysis_obj is None:
            try:
                analysis_obj = json.loads(response_text)
            except Exception as e:
                print("❌ Failed to parse JSON from LLM response. Response head:", response_text[:800])
                raise RuntimeError("Failed to parse JSON from LLM response: " + str(e))
        print("✅ AI analysis successful (parsed JSON)")
        return analysis_obj
    except Exception as e:
        print("❌ LLM analysis failed:", str(e))
        traceback.print_exc()
        return {
            "overallScore": 6,
            "summary": f"Fallback analysis: LLM failed ({str(e)[:200]})",
            "readability": {"score": 6, "comments": "Could not complete full analysis", "issues": []},
            "bestPractices": {"score": 6, "comments": "Could not complete full analysis", "violations": []},
            "bugs": {"severity": "low", "found": []},
            "security": {"score": 6, "issues": []},
            "performance": {"score": 6, "suggestions": []},
            "improvements": []
        }

@app.route('/')
def home():
    return "✅ Backend is running successfully! Use /api/health to check status."

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "genai_available": genai is not None,
        "gemini_model_object": model is not None
    })

@app.route('/api/review', methods=['POST'])
def review_code():
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict() or request.get_json(silent=True) or {}
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
        return jsonify({
            "success": True,
            "reviewId": review["id"],
            "analysis": analysis
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    return jsonify({
        "success": True,
        "count": len(reviews),
        "reviews": reviews
    })

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

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("\n" + "="*50)
    print("🚀 Starting Code Review Assistant Backend")
    print(f"📡 Server will run on: http://0.0.0.0:{port}")
    print(f"✅ genai library present: {genai is not None}")
    print(f"✅ Gemini model object present: {model is not None}")
    print("="*50 + "\n")
    app.run(debug=True, port=port, host='0.0.0.0')
