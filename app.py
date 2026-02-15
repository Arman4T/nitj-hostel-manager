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

apply_theme()

# --- SESSION STATE SETUP ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'username' not in st.session_state:
    st.session_state.username = ""

# --- SHARED DATA (MENU & POLLS) ---
if 'menu' not in st.session_state:
    st.session_state.menu = {
        "Breakfast": "Aloo Paratha & Curd",
        "Lunch": "Rajma Chawal",
        "Dinner": "Mix Veg & Chapati"
    }
# POLL STATE
if 'poll' not in st.session_state:
    st.session_state.poll = {
        "active": False,
        "question": "",
        "options": [],
        "votes": {} 
    }
if 'has_voted' not in st.session_state:
    st.session_state.has_voted = False

# --- 2. LOGIN SCREEN ---
def login():
    st.markdown("<h1 style='text-align: center;'>🏛️ NITJ Hostel Portal</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
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
    
    # ALERT: POLL NOTIFICATION
    if st.session_state.poll['active'] and not st.session_state.has_voted:
        st.info("🗳️ **New Poll Active:** The Mess Manager wants your opinion!")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Maintenance", "Mess Feedback", "Guest Pass", "🗳️ Vote for Meal"])
    
    with tab1:
        st.subheader("Report an Issue")
        c1, c2 = st.columns(2)
        issue = c1.selectbox("Category", ["Electrical", "Plumbing", "Carpenter", "Wi-Fi"])
        priority = c2.select_slider("Priority", ["Low", "Medium", "High", "Critical"])
        desc = st.text_area("Description")
        if st.button("Submit Ticket"):
            st.success(f"Ticket for {issue} raised successfully!")
            
    with tab2:
        st.subheader("Today's Menu (Live Update)")
        c1, c2, c3 = st.columns(3)
        c1.info(f"**Breakfast:**\n{st.session_state.menu['Breakfast']}")
        c2.info(f"**Lunch:**\n{st.session_state.menu['Lunch']}")
        c3.info(f"**Dinner:**\n{st.session_state.menu['Dinner']}")
        st.write("Rate Today's Food:")
        st.feedback("stars")
        
    with tab3:
        if st.button("Generate Gate Pass"):
            st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=NITJ-PASS-123", width=150)

    # --- VOTING TAB ---
    with tab4:
        st.header("Community Poll")
        if st.session_state.poll['active']:
            st.write(f"### {st.session_state.poll['question']}")
            
            if not st.session_state.has_voted:
                vote = st.radio("Choose your preference:", st.session_state.poll['options'])
                if st.button("Submit Vote"):
                    st.session_state.poll['votes'][vote] += 1
                    st.session_state.has_voted = True
                    st.success("Vote Recorded!")
                    st.rerun()
            else:
                st.success("You have already voted.")
                # Show results to student too
                chart_data = pd.DataFrame(list(st.session_state.poll['votes'].items()), columns=["Option", "Votes"])
                st.bar_chart(chart_data.set_index("Option"))
        else:
            st.write("No active polls at the moment.")

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
    
    tab1, tab2, tab3 = st.tabs(["📝 Update Menu", "🗳️ Create Poll", "📉 Wastage"])
    
    with tab1:
        st.subheader("Set Menu for Tomorrow")
        with st.form("menu_form"):
            c1, c2, c3 = st.columns(3)
            b_new = c1.text_input("Breakfast Item", value=st.session_state.menu['Breakfast'])
            l_new = c2.text_input("Lunch Item", value=st.session_state.menu['Lunch'])
            d_new = c3.text_input("Dinner Item", value=st.session_state.menu['Dinner'])
            if st.form_submit_button("Update Menu"):
                st.session_state.menu['Breakfast'] = b_new
                st.session_state.menu['Lunch'] = l_new
                st.session_state.menu['Dinner'] = d_new
                st.success("Menu Updated!")

    # --- POLL CREATION ---
    with tab2:
        st.subheader("Launch Student Poll")
        
        c1, c2 = st.columns([1, 1])
        
        with c1:
            with st.form("poll_form"):
                q = st.text_input("Poll Question", placeholder="e.g. Breakfast for Sunday?")
                opt1 = st.text_input("Option 1", placeholder="Aloo Paratha")
                opt2 = st.text_input("Option 2", placeholder="Poha & Jalebi")
                
                if st.form_submit_button("Start Poll"):
                    if q and opt1 and opt2:
                        st.session_state.poll = {
                            "active": True,
                            "question": q,
                            "options": [opt1, opt2],
                            "votes": {opt1: 0, opt2: 0}
                        }
                        st.session_state.has_voted = False # Reset voting for demo
                        st.success("Poll Launched! Students can now vote.")
                        st.rerun()
        
        with c2:
            st.write("### Live Results")
            if st.session_state.poll['active']:
                st.info(f"Q: {st.session_state.poll['question']}")
                chart_data = pd.DataFrame(list(st.session_state.poll['votes'].items()), columns=["Option", "Votes"])
                st.bar_chart(chart_data.set_index("Option"))
                
                if st.button("End Poll"):
                    st.session_state.poll['active'] = False
                    st.warning("Poll Ended.")
                    st.rerun()
            else:
                st.write("No active poll.")

    with tab3:
        st.write("Wastage Analytics Module")
        st.bar_chart(pd.DataFrame({"Day": ["Mon", "Tue"], "Waste": [12, 10]}).set_index("Day"))

# --- MAIN APP ROUTER ---
if not st.session_state.logged_in:
    login()
else:
    with st.sidebar:
        st.title("⚙️ Settings")
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

    if st.session_state.role == "Student":
        student_dashboard()
    elif st.session_state.role == "Warden":
        warden_dashboard()
    elif st.session_state.role == "Mess Manager":
        mess_manager_dashboard()
