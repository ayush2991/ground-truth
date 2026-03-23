# Ground Truth

A full-stack web application designed for fact-checking and extracting "ground truth" information using Natural Language Inference (NLI) and machine learning models.

## Project Structure

This repository is structured as a monorepo containing:

- **`backend/`**: A Python-based FastAPI server. It handles the core logic, including ML model pipelines (Extractor, NLI) and interfaces with external services like the Brave Search API.
- **`frontend/`**: A modern Next.js (React) front-end web application, styled with Tailwind CSS.
- **`railway.json`**: Configuration file for deploying the application on [Railway](https://railway.app/).

## Prerequisites

- Node.js (v18+ recommended)
- npm or yarn
- Python 3.8+
- [Brave Search API Key](https://brave.com/search/api/)

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Set up a Python virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your environment variables:
   ```bash
   cp .env.example .env
   ```
   Open the newly created `.env` file and add your `BRAVE_API_KEY` and any other required configurations.
5. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The backend API will start running at `http://localhost:8000`.

### Frontend Setup

1. Open a new terminal window and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the frontend dependencies:
   ```bash
   npm install
   ```
3. Start the Next.js development server:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:3000](http://localhost:3000) in your web browser to interact with the application.

## Testing

The backend includes tests written with `pytest`. To run the tests, navigate to the `backend` directory and execute:

```bash
cd backend
python -m pytest
```

## Deployment

This application is configured for deployment using Docker. The `backend/Dockerfile` and the root `railway.json` files provide out-of-the-box configuration for deploying the services seamlessly to platforms like Railway.
