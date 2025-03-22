from flask import Flask, jsonify, request, send_from_directory
from db.repository import Repository
from pipeline import run_pipeline
from ml_model.linear import train_linear_model, predict

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('src/ui', 'index.html')

@app.route('/train-model', methods=['POST'])
def train_model():
    try:
        train_linear_model()
        return jsonify({"message": "Modèle entraîné avec succès."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict_route():
    try:
        features = request.get_json()
        prediction = predict(features)
        return jsonify({"prediction": prediction}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/matrix', methods=['GET'])
def get_matrix():
    repo = Repository()
    data = repo.fetch_all("matrix_cost_of_life")
    repo.close()

    if not data:
        return jsonify({"error": "No data found"}), 404

    columns = ["country", "meal_inexpensive", "mcmeal", "gasoline", "internet", "crime_index"]
    result = [dict(zip(columns, row)) for row in data]

    return jsonify(result)

@app.route('/run-pipeline', methods=['POST'])
def trigger_pipeline():
    """ API Endpoint to manually trigger the data pipeline """
    try:
        run_pipeline()
        return jsonify({"message": "Pipeline executed successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
