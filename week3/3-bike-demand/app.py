"""Streamlit dashboard for bike-demand prediction and AI guidance."""

from __future__ import annotations

import streamlit as st

from llm_service import generate_guidance
from predict import predict_bike_demand

SEASONS = ["Spring", "Summer", "Autumn", "Winter"]


st.set_page_config(page_title="Bike Demand Assistant", page_icon="🚲", layout="centered")

st.title("Bike Demand Assistant")
st.caption("Predict hourly bike demand and get a local AI explanation.")

with st.form("bike_demand_form"):
    col1, col2 = st.columns(2)
    with col1:
        hour = st.number_input("Hour of day", min_value=0, max_value=23, value=17)
        temperature = st.number_input("Temperature (°C)", value=25.0)
        humidity = st.number_input("Humidity (%)", min_value=0, max_value=100, value=55)
        wind_speed = st.number_input("Wind speed (m/s)", min_value=0.0, value=2.5)
        visibility = st.number_input("Visibility (10m)", min_value=0, value=1200)
    with col2:
        rainfall = st.number_input("Rainfall (mm)", min_value=0.0, value=0.0)
        snowfall = st.number_input("Snowfall (cm)", min_value=0.0, value=0.0)
        season = st.selectbox("Season", SEASONS)
        is_holiday = st.checkbox("Holiday")
        is_working_day = st.checkbox("Working day", value=True)

    submitted = st.form_submit_button("Predict bike demand")

if submitted:
    inputs = {
        "hour": int(hour),
        "temperature_c": float(temperature),
        "humidity_pct": float(humidity),
        "wind_speed_m_s": float(wind_speed),
        "visibility_10m": float(visibility),
        "rainfall_mm": float(rainfall),
        "snowfall_cm": float(snowfall),
        "season": season,
        "is_holiday": bool(is_holiday),
        "is_working_day": bool(is_working_day),
    }

    try:
        prediction = predict_bike_demand(inputs)
        guidance, llm_used = generate_guidance(prediction, inputs, return_status=True)

        st.subheader("Prediction")
        st.metric(label="Predicted bike demand", value=f"{prediction:,.0f} rentals")

        st.subheader("AI-generated guidance")
        if llm_used:
            st.success("Local Ollama response")
        else:
            st.warning("Local LLM unavailable; using built-in fallback guidance.")
        st.write(guidance)
    except ValueError as exc:
        st.error(str(exc))
        st.info("Please check the required values and try again.")
