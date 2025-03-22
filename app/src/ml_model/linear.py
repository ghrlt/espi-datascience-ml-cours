import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib
from db.repository import Repository

MODEL_PATH = "app/src/ml_model/linear_model.joblib"

def train_linear_model(target_column="meal_inexpensive"):
    repo = Repository()
    data = repo.fetch_all("matrix_cost_of_life")
    repo.close()
    if not data:
        print("❌ Aucune donnée disponible pour l'entraînement.")
        return
    
    df = pd.DataFrame(data, columns=[
        "country", "meal_inexpensive", "meal_for_two", "mcmeal", "domestic_beer", 
        "imported_beer", "cappuccino", "coke_pepsi", "water_small", "milk", 
        "bread", "rice", "eggs", "cheese", "chicken", "beef", "apples", "banana", 
        "oranges", "tomato", "potato", "onion", "lettuce", "water_large", 
        "non_alcoholic_wine", "cigarettes", "local_transport_ticket", "monthly_pass", 
        "taxi_start", "taxi_per_km", "taxi_waiting", "gasoline", "volkswagen_golf", 
        "toyota_corolla", "utilities", "mobile_plan", "internet", "fitness_club", 
        "tennis_court", "cinema", "preschool", "primary_school", "jeans", 
        "summer_dress", "nike_shoes", "leather_shoes", "apt_1bed_city", 
        "apt_1bed_out", "apt_3bed_city", "apt_3bed_out", "price_sq_m_city", 
        "price_sq_m_out", "net_salary", "crime_index"
    ])
    
    df = df.drop(columns=["country"])
    df = df.dropna()
    
    X = df.drop(columns=[target_column])
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(f"🎯 R² score sur le test set: {r2_score(y_test, y_pred):.4f}")

    joblib.dump(model, MODEL_PATH)
    print(f"✅ Modèle sauvegardé dans {MODEL_PATH}")

def predict(input_features: dict):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("⚠️ Modèle non trouvé. Entraîne-le d'abord via /train-model.")
    model = joblib.load(MODEL_PATH)
    df = pd.DataFrame([input_features])
    return model.predict(df)[0]
