# DSmith AI — Autonomous Data Science Agent

DSmith AI is an autonomous data science agent designed to automate the end-to-end machine learning workflow.

Instead of manually performing each stage of a data science project, DSmith AI uses an LLM-driven workflow to inspect the dataset, generate and execute data preparation code, train machine learning models, validate the results, and produce the final artifacts.

## 🚀 Live Demo

[**Try DSmith AI →**](https://autonomous-data-science-agent.onrender.com)

## 🚀 Key Capabilities

- Automated dataset inspection and profiling
- LLM-generated data cleaning and preprocessing
- Automatic validation of generated code
- Self-correction and retry workflow
- Automated machine learning model selection
- Classification and regression workflows
- Model training and evaluation
- Generated training code
- Trained model artifact generation
- Downloadable cleaned datasets and models
- Streamlit-based user interface
- FastAPI backend
- LangGraph-based workflow orchestration
- Docker-ready deployment

## 🧠 How DSmith AI Works

    User uploads dataset
            │
            ▼
    Dataset Inspection
            │
            ▼
    Problem Understanding
            │
            ▼
    Generate Data Cleaning Code
            │
            ▼
    Validate Generated Code
            │
            ├── Failed ──► LLM Repair ──► Validate Again
            │
            ▼
    Execute Data Preparation
            │
            ▼
    Generate ML Training Code
            │
            ▼
    Validate Training Workflow
            │
            ├── Failed ──► LLM Repair ──► Validate Again
            │
            ▼
    Train & Evaluate Models
            │
            ▼
    Generate Final Artifacts
            │
            ▼
    Results & Downloads

## 🏗️ Architecture

DSmith AI uses a layered architecture:

    ┌─────────────────────────────┐
    │       Streamlit UI          │
    │       app.py                │
    └──────────────┬──────────────┘
                   │ HTTP
                   ▼
    ┌─────────────────────────────┐
    │       FastAPI Backend       │
    │       main.py               │
    └──────────────┬──────────────┘
                   │
                   ▼
    ┌─────────────────────────────┐
    │       LangGraph             │
    │       Workflow              │
    └──────────────┬──────────────┘
                   │
           ┌───────┴────────┐
           ▼                ▼
    ┌─────────────┐  ┌─────────────┐
    │    Agents   │  │    Tools    │
    └─────────────┘  └─────────────┘
           │                │
           └───────┬────────┘
                   ▼
    ┌─────────────────────────────┐
    │ Pandas / Scikit-learn / ML  │
    └─────────────────────────────┘

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- FastAPI
- Uvicorn

### AI & Orchestration
- LangChain
- LangGraph
- Google Generative AI

### Data Science
- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib

### Deployment
- Docker
- Render

## 📁 Project Structure

    Autonomous-Data-Science-Agent/
    │
    ├── agent/
    │   └── AI agent components
    │
    ├── orchestration/
    │   └── LangGraph workflow
    │
    ├── schemas/
    │   └── Pydantic/data schemas
    │
    ├── tools/
    │   └── Data processing and ML tools
    │
    ├── tests/
    │   └── Project tests
    │
    ├── uploads/
    │   └── Runtime uploaded datasets
    │
    ├── workspace/
    │   └── Runtime-generated artifacts
    │
    ├── app.py
    │   └── Streamlit frontend
    │
    ├── main.py
    │   └── FastAPI backend
    │
    ├── requirements.txt
    │   └── Python dependencies
    │
    ├── Dockerfile
    │   └── Container configuration
    │
    ├── start.sh
    │   └── Starts FastAPI and Streamlit
    │
    ├── .env.example
    │   └── Environment variable template
    │
    ├── .gitignore
    ├── .dockerignore
    └── README.md

## ⚙️ Local Setup

### 1. Clone the repository

    git clone https://github.com/manishk385/Autonomous-Data-Science-Agent.git
    cd Autonomous-Data-Science-Agent

### 2. Create a virtual environment

    python -m venv venv

Activate it on Windows PowerShell:

    .\venv\Scripts\Activate.ps1

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Add the required API credentials:

    GOOGLE_API_KEY=your_api_key

Never commit `.env` or API keys to GitHub.

### 5. Start the FastAPI backend

    uvicorn main:app --reload

The backend will run on:

    http://127.0.0.1:8000

### 6. Start the Streamlit frontend

In another terminal:

    streamlit run app.py

The frontend will run on:

    http://localhost:8501

## 🐳 Docker

Build the Docker image:

    docker build -t dsmith-ai .

Run the container:

    docker run -p 8501:8501 --env-file .env dsmith-ai

The Streamlit application will be available at:

    http://localhost:8501

## 🔄 Autonomous Workflow

The core workflow is orchestrated using LangGraph.

The system maintains workflow state while moving through different stages such as:

1. Dataset inspection
2. Problem understanding
3. Cleaning code generation
4. Code validation
5. Cleaning code execution
6. Preprocessing
7. Model/training code generation
8. Training validation
9. Model training
10. Result verification
11. Artifact generation

When generated code fails validation, the workflow can return to the LLM for correction before continuing.

## 📦 Generated Artifacts

The system can generate artifacts such as:

- Cleaned datasets
- Trained machine learning models
- Training code
- Evaluation metrics
- Analysis results

Runtime artifacts are stored locally in the workspace and are excluded from version control.

## 🔐 Security

Sensitive information such as API keys should be stored in environment variables.

The following files and directories are intentionally excluded from Git:

    .env
    venv/
    uploads/
    workspace/
    *.joblib

## 🚧 Current Status

**Version 1**

The current version provides the core autonomous data science workflow, including dataset inspection, automated data preparation, model training, validation, and artifact generation.

## 🔮 Future Improvements

- More machine learning algorithms
- Advanced feature engineering
- Hyperparameter optimization
- Explainable AI
- Experiment tracking
- Persistent artifact storage
- Authentication and user management
- Improved autonomous error recovery
- Production-scale deployment
- Automated model monitoring

## 👨‍💻 Author

Manish Kumar K

B.Tech — Civil Engineering  
National Institute of Technology, Tiruchirappalli

GitHub: https://github.com/manishk385
