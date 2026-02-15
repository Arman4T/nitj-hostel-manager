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

# --- 1. THEME LOGIC ---
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True # Default to Dark

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

# --- 2. LOGIN SCREEN ---
def login():
    st.markdown("<h1 style='text-align: center;'>🏛️ NITJ Hostel Portal</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            # SLIDER BUTTON FOR THEME
            is_dark = st.toggle("Dark Mode 🌙", value=st.session_state.dark_mode, key="login_toggle")
            if is_dark != st.session_state.dark_mode:
                st.session_state.dark_mode = is_dark
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
    if st.session_state.poll['active'] and not st.session_state.has_voted:
        st.info("🗳️ **New Poll Active:** The Mess Manager wants your opinion!")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Maintenance", "Mess Feedback", "Guest Pass", "Vote"])
    
    with tab1:
        st.subheader("Report an Issue")
        c1, c2 = st.columns(2)
        issue = c1.selectbox("Category", ["Electrical", "Plumbing", "Carpenter", "Wi-Fi"])
        priority = c2.select_slider("Priority", ["Low", "Medium", "High", "Critical"])
        if st.button("Submit Ticket"):
            st.success(f"Ticket for {issue} raised successfully!")
            
    with tab2:
        st.subheader("Today's Menu")
        c1, c2, c3 = st.columns(3)
        c1.info(f"**Breakfast:**\n{st.session_state.menu['Breakfast']}")
        c2.info(f"**Lunch:**\n{st.session_state.menu['Lunch']}")
        c3.info(f"**Dinner:**\n{st.session_state.menu['Dinner']}")
        st.write("Rate Today's Food:")
        st.feedback("stars")
        
    with tab3:
        if st.button("Generate Gate Pass"):
            st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=NITJ-PASS-123", width=150)

    with tab4:
        st.header("Community Poll")
        if st.session_state.poll['active']:
            st.write(f"### {st.session_state.poll['question']}")
            if not st.session_state.has_voted:
                vote = st.radio("Choose:", st.session_state.poll['options'])
                if st.button("Submit Vote"):
                    st.session_state.poll['votes'][vote] += 1
                    st.session_state.has_voted = True
                    st.rerun()
            else:
                st.success("You voted!")
                chart_data = pd.DataFrame(list(st.session_state.poll['votes'].items()), columns=["Option", "Votes"])
                st.bar_chart(chart_data.set_index("Option"))
        else:
            st.write("No active polls.")

def warden_dashboard():
    st.title("Warden Dashboard")
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

def mess_manager_dashboard():
    st.title("Mess Operations Center")
    tab1, tab
