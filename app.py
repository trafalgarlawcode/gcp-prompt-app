import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration using environment variables
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']
db_host = os.environ.get('DB_HOST', '127.0.0.1')
db_port = os.environ.get('DB_PORT', '3306')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model for prompts
class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)

# Create the table if it doesn't exist
with app.app_context():
    db.create_all()

@app.route('/prompt', methods=['POST'])
def prompt():
    data = request.get_json()
    message = data.get('message', '')
    # Save to database
    prompt_entry = Prompt(message=message)
    db.session.add(prompt_entry)
    db.session.commit()
    return jsonify({'reply': f'You said: {message}'})

@app.route('/')
def index():
    return "App is running!"

@app.route('/healthz')
def healthz():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
