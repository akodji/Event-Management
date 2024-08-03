import streamlit as st

# Add CSS styling to include background image
st.markdown(
    """
    <style>
    .main {
        background-image: url("pexels-towfiqu-barbhuiya-3440682-9810172");
        background-size: cover;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Your existing Streamlit code follows
st.title("Event Scheduler and Calendar")
# Continue with the rest of your code...
