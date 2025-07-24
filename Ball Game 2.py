from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scores.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Score model
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)

# Create the table
with app.app_context():
    db.create_all()

# Submit score (POST)
@app.route('/score', methods=['POST'])
def submit_score():
    data = request.get_json()
    name = data.get('name')
    score_value = data.get('score')

    if not name or score_value is None:
        return jsonify({"error": "Missing name or score"}), 400

    new_score = Score(name=name, score=score_value)
    db.session.add(new_score)
    db.session.commit()
    return jsonify({"message": "Score submitted successfully"}), 201

# Get all scores (GET)
@app.route('/scores', methods=['GET'])
def get_scores():
    scores = Score.query.all()
    result = [{"name": s.name, "score": s.score} for s in scores]
    return jsonify(result)

# Get highest score (GET)
@app.route('/highscore', methods=['GET'])
def get_highscore():
    high = Score.query.order_by(Score.score.desc()).first()
    if high:
        return jsonify({"name": high.name, "score": high.score})
    else:
        return jsonify({"message": "No scores found."})

if __name__ == '__main__':
    app.run(debug=True)
