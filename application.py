import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# Set page configuration
st.set_page_config(
    page_title="Event Scheduler",
    page_icon="📅",
    layout="wide"
)

# Function to encode the image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set banner image
def set_banner_image(banner_image):
    banner_base64 = get_base64_of_bin_file(banner_image)
    st.markdown(
        f"""
        <style>
        .banner {{
            background-image: url(data:image/png;base64,{banner_base64});
            background-size: cover;
            background-position: center;
            padding: 150px 0;
            margin-bottom: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set banner image
set_banner_image('event.jpg')  # replace with your image file name

# Create a banner container without the title
st.ma
