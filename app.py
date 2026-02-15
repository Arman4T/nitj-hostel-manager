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

# --- 1. THEME TOGGLE LOGIC ---
if 'theme' not in st.session_state:
    st.session_state.theme = "Dark 🌙"

def apply_theme():
    if st.session_state.theme == "Dark 🌙":
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

# Apply the theme immediately
apply_theme()

# --- SESSION STATE SETUP ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'username' not in st.session_state:
    st.session_state.username = ""

# --- 2. LOGIN SCREEN ---
def login():
    st.markdown("<h1 style='text-align: center;'>🏛️ NITJ Hostel Portal</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            # THEME TOGGLE (On Login Page)
            st.write("Select Theme:")
            new_theme = st.radio("", ["Light ☀️", "Dark 🌙"], horizontal=True, index=1, key="login_theme")
            
            if new_theme != st.session_state.theme:
                st.session_state.theme = new_theme
                st.rerun()

            st.divider()
            st.info("For Demo: Use Password 'admin'")
            
            role = st.selectbox("Select Role", ["Student", "Warden", "Mess Manager"])
            username = st.text_input("Roll Number / ID")
            password = st.text_input("Password", type="password")
            
            if st.button("Login", type="primary", use_container_width=True):
                if password == "admin":
                    st.session_state.logged_in = True
                    st.session_state.role = role
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Wrong Password! Try 'admin'")

# --- 3. DASHBOARDS ---
def student_dashboard():
    st.title("Student Dashboard")
    tab1, tab2, tab3 = st.tabs(["Maintenance", "Mess Feedback", "Guest Pass"])
    
    with tab1:
        st.subheader("Report an Issue")
        c1, c2 = st.columns(2)
        issue = c1.selectbox("Category", ["Electrical", "Plumbing", "Carpenter", "Wi-Fi"])
        priority = c2.select_slider("Priority", ["Low", "Medium", "High", "Critical"])
        desc = st.text_area("Description")
        if st.button("Submit Ticket"):
            st.success(f"Ticket for {issue} raised successfully!")
            
    with tab2:
        st.subheader("Rate Today's Meal")
        st.info("Menu: Rajma Chawal")
        st.feedback("stars")
        
    with tab3:
        st.write("Generate a digital pass for your guest.")
        if st.button("Generate Gate Pass"):
            st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=NITJ-PASS-123", width=150)

def warden_dashboard():
    st.title("Warden Dashboard")
    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Occupancy", "485/500", "97%")
    c2.metric("Pending Complaints", "12", "-3 today")
    c3.metric("Mess Rating", "3.8/5", "-0.4")
    
    st.subheader("Recent Tickets")
    data = pd.DataFrame({
        "Room": ["204", "108", "305"],
        "Issue": ["Fan Broken", "Leaking Tap", "No Wi-Fi"],
        "Status": ["Open", "Open", "Critical"]
    })
    st.dataframe(data, use_container_width=True)

# --- MAIN APP ROUTER ---
if not st.session_state.logged_in:
    login()
else:
    # Sidebar Navigation
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # THEME TOGGLE (In Sidebar)
        st.write("Theme Mode:")
        side_theme = st.radio("", ["Light ☀️", "Dark 🌙"], index=0 if st.session_state.theme == "Light ☀️" else 1, key="sidebar_theme")
        
        if side_theme != st.session_state.theme:
            st.session_state.theme = side_theme
            st.rerun()
            
        st.divider()
        st.write(f"User: **{st.session_state.username}**")
        st.write(f"Role: **{st.session_state.role}**")
        
        if st.button("Logout", type="primary"):
            st.session_state.logged_in = False
            st.rerun()

    # Show the correct dashboard based on role
    if st.session_state.role == "Student":
        student_dashboard()
    elif st.session_state.role == "Warden":
        warden_dashboard()
    else:
        st.title("Mess Manager Dashboard")
        st.warning("Inventory Module is under construction.")
