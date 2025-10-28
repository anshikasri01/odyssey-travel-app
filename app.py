from flask import Flask, render_template, jsonify, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask_cors import CORS

# --- 1. APP AND DATABASE CONFIGURATION ---
app = Flask(__name__)
CORS(app) 

# Configuration for Database (PostgreSQL/SQLite)
database_url = os.environ.get('DATABASE_URL') or 'sqlite:///feedback.db'

# SQLAlchemy compatibility fix for PostgreSQL URL
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.secret_key = os.environ.get('SECRET_KEY', 'a_strong_fallback_key_for_local_dev_only')

db = SQLAlchemy(app)

# --- 2. DATABASE MODEL ---
# The email column is nullable=True to allow submission without an email.
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Feedback('{self.rating}', '{self.name}', '{self.date_posted}')"

# --- 3. API ENDPOINT FOR TOUR DATA (Home Page) ---
@app.route('/api/tours', methods=['GET'])
def get_tours_data():
    """Returns a list of tour destinations for dynamic loading."""
    
    # NOTE: In a real Flask app, url_for is used to generate the correct paths.
    # We use placeholders here for clarity.
    tours_data = [
        {"name": "Jaipur", "image_url": url_for('static', filename='jaipur.jpg')}, 
        {"name": "Agra", "image_url": url_for('static', filename='agra.jpg')},
        {"name": "Nepal", "image_url": url_for('static', filename='nepal.jpg')},
        {"name": "Khajuraho", "image_url": url_for('static', filename='khajuraho.jpg')},
        {"name": "Bhubaneswar", "image_url": url_for('static', filename='bhubaneswar.jpg')},
        {"name": "Rishikesh", "image_url": url_for('static', filename='rishikesh.jpg')}
    ]
    return jsonify(tours_data)

# --- 4. API ENDPOINT FOR FEEDBACK SUBMISSION (FIXED FOR NULL EMAIL HANDLING) ---
@app.route('/api/submit_feedback', methods=['POST'])
def submit_feedback():
    if not request.is_json:
        return jsonify({"success": False, "message": "Request must be JSON"}), 400
    data = request.get_json()
    rating = data.get('rating')
    comments = data.get('comments')
    
    # 🚨 FIX: Sanitize the email field for database NULL acceptance 🚨
    submitted_email = data.get('email')
    # If email is missing or an empty string, set it to None (which is NULL in DB)
    if not submitted_email or submitted_email.strip() == "":
        submitted_email = None
    else:
        submitted_email = submitted_email.strip() # Clean up whitespace

    
    if not rating or not comments or not isinstance(rating, int) or not (1 <= rating <= 5):
        return jsonify({"success": False, "message": "Rating (1-5) and comments are required."}), 400

    try:
        feedback = Feedback(
            name=data.get('name', 'Anonymous'),
            email=submitted_email, # Use the sanitized variable
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
        # Log the detailed error for debugging on the server side
        print(f"Database error during feedback submission: {e}") 
        return jsonify({"success": False, "message": "An internal error occurred while saving feedback. Please try again."}), 500


# --- 5. PAGE ROUTES ---
@app.route('/')
def index():
    return redirect(url_for('home_page')) 

# All routes now render their respective HTML templates
@app.route('/home.html')
def home_page():
    return render_template('home.html')

@app.route('/discover.html')
def discover_page():
    return render_template('discover.html') 

@app.route('/places.html')
def places_page():
    return render_template('places.html') 

@app.route('/about.html')
def about_page():
    return render_template('about.html') 

@app.route('/login.html')
def login_page():
    return render_template('login.html') 

# --- 6. RUN THE APP ---
if __name__ == '__main__':
    # Initialize the database within the application context if running locally
    with app.app_context():
        # This will create tables if they don't exist
        db.create_all() 
        print("Database checked/created successfully.")

    from waitress import serve
    # Use 0.0.0.0 for serving in environments like Render
    serve(app, host='0.0.0.0', port=os.environ.get('PORT', 5000))
