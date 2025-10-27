from flask import Flask, render_template, jsonify, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask_cors import CORS

# --- 1. APP AUR DATABASE CONFIGURATION ---
app = Flask(__name__)
CORS(app) # CORS enabled

# Deployment ke liye DATABASE_URL (Render se) use karein.
database_url = os.environ.get('DATABASE_URL') or 'sqlite:///feedback.db'

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# 🚨 CRITICAL FIX: SECRET_KEY ko Environment Variable se load karein
# Agar SECRET_KEY set nahi hai, toh app start nahi honi chahiye (Production best practice).
# Lekin development ke liye, hum ek dummy value rakh sakte hain.
# Aapke code mein iski zarurat nahi hai, kyunki aap sessions use nahi kar rahe, 
# lekin security ke liye isko set karna accha hai.
app.secret_key = os.environ.get('SECRET_KEY', 'a_strong_fallback_key_for_local_dev_only')

db = SQLAlchemy(app)

# --- 2. DATABASE MODEL ---
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    rating = db.Column(db.Integer, nullable=False) # 1 to 5
    comments = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Feedback('{self.rating}', '{self.name}', '{self.date_posted}')"


# --- 3. API ENDPOINT FOR TOUR DATA (Home Page) ---
@app.route('/api/tours', methods=['GET'])
def get_tours_data():
    """Returns a list of tour destinations for dynamic loading."""
    
    tours_data = [
        {"name": "Jaipur", "image_url": "https://i.pinimg.com/736x/f2/a7/6d/f2a76d7d1a7540c124de3f05f560e844.jpg"},
        {"name": "Agra", "image_url": "https://i.pinimg.com/736x/05/7e/c3/057ec30f1aaf14945ac0322502251341.jpg"},
        {"name": "Nepal", "image_url": "https://i.pinimg.com/1200x/02/1b/ff/021bff44798638c0e0ce78b5aea86c0f.jpg"},
        {"name": "Khajuraho", "image_url": "https://i.pinimg.com/originals/a0/78/34/a0783472013f9f592a95c93c4c92e92c.jpg"},
        {"name": "Bhubaneswar", "image_url": "https://i.pinimg.com/736x/89/13/f2/8913f225f20a9d4449c4bfbab5af6472.jpg"},
        {"name": "Rishikesh", "image_url": "https://i.pinimg.com/736x/cb/47/93/cb4793023e05da0a154955e7b91c6cf4.jpg"}
    ]
    return jsonify(tours_data)

# --- 4. API ENDPOINT FOR FEEDBACK SUBMISSION (Login Page) ---
@app.route('/api/submit_feedback', methods=['POST'])
def submit_feedback():
    """Receives feedback data and saves it to the database."""
    if not request.is_json:
        return jsonify({"success": False, "message": "Request must be JSON"}), 400

    data = request.get_json()
    
    rating = data.get('rating')
    comments = data.get('comments')
    
    # Validation check 
    if not rating or not comments or not isinstance(rating, int) or not (1 <= rating <= 5):
        return jsonify({"success": False, "message": "Rating (1-5) and comments are required."}), 400

    try:
        feedback = Feedback(
            name=data.get('name', 'Anonymous'),
            email=data.get('email'),
            rating=int(rating),
            comments=comments
        )
        db.session.add(feedback)
        db.session.commit()

        return jsonify({
            "success": True, 
            "message": "Thank you! Your feedback has been successfully submitted.",
            "feedback_id": feedback.id
        }), 201

    except Exception as e:
        db.session.rollback()
        # Error ko console mein print karein (Render logs mein dikhega)
        print(f"Database error: {e}") 
        return jsonify({"success": False, "message": "An error occurred while saving feedback."}), 500


# --- 5. PAGE ROUTES ---

# Default Route: Root domain se home page par redirect karega
@app.route('/')
def index():
    """Redirects the root URL to the home page."""
    return redirect(url_for('home_page')) 

# Main Route: Home Page
@app.route('/home.html')
def home_page():
    """Serves the home.html file from the 'templates' folder."""
    return render_template('home.html')

# Sub-Route: Discover Page
@app.route('/discover.html')
def discover_page():
    """Serves the discover.html file from the 'templates' folder."""
    return render_template('discover.html') 

# Sub-Route: Places Page
@app.route('/places.html')
def places_page():
    """Serves the places.html file from the 'templates' folder."""
    return render_template('places.html') 

# Sub-Route: About Page
@app.route('/about.html')
def about_page():
    """Serves the about.html file from the 'templates' folder."""
    return render_template('about.html') 

# Sub-Route: Login/Feedback Page
@app.route('/login.html')
def login_page():
    """Serves the login.html file from the 'templates' folder."""
    return render_template('login.html') 

# --- 6. RUN THE APP ---
# Production mein gunicorn/Procfile se run hoga. Local development ke liye Waitress.
if __name__ == '__main__':
    from waitress import serve
    # PORT environment variable use karein, ya 5000 par fallback karein (default)
    serve(app, host='0.0.0.0', port=os.environ.get('PORT', 5000))