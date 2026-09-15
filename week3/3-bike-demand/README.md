# Bike Demand AI Assistant

This application predicts hourly bike-rental demand and uses a local Ollama language model to provide a short operational recommendation.

## Components

- `app.py`: Streamlit webpage where the user enters conditions and sees results.
- `predict.py`: validates input and produces the bike-demand prediction.
- `llm_service.py`: sends the prediction to local Ollama and returns AI guidance. If Ollama is unavailable, it returns fallback guidance instead.

## Install Python packages

From the project folder, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Start the local LLM

In a separate Terminal window, start the Docker/Ollama environment used in the course tutorial:

```bash
cd ~/Documents/psgv-sweng889/week3/1-local-llm
docker compose up --build
```

Leave this Terminal running while using the application.

## Run the application

In the bike-demand project folder, run:

```bash
source .venv/bin/activate
streamlit run app.py
```

Open the local URL shown in Terminal, usually `http://localhost:8501`.

## LLM-enabled capability

The bike-demand model produces the rental prediction. The local LLM uses that prediction and the input conditions to generate a short recommendation for bike availability and operations. The LLM does not calculate the prediction itself.

## Validation

The application was tested in three situations:

- Valid input produced a bike-demand prediction and a local Ollama response.
- Invalid input was blocked with a clear message.
- When Ollama was unavailable, the bike-demand prediction still appeared with fallback guidance.

Run automated tests with:

```bash
pytest -q
```