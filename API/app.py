import uvicorn
from fastapi import FastAPI
import pandas as pd
import mlflow
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from enum  import Enum


# Load environment variables from .env
load_dotenv()
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

description = """
    This API is used to support the features_df Science team's pricing optimization efforts,
    we have defined a RESTful API with a /predict endpoint.
    This endpoint is accessible via POST method at the following URL: 
    http://localhost:8000/predict and is designed to return optimized price predictions for car owners based on the input features_df.

    The inpud should be provided in the following format:
    {
        "model_key": "Citroën",
        "mileage": 150411,
        "engine_power": 90,
        "fuel": "petrol",
        "paint_color": "grey",
        "car_type": "convertible",
        "private_parking_available": true,
        "has_gps": false,
        "has_air_conditioning": true,
        "automatic_car": true,
        "has_getaround_connect": true,
        "has_speed_regulator": true,
        "winter_tires": true
    }

    And for simplicity, we assume all requests are well-formed and valid.
    Error handling is not included at this stage but may be added as an enhancement in future iterations.
    """
# ---------------- Enums ----------------
class ModelKey(str, Enum):
    citroën = "Citroën"
    peugeot = "Peugeot"
    pgo = "PGO"
    renault = "Renault"
    audi = "Audi"
    bmw = "BMW"
    ford = "Ford"
    mercedes = "Mercedes"
    opel = "Opel"
    porsche = "Porsche"
    volkswagen = "Volkswagen"
    kia_motors = "KIA Motors"
    alfa_romeo = "Alfa Romeo"
    ferrari = "Ferrari"
    fiat = "Fiat"
    lamborghini = "Lamborghini"
    maserati = "Maserati"
    lexus = "Lexus"
    honda = "Honda"
    mazda = "Mazda"
    mini = "Mini"
    mitsubishi = "Mitsubishi"
    nissan = "Nissan"
    seat = "SEAT"
    subaru = "Subaru"
    suzuki = "Suzuki"
    toyota = "Toyota"
    yamaha = "Yamaha"

class FuelType(str, Enum):
    diesel = "diesel"
    petrol = "petrol"
    hybrid_petrol = "hybrid_petrol"
    electro = "electro"
class PaintColor(str, Enum):
    black = "black"
    grey = "grey"
    white = "white"
    red = "red"
    silver = "silver"
    blue = "blue"
    orange = "orange"
    beige = "beige"
    brown = "brown"
    green = "green"
class CarType(str, Enum):
    convertible = "convertible"
    coupe = "coupe"
    estate = "estate"
    hatchback = "hatchback"
    sedan = "sedan"
    subcompact = "subcompact"
    suv = "suv"
    van = "van"

# ---------------- Input features for the prediction ----------------
class PredictionFeatures(BaseModel):
    model_key: ModelKey
    mileage: int
    engine_power: int
    fuel: FuelType
    paint_color: PaintColor
    car_type: CarType
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool

# ---------------- FastAPI app ----------------
app = FastAPI(
    title = "Car Price Prediction API",
    description = description,
    version = "1.0.0",
    contact = {
        "name": "Andriana's Team",
    }
)

"""
    Endpoint for making predictions /predict
"""
# ---------------- Root endpoint ----------------
@app.get("/") 
async def root():
    return {"message": "Welcome to the Car Price Prediction API"}

# ---------------- Prediction endpoint ----------------
@app.post("/predict", tags=["Prediction"])
async def predict(features: PredictionFeatures):
    """
        Predict the price of a car based on the provided features.
    """
    try:
        # Prepare the input data for prediction
        # input_data = pd.DataFrame([features.dict()])
        input_data = pd.DataFrame([features.model_dump()])
        print("Input data:", input_data)

        # Load the model
        # logged_model = 'runs:/a1388f05f64c4da0b491f886cdab93b1/model'
        logged_model = 'runs:/4943284e50ec4d0c986a1379bb48023a/model'
        print("Loading model from: ", logged_model)

        # Load model as a PyFuncModel.
        loaded_model = mlflow.pyfunc.load_model(logged_model)
        print("Model loaded successfully")

        # Make prediction
        prediction = loaded_model.predict(pd.DataFrame(input_data))
        print("Prediction result:", prediction)

        # Return prediction
        return {"predicted_price": float(prediction[0])}

    except Exception as e:
        print("Error during prediction:", e)
        return {"error": str(e)}

# ---------------- Error handling ----------------
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Request
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"Validation error on request: {await request.body()}")
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "error": "Validation Error",
            "details": exc.errors(),
            "body": exc.body,
        }),
    )