import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def generate_component_recommendations(budget, usage):
    try:
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        prompt = f"For a budget of ${budget} and intended use of {usage}, recommend compatible PC components (CPU, GPU, Motherboard, RAM, Storage, Power Supply, and Case) along with their current prices. Return the results in a list format, with each item on a new line, formatted as 'Component Name - $Price'."
        response = model.generate_content(prompt)
        recommendations = response.text.strip().split("\n")
        return recommendations
    except Exception as e:
        st.error(f"Error generating component recommendations: {e}")
        return []

st.title("PCBuilder AI")

budget = st.number_input("Enter your budget:", min_value=500, max_value=5000, step=100, key="budget")
usage = st.selectbox("Intended use:", ["Gaming", "Design", "Office", "General Use"], key="usage")

if st.button("Get Recommendations", key="recommendations_button"):
    st.write("Generating PC configuration based on your input...")

    recommendations = generate_component_recommendations(budget, usage)

    st.subheader("Recommended Components:")
    total_price = 0
    for component in recommendations:
        try:
            component_name = component.split(" - ")[0]
            price = float(component.split("$")[-1])
            st.write(f"- {component_name}: ${price:.2f}")
            total_price += price
        except:
            st.write(f"- {component}")

    st.write(f"Total Price: ${total_price:.2f}")
