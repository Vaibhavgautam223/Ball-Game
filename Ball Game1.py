from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory score storage
scores = []

# Submit new score
@app.route('/score', methods=['POST'])
def submit_score():
    data = request.get_json()
    name = data.get('name')
    score = data.get('score')

    if not name or score is None:
        return jsonify({"error": "Missing name or score"}), 400

    scores.append({'name': name, 'score': score})
    return jsonify({"message": "Score submitted successfully"}), 201

# Get all scores
@app.route('/scores', methods=['GET'])
def get_scores():
    return jsonify(scores)

# Get high score
@app.route('/highscore', methods=['GET'])
def get_highscore():
    if not scores:
        return jsonify({"highscore": None})
    high = max(scores, key=lambda x: x['score'])
    return jsonify(high)

if __name__ == '__main__':
    app.run(debug=True)
