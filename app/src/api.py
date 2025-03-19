from flask import Flask, jsonify
from db.repository import Repository
from pipeline import run_pipeline

app = Flask(__name__)

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
