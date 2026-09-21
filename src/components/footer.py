import streamlit as st
from PIL import Image
import base64

def footer_home():
    with open("src/imagesss/home_screen_image.png", "rb") as f:
        img = base64.b64encode(f.read()).decode()

    st.markdown("""
    <div style='text-align:center; color:white; margin-top:20px;'>
        <p>EchoAttend © 2026 <br/> AI-Powered Smart Attendance</p>
    </div>
    """, unsafe_allow_html=True)


def footer_dashboard():
    with open("src/imagesss/home_screen_image.png", "rb") as f:
        img = base64.b64encode(f.read()).decode()

    st.markdown("""
    <div style='text-align:center; color:white; margin-top:20px;'>
        <p>EchoAttend © 2026 <br/> AI-Powered Smart Attendance</p>
    </div>
    """, unsafe_allow_html=True)