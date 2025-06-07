# 🚗 Car Price Prediction - MLOps Project

A complete car price prediction project with a modern MLOps architecture deployed on Hugging Face Spaces.

## 🎯 Project Overview

This project implements an end-to-end solution for predicting car prices using MLOps best practices. It includes a REST API, an MLflow tracking server, and a Streamlit user interface.

## 🏗️ Architecture

The project consists of three interconnected Hugging Face spaces:

### 1. 🔗 REST API (FastAPI)
**URL:** https://andrianiniaina-api-space-1f33d3f.hf.space/docs

- RESTful API for car price predictions
- Interactive documentation with Swagger UI
- Endpoints for training and inference
- Input data validation

### 2. 📊 MLflow Server
**URL:** https://andrianiniaina-mlflow-server.hf.space

- Experiment tracking and metrics
- Model and version management
- Performance comparison
- Centralized model registry

### 3. 🖥️ Streamlit Interface
**URL:** https://andrianiniaina-streamlit.hf.space

- Interface Intuitive user experience
- Real-time predictions
- Interactive visualizations
- Feature entry form

## ✨ Features

- **Machine Learning**: Powerful price prediction models
- **Tracking**: Complete experiment tracking with MLflow
- **API**: REST service for external integrations
- **Interface**: User-friendly web application
- **Cloud**: Deployment on Hugging Face Spaces
- **MLOps**: Complete development-to-production pipeline

## 🛠️ Technologies Used

- **Machine Learning**: scikit-learn, pandas, numpy
- **API**: FastAPI, uvicorn
- **Frontend**: Streamlit
- **MLOps**: MLflow
- **Deployment**: Hugging Face Spaces
- **Documentation**: Swagger/OpenAPI

## 🚀 Usage

### Via the Web Interface
1. Go to https://andrianiniaina-streamlit.hf.space
2. Fill in the car's specifications
3. Get the price prediction instantly

### Via the API
1. Consult the documentation: https://andrianiniaina-api-space-1f33d3f.hf.space/docs
2. Test the endpoints directly in Swagger UI
3. Integrate the API into your applications

### Experiment Monitoring
1. Access MLflow: https://andrianiniaina-mlflow-server.hf.space
2. Explore metrics and models
3. Compare performance

## 🔧 Architecture Technical

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI      │    │    MLflow       │
│   Frontend      │◄──►│      API        │◄──►│    Server       │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  ML Models &    │
                    │  Predictions    │
                    └─────────────────┘
```

## 📈 Metrics and Performance

- **Accuracy**: Real-time monitoring via MLflow
- **API Latency**: < 100ms for predictions
- **Availability**: 24/7 on Hugging Face Spaces
- **Scalability**: Auto-scaling based on demand

## 🌟 Key Features

- ✅ **Complete Architecture**: From training to deployment
- ✅ **Intuitive Interface**: Accessible to non-technical users
- ✅ **Robust API**: For professional integrations
- ✅ **Monitoring**: Complete performance monitoring
- ✅ **Documentation**: Comprehensive and interactive
- ✅ **Cloud deployment**: High availability

## 🔄 MLOps workflow

1. **Development**: Model training and validation
2. **Tracking**: Recording experiments in MLflow
3. **Deployment**: REST API for predictions
4. **Interface**: Streamlit application for users
5. **Monitoring**: Performance tracking in production

## 🎯 Use cases

- **Car dealerships**: Rapid price estimation
- **Sales platforms**: Validation of advertised prices
- **Insurance**: Vehicle valuation
- **Private buyers**: Negotiation assistance

---

## 👤 Author

Project by **Andriana**

🔗 GitHub: [https://github.com/Andrianiniaina/0-Deployment]
