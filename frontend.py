
import streamlit as st
import requests

API_URL = "https://credit-card-fraud-detection-deployed-project-zhcx-bdqz7cjbw.vercel.app/predict"

st.title("Credit Card Fraud Detection Predictor")
st.markdown("Enter your transaction details below:")

# Input Fields
amount = st.number_input(
    "Amount", min_value=0.0, value=30.0
)

transaction_hour = st.number_input(
    "Transaction Hour", min_value=0, max_value=23, value=3
)

foreign_transaction = st.number_input(
    "Foreign Transaction (0 = No, 1 = Yes)",
    min_value=0, max_value=1, value=1
)

location_mismatch = st.number_input(
    "Location Mismatch (0 = No, 1 = Yes)",
    min_value=0, max_value=1, value=1
)

device_trust_score = st.number_input(
    "Device Trust Score", min_value=0, max_value=100, value=50
)

velocity_last_24h = st.number_input(
    "Velocity Last 24 Hours", min_value=0, value=33
)

cardholder_age = st.number_input(
    "Cardholder Age", min_value=1, max_value=100, value=18
)

merchant_category = st.selectbox(
    "Merchant Category",
    ["Electronics", "Travel", "Grocery", "Food", "Clothing"]
)

if st.button("Predict Fraud or Not"):

    input_data = {
        "amount": amount,
        "transaction_hour": transaction_hour,
        "foreign_transaction": foreign_transaction,
        "location_mismatch": location_mismatch,
        "device_trust_score": device_trust_score,
        "velocity_last_24h": velocity_last_24h,
        "cardholder_age": cardholder_age,
        "merchant_category": merchant_category
    }

    try:
        response = requests.post(
            API_URL,
            json=input_data,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()

            if "is_fraud" in result:
                prediction = result["is_fraud"]

                if prediction == 1:
                    st.error("Prediction: Yes, it's Fraud")
                elif prediction == 0:
                    st.success("Prediction: No, it's Not Fraud")
                else:
                    st.warning(f"Unexpected prediction value: {prediction}")
            else:
                st.error("API response mein 'is_fraud' field nahi hai.")
                st.json(result)

        else:
            st.error(f"API Error: {response.status_code}")
            st.code(response.text)

    except requests.exceptions.ConnectionError:
        st.error(
            "FastAPI server se connection nahi ho raha. "
            "Check karo ke backend running hai."
        )

    except requests.exceptions.Timeout:
        st.error("API request timeout ho gayi. Dobara try karo.")

    except requests.exceptions.RequestException as e:
        st.error(f"Request error: {e}")

    except ValueError:
        st.error("API ne valid JSON response return nahi kiya.")
