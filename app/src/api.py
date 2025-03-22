import os
from flask import Flask, jsonify, request, send_from_directory, Response
from db.repository import Repository
import pandas as pd
from pipeline import run_pipeline
from ml_model.linear import train_linear_model, predict

app = Flask(__name__)

@app.route('/')
def index():
    full_path = os.path.join(app.root_path, 'ui')
    return send_from_directory(full_path, 'index.html')

@app.route('/train-model', methods=['POST'])
def train_model():
    try:
        train_linear_model()
        return jsonify({"message": "Modèle entraîné avec succès."}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/predict', methods=['POST'])
def predict_route():
    try:
        features = request.get_json()
        prediction = predict(features)
        return jsonify({"prediction": prediction}), 200
    except FileNotFoundError as fnfe:
        return jsonify({"error": str(fnfe)}), 400
    except ValueError as ve:
        return jsonify({"error": f"Données invalides : {ve}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erreur interne : {e}"}), 500


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

@app.route('/matrix/csv', methods=['GET'])
def download_matrix_csv():
    repo = Repository()
    data = repo.fetch_all("matrix_cost_of_life")
    repo.close()

    if not data:
        return jsonify({"error": "Aucune donnée trouvée dans matrix_cost_of_life"}), 404

    # Colonnes attendues (peut être raccourci si besoin)
    columns = [
        "country", "meal_inexpensive", "meal_for_two", "mcmeal", "domestic_beer",
        "imported_beer", "cappuccino", "coke_pepsi", "water_small", "milk", "bread",
        "rice", "eggs", "cheese", "chicken", "beef", "apples", "banana", "oranges",
        "tomato", "potato", "onion", "lettuce", "water_large", "non_alcoholic_wine",
        "cigarettes", "local_transport_ticket", "monthly_pass", "taxi_start",
        "taxi_per_km", "taxi_waiting", "gasoline", "volkswagen_golf", "toyota_corolla",
        "utilities", "mobile_plan", "internet", "fitness_club", "tennis_court",
        "cinema", "preschool", "primary_school", "jeans", "summer_dress", "nike_shoes",
        "leather_shoes", "apt_1bed_city", "apt_1bed_out", "apt_3bed_city",
        "apt_3bed_out", "price_sq_m_city", "price_sq_m_out", "net_salary",
        "crime_index"
    ]

    df = pd.DataFrame(data, columns=columns)

    # Conversion en CSV en mémoire
    csv_data = df.to_csv(index=False)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=matrix_cost_of_life.csv"}
    )


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
