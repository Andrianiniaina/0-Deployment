# Import useful libraries

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

import os
import time
from dotenv import load_dotenv
import mlflow
import mlflow.sklearn
from mlflow import log_metric, log_param, log_artifact

import pandas as pd
import numpy as np

# Load .env file
load_dotenv()
print("MLFLOW_TRACKING_URI =", os.getenv("MLFLOW_TRACKING_URI"))

# Set tracking URI to our Hugging Face application
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

# Mlfow experiment setup
experiment_name = "get_around_price_prediction"
mlflow.set_experiment(experiment_name)

with mlflow.start_run():

    print("training model ...")
    start_time = time.time()

    # Load data
    data = pd.read_csv("get_around_pricing_project.csv", index_col=0)

    # Encode categorical vartiables
    label_encoders = {}
    for column in ['model_key', 'fuel', 'paint_color', 'car_type']:
        label_encoders[column] = LabelEncoder()
        data[column] = label_encoders[column].fit_transform(data[column])

    # Prepare featueres and label
    X=data.drop(columns='rental_price_per_day')
    y=data['rental_price_per_day']

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Preidct and evaluate
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    # Log metrics
    log_metric("rmse", rmse)
    log_metric("execution_time", time.time() - start_time)

    # Log parameters
    log_param("n_estimators", 100)
    log_param("random_state", 42)
    log_param("scaler", "StandardScaler")
    log_param("label_encoders", ",".join(label_encoders.keys()))


    # Log artifacts
    log_artifact("get_around_pricing_project.csv")


    # Log model
    mlflow.sklearn.log_model(
        model, "model",
        registered_model_name="get_around_price_prediction",
        signature=mlflow.models.signature.infer_signature(X_train, y_train)
        )
    mlflow.autolog()
    mlflow.end_run()