import streamlit as st
from PIL import Image
import base64

def header_home():
    with open("src/imagesss/home_screen_image.png", "rb") as f:
        img = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:10px; margin-top:10px;">
        <img src="data:image/png;base64,{img}" style="height:100px; border-radius:5px;">
        <h1 style="text-align:center; color:#E0E3FF">Echo<br/>Attend </h1>
    </div>
    """, unsafe_allow_html=True)


def header_dashboard():
    with open("src/imagesss/home_screen_image.png", "rb") as f:
        img = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:center; gap:10px;">
        <img src="data:image/png;base64,{img}" style="height:85px; border-radius:5px;">
        <h2 style="text-align:left; color:#5865F2;">Echo<br/>Attend </h2>
    </div>
    """, unsafe_allow_html=True)