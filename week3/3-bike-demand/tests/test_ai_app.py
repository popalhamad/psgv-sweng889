import pytest

from src.ml_service import predict_bike_demand, validate_inputs
from src.llm_service import generate_guidance


VALID_FEATURES = {
    "hour": 17,
    "temperature_c": 25.0,
    "humidity_pct": 55,
    "wind_speed_m_s": 2.5,
    "visibility_10m": 1200,
    "rainfall_mm": 0.0,
    "snowfall_cm": 0.0,
    "season": "Summer",
    "is_holiday": 0,
    "is_working_day": 1,
}


def test_prediction_for_valid_input():
    prediction = predict_bike_demand(VALID_FEATURES)
    assert isinstance(prediction, float)
    assert prediction > 0


def test_invalid_input_raises_value_error():
    invalid = dict(VALID_FEATURES)
    invalid["humidity_pct"] = -5

    with pytest.raises(ValueError):
        validate_inputs(invalid)


def test_llm_guidance_handles_unavailable_service(monkeypatch):
    def raise_error(*args, **kwargs):
        raise RuntimeError("LLM unavailable")

    monkeypatch.setattr("src.llm_service.requests.post", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("LLM unavailable")))

    guidance = generate_guidance(340, VALID_FEATURES)
    assert "Demand" in guidance or "monitor" in guidance.lower()
