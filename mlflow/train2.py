# Import useful libraries
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

import os
import time
from dotenv import load_dotenv
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature

import pandas as pd
import numpy as np

# Load .env file
load_dotenv()
print("MLFLOW_TRACKING_URI =", os.getenv("MLFLOW_TRACKING_URI"))

# Set tracking URI to our Hugging Face application
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

# Mlfow experiment setup
experiment_name = "get_around_price_prediction_2"
mlflow.set_experiment(experiment_name)

# Load data
data = pd.read_csv("get_around_pricing_project.csv", index_col=0)

# Define feature groups
cat_features = ['model_key', 'fuel', 'paint_color', 'car_type']
num_features = ['mileage', 'engine_power']
bool_features = [
    'private_parking_available', 'has_gps', 'has_air_conditioning',
    'automatic_car', 'has_getaround_connect', 'has_speed_regulator', 'winter_tires'
]

# Prepare featueres and label
X = data[cat_features + num_features + bool_features]
y = data['rental_price_per_day']

# Preprocessing pipeline
preprocessor = ColumnTransformer(transformers=[
    ('cat', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1), cat_features),
    ('num', StandardScaler(), num_features),
    ('bool', 'passthrough', bool_features)
])

# Complete pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

with mlflow.start_run():

    print("training model ...")
    start_time = time.time()

    # Train pipeline
    pipeline.fit(X_train, y_train)

    # Predict and evaluate
    y_pred = pipeline.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    # Log metrics and parameters
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("execution_time", time.time() - start_time)
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("random_state", 42)

    # Log raw data as artifact
    mlflow.log_artifact("get_around_pricing_project.csv")

    # Log model with pipeline and signature
    signature = infer_signature(X_train, y_train)
    mlflow.sklearn.log_model(
        sk_model=pipeline,
        artifact_path="model",
        registered_model_name="get_around_price_prediction_2",
        signature=signature
    )

    mlflow.end_run()