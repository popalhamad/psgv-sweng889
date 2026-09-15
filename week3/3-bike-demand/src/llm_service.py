"""Local LLM guidance for the bike-demand app."""

from __future__ import annotations

import json
from typing import Any, Dict, Tuple

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3.2:latest"


def _fallback_guidance(prediction: float, inputs: Dict[str, Any]) -> str:
    """Return a rule-based explanation when the local LLM is unavailable."""
    season = inputs["season"]
    hour = inputs["hour"]
    if prediction >= 700:
        demand_text = "very high"
    elif prediction >= 450:
        demand_text = "moderately high"
    elif prediction >= 250:
        demand_text = "steady"
    else:
        demand_text = "low"

    if inputs["is_holiday"]:
        holiday_note = "The holiday setting may shift rider patterns and reduce commuter trips."
    elif inputs["is_working_day"]:
        holiday_note = "A working day usually supports commuting demand and stronger midday or evening activity."
    else:
        holiday_note = "Weekend traffic is likely to be more leisure-driven and less predictable."

    if 6 <= hour <= 9 or 17 <= hour <= 19:
        time_note = "This is a peak travel period, so station availability should be monitored closely."
    elif 0 <= hour <= 5:
        time_note = "Night demand is typically low, so fewer bikes may be needed."
    else:
        time_note = "Demand should be manageable during this time of day, though conditions may still shift."

    return (
        f"Demand is expected to be {demand_text} in {season}. "
        f"{holiday_note} {time_note} "
        "Consider checking high-traffic stations and preparing additional support if demand rises."
    )


def generate_guidance(
    prediction: float,
    inputs: Dict[str, Any],
    model: str = DEFAULT_MODEL,
    llm_url: str = OLLAMA_URL,
    return_status: bool = False,
) -> str | Tuple[str, bool]:
    """Ask the local Ollama model for operational guidance. Falls back if the model is unavailable."""
    prompt = (
        "You are a bike-share operations assistant. "
        f"The predicted hourly bike demand is {prediction:.0f} rentals. "
        f"Context: season={inputs['season']}, hour={inputs['hour']}, "
        f"temperature_c={inputs['temperature_c']}, "
        f"humidity_pct={inputs['humidity_pct']}, "
        f"is_holiday={int(inputs['is_holiday'])}, "
        f"is_working_day={int(inputs['is_working_day'])}. "
        "Give a short operational recommendation in plain English, no jargon, and keep it under 120 words."
    )

    try:
        response = requests.post(
            llm_url,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        llm_text = str(payload.get("response", "")).strip()
        if llm_text:
            if return_status:
                return llm_text, True
            return llm_text
    except Exception:
        pass

    fallback_text = _fallback_guidance(prediction, inputs)
    if return_status:
        return fallback_text, False
    return fallback_text
