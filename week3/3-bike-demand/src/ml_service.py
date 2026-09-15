"""Machine-learning prediction logic for the bike-demand app."""

from __future__ import annotations

from typing import Any, Dict

SEASON_FACTORS = {
    "Spring": 1.08,
    "Summer": 1.25,
    "Autumn": 1.04,
    "Winter": 0.72,
}

REQUIRED_FIELDS = {
    "hour",
    "temperature_c",
    "humidity_pct",
    "wind_speed_m_s",
    "visibility_10m",
    "rainfall_mm",
    "snowfall_cm",
    "season",
    "is_holiday",
    "is_working_day",
}


def validate_inputs(raw_inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and normalize the user inputs before prediction."""
    if not isinstance(raw_inputs, dict):
        raise ValueError("Input must be a dictionary of feature values.")

    missing = sorted(REQUIRED_FIELDS - set(raw_inputs.keys()))
    if missing:
        raise ValueError(f"Missing required input(s): {', '.join(missing)}")

    hour = raw_inputs["hour"]
    if not isinstance(hour, (int, float)) or isinstance(hour, bool):
        raise ValueError("Hour must be a number between 0 and 23.")
    hour = int(hour)
    if hour < 0 or hour > 23:
        raise ValueError("Hour must be between 0 and 23.")

    temperature = float(raw_inputs["temperature_c"])
    humidity = float(raw_inputs["humidity_pct"])
    wind_speed = float(raw_inputs["wind_speed_m_s"])
    visibility = float(raw_inputs["visibility_10m"])
    rainfall = float(raw_inputs["rainfall_mm"])
    snowfall = float(raw_inputs["snowfall_cm"])

    if temperature < -30 or temperature > 50:
        raise ValueError("Temperature must be between -30°C and 50°C.")
    if humidity < 0 or humidity > 100:
        raise ValueError("Humidity must be between 0% and 100%.")
    if wind_speed < 0 or wind_speed > 50:
        raise ValueError("Wind speed must be between 0 and 50 m/s.")
    if visibility < 0:
        raise ValueError("Visibility must be a non-negative value.")
    if rainfall < 0 or snowfall < 0:
        raise ValueError("Rainfall and snowfall must be non-negative.")

    season = str(raw_inputs["season"]).strip().title()
    if season not in SEASON_FACTORS:
        raise ValueError("Season must be one of: Spring, Summer, Autumn, Winter.")

    is_holiday = bool(raw_inputs["is_holiday"])
    is_working_day = bool(raw_inputs["is_working_day"])

    return {
        "hour": hour,
        "temperature_c": temperature,
        "humidity_pct": humidity,
        "wind_speed_m_s": wind_speed,
        "visibility_10m": visibility,
        "rainfall_mm": rainfall,
        "snowfall_cm": snowfall,
        "season": season,
        "is_holiday": is_holiday,
        "is_working_day": is_working_day,
    }


def predict_bike_demand(raw_inputs: Dict[str, Any]) -> float:
    """Return a predicted hourly bike demand using a simple interpretable model."""
    inputs = validate_inputs(raw_inputs)

    base_demand = 140.0
    season_factor = SEASON_FACTORS[inputs["season"]]

    if 6 <= inputs["hour"] <= 9 or 17 <= inputs["hour"] <= 19:
        hour_factor = 1.22
    elif 0 <= inputs["hour"] <= 5:
        hour_factor = 0.62
    else:
        hour_factor = 0.94

    working_day_factor = 1.18 if inputs["is_working_day"] else 0.82
    holiday_factor = 0.72 if inputs["is_holiday"] else 1.0

    prediction = (
        base_demand
        * season_factor
        * hour_factor
        * working_day_factor
        * holiday_factor
    )
    prediction += inputs["temperature_c"] * 8.0
    prediction -= max(0.0, inputs["humidity_pct"] - 60.0) * 1.5
    prediction -= inputs["wind_speed_m_s"] * 10.0
    prediction -= inputs["rainfall_mm"] * 24.0
    prediction -= inputs["snowfall_cm"] * 32.0
    prediction += inputs["visibility_10m"] * 0.04

    prediction = max(prediction, 20.0)
    return round(prediction, 2)
