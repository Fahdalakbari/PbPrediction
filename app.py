import streamlit as st
from utils import load_model, predict

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Bubble Point Pressure Prediction using PINN",
    page_icon="🛢️",
    layout="centered"
)

# ==========================================================
# Load Model
# ==========================================================

@st.cache_resource
def initialize():
    return load_model()

model, scalers = initialize()

# ==========================================================
# Default Values
# ==========================================================

DEFAULTS = {

    "T": "132",

    "N2": "0.0",
    "C1": "34.53",
    "C2": "7.24",
    "C3": "5.31",
    "C4": "2.79",
    "C5": "1.91",
    "C6": "3.48",
    "C7": "43.44",
    "MWC7": "200",
    "H2S": "0.0",
    "CO2": "1.3",
}

EMPTY = {k: "" for k in DEFAULTS}

# Initialize Session State

for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)

# ==========================================================
# Header
# ==========================================================

st.title("Bubble Point Pressure Prediction")

st.markdown(
"""
Predict **Bubble Point Pressure (Pb)** from reservoir fluid
composition using the Artificial Neural Networks (ANNs).
"""
)

st.divider()

# ==========================================================
# Inputs
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    st.session_state["T"] = st.text_input(
        "Temperature (°F)",
        value=st.session_state["T"]
    )

    st.session_state["N2"] = st.text_input(
        "N₂ (mol%)",
        value=st.session_state["N2"]
    )

    st.session_state["C1"] = st.text_input(
        "C1 (mol%)",
        value=st.session_state["C1"]
    )

    st.session_state["C2"] = st.text_input(
        "C2 (mol%)",
        value=st.session_state["C2"]
    )

    st.session_state["C3"] = st.text_input(
        "C3 (mol%)",
        value=st.session_state["C3"]
    )

    st.session_state["C4"] = st.text_input(
        "C4 (mol%)",
        value=st.session_state["C4"]
    )


with col2:

    st.session_state["C5"] = st.text_input(
        "C5 (mol%)",
        value=st.session_state["C5"]
    )

    st.session_state["C6"] = st.text_input(
        "C6 (mol%)",
        value=st.session_state["C6"]
    )

    st.session_state["C7"] = st.text_input(
        "C7+ (mol%)",
        value=st.session_state["C7"]
    )

    st.session_state["MWC7"] = st.text_input(
        "MW C7+",
        value=st.session_state["MWC7"]
    )

    st.session_state["H2S"] = st.text_input(
        "H₂S (mol%)",
        value=st.session_state["H2S"]
    )

    st.session_state["CO2"] = st.text_input(
        "CO₂ (mol%)",
        value=st.session_state["CO2"]
    )

st.divider()

# ==========================================================
# Buttons
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    predict_button = st.button(
        "Predict",
        use_container_width=True
    )

with col2:

    clear_button = st.button(
        "Clear",
        use_container_width=True
    )

# ==========================================================
# Clear
# ==========================================================

if clear_button:

    for key in EMPTY:
        st.session_state[key] = ""

    st.rerun()

# ==========================================================
# Prediction
# ==========================================================

if predict_button:

    try:

        T = float(st.session_state["T"])
        N2 = float(st.session_state["N2"])
        C1 = float(st.session_state["C1"])
        C2 = float(st.session_state["C2"])
        C3 = float(st.session_state["C3"])
        C4 = float(st.session_state["C4"])
        C5 = float(st.session_state["C5"])
        C6 = float(st.session_state["C6"])
        C7 = float(st.session_state["C7"])
        MWC7 = float(st.session_state["MWC7"])
        H2S = float(st.session_state["H2S"])
        CO2 = float(st.session_state["CO2"])

    except ValueError:

        st.error("Please enter numeric values in all fields.")
        st.stop()

    with st.spinner("Predicting Bubble Point Pressure..."):

        result = predict(
            model,
            scalers,
            T,
            N2,
            C1,
            C2,
            C3,
            C4,
            C5,
            C6,
            C7,
            MWC7,
            H2S,
            CO2,
        )

    st.divider()

    st.success(
        f"""
### Predicted Bubble Point Pressure

# **{result:.2f} psi**
"""
    )
