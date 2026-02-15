import streamlit as st
import pandas as pd
import time
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NITJ Hostel Ops",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. THEME LOGIC (SLIDER VERSION) ---
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True 

def apply_theme():
    if st.session_state.dark_mode:
        st.markdown("""
            <style>
            .stApp { background-color: #0e1117; color: #fafafa; }
            [data-testid="stSidebar"] { background-color: #262730; }
            div[data-testid="stMetric"] { background-color: #1f2129; border: 1px solid #41424C; color: #fff; }
            </style>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp { background-color: #ffffff; color: #31333F; }
            [data-testid="stSidebar"] { background-color: #f0f2f6; }
            div[data-testid="stMetric"] { background-color: #ffffff; border: 1px solid #e6e6e6; box-shadow: 0 2px 5px rgba(0,0,0,0.05); color: #000; }
            </style>
            """, unsafe_allow_html=True)

apply_theme()

# --- SESSION STATE SETUP ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'username' not in st.session_state:
    st.session_state.username = ""

# SHARED DATA
if 'menu' not in st.session_state:
    st.session_state.menu = {
        "Breakfast": "Aloo Paratha & Curd",
        "Lunch": "Rajma Chawal",
        "Dinner": "Mix Veg & Chapati"
    }
if 'poll' not in st.session_state:
    st.session_state.poll = {"active": False, "question": "", "options": [], "votes": {}}
if 'has_voted' not in st.session_state:
    st.session_state.has_voted = False
if 'wastage_data' not in st.session_state:
    st.session_state.wastage_data = [
        {"Day": "Monday", "Waste (kg)": 12},
        {"Day": "Tuesday", "Waste (kg)": 1
