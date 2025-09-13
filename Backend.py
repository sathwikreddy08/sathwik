from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os

app = Flask(_name_)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- In-memory “database” for demonstration ---
user_profile = {"name": "Alex Learner", "email": "alex@learn.ai"}
progress = {
    "study_time": "2h 35m/week",
    "quiz_score": "82%",
    "topic_mastery": {"Algebra": "70%", "Biology": "90%"},
    "learning_trends": "Improving!"
}
materials = [
    {"material": "Intro to ML PDF", "time": "40min", "cost": "Free", "skill_level": "Beginner"},
    {"material": "JS Course PPT", "time": "1h", "cost": "$20", "skill_level": "Intermediate"}
]
recommendations = [
    "Practice algebra for 15min to boost mastery.",
    "Review flashcards before next quiz attempt.",
    "Schedule biology revision for Monday.",
    "Try interactive coding exercises for deeper JS practice."
]

if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)

# --- Endpoints ---

@app.route('/api/progress', methods=['GET'])
def get_progress():
    return jsonify(progress)

@app.route('/api/materials', methods=['GET'])
def get_materials():
    return jsonify(materials)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # Simulated extraction
    extracted = {
        "key_concepts": ["Adaptive Algorithms", "Performance Analytics", "Automated Assessments"],
        "study_notes": [
            "AI customizes learning paths to student needs",
            "Progress tracked by quizzes and topic mastery"
        ],
        "flashcards": [
            {"q": "What does an adaptive platform do?", "a": "Personalizes study content and difficulty."}
        ]
    }
    return jsonify({"filename": filename, "extracted": extracted})

@app.route('/api/assess', methods=['POST'])
def submit_assessment():
    data = request.json
    # Example: Validate the quiz response
    response = {}
    if data.get('q1') == True:
        response['q1'] = "Correct! Well done."
    else:
        response['q1'] = "Try again!"

    if data.get('q3'):
        response['q3'] = "Great! Personalized study increases retention."
    return jsonify(response)

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    return jsonify(recommendations)

@app.route('/api/profile', methods=['GET', 'POST'])
def handle_profile():
    if request.method == 'POST':
        body = request.json
        user_profile['name'] = body.get('name', user_profile['name'])
        user_profile['email'] = body.get('email', user_profile['email'])
        return jsonify({"status": "Profile updated!", "profile": user_profile})
    return jsonify(user_profile)

@app.route('/api/report/export', methods=['GET'])
def export_report():
    # For demonstration, just returning a text file
    filepath = "./progress_report.txt"
    with open(filepath, "w") as f:
        f.write("Progress Report\n")
        for k, v in progress.items():
            f.write(f"{k}: {v}\n")
    return send_file(filepath, as_attachment=True)

if _name_ == '_main_':
    app.run(debug=True)
