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
        {"Day": "Tuesday", "Waste (kg)": 15}
    ]
# TICKET SYSTEM (Connected Data)
if 'tickets' not in st.session_state:
    st.session_state.tickets = [
        {"Room": "204", "Issue": "Electrical - Fan Broken", "Priority": "Medium", "Status": "Open"},
        {"Room": "108", "Issue": "Plumbing - Leaking Tap", "Priority": "Low", "Status": "Resolved"}
    ]

# --- 2. LOGIN SCREEN ---
def login():
    st.markdown("<h1 style='text-align: center;'>🏛️ NITJ Hostel Portal</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            # THEME SLIDER
            c_left, c_mid, c_right = st.columns([2, 1, 2])
            with c_left: st.markdown("<h5 style='text-align: right;'>Light ☀️</h5>", unsafe_allow_html=True)
            with c_mid: is_dark = st.toggle("", value=st.session_state.dark_mode, key="login_toggle", label_visibility="collapsed")
            with c_right: st.markdown("<h5 style='text-align: left;'>🌙 Dark</h5>", unsafe_allow_html=True)
            
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
        
        # --- NEW INPUTS HERE ---
        c1, c2 = st.columns(2)
        room_no = c1.text_input("Room Number", placeholder="e.g. 305")
        cat = c2.selectbox("Category", ["Electrical", "Plumbing", "Carpenter", "Wi-Fi"])
        
        desc = st.text_area("Description of Problem", placeholder="e.g. The fan is making a loud noise and rotating slowly...")
        priority = st.select_slider("Priority Level", ["Low", "Medium", "High", "Critical"])
        
        if st.button("Submit Ticket"):
            if room_no and desc:
                # Add to the global ticket list
                new_ticket = {
                    "Room": room_no,
                    "Issue": f"{cat} - {desc}",
                    "Priority": priority,
                    "Status": "Open"
                }
                st.session_state.tickets.append(new_ticket)
                st.success(f"Ticket raised for Room {room_no}! Warden Notified.")
            else:
                st.error("Please enter Room Number and Description.")
            
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
    c2.metric("Pending Complaints", str(len([t for t in st.session_state.tickets if t['Status']=='Open'])), "Live")
    c3.metric("Mess Rating", "3.8/5", "-0.4")
    
    st.subheader("Live Ticket Feed")
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(st.session_state.tickets)
    st.dataframe(df, use_container_width=True)

def mess_manager_dashboard():
    st.title("Mess Operations Center")
    tab1, tab2, tab3 = st.tabs(["Update Menu", "Create Poll", "Wastage Analytics"])
    
    with tab1:
        st.subheader("Set Menu for Tomorrow")
        with st.form("menu_form"):
            c1, c2, c3 = st.columns(3)
            b_new = c1.text_input("Breakfast", value=st.session_state.menu['Breakfast'])
            l_new = c2.text_input("Lunch", value=st.session_state.menu['Lunch'])
            d_new = c3.text_input("Dinner", value=st.session_state.menu['Dinner'])
            if st.form_submit_button("Update"):
                st.session_state.menu['Breakfast'] = b_new
                st.session_state.menu['Lunch'] = l_new
                st.session_state.menu['Dinner'] = d_new
                st.success("Menu Updated!")

    with tab2:
        st.subheader("Launch Student Poll")
        with st.form("poll_form"):
            q = st.text_input("Question")
            opt1 = st.text_input("Option 1")
            opt2 = st.text_input("Option 2")
            if st.form_submit_button("Start Poll"):
                st.session_state.poll = {"active": True, "question": q, "options": [opt1, opt2], "votes": {opt1: 0, opt2: 0}}
                st.session_state.has_voted = False
                st.success("Poll Started!")
                st.rerun()
        
        if st.session_state.poll['active']:
            st.divider()
            st.write("### Live Results")
            chart_data = pd.DataFrame(list(st.session_state.poll['votes'].items()), columns=["Option", "Votes"])
            st.bar_chart(chart_data.set_index("Option"))
            if st.button("End Poll"):
                st.session_state.poll['active'] = False
                st.rerun()

    with tab3:
        st.subheader("Wastage Analytics")
        with st.expander("Add New Data"):
            d = st.selectbox("Day", ["Wednesday", "Thursday", "Friday"])
            w = st.number_input("Kg", 0)
            if st.button("Add"):
                st.session_state.wastage_data.append({"Day": d, "Waste (kg)": w})
        
        df = pd.DataFrame(st.session_state.wastage_data)
        st.bar_chart(df.set_index("Day"))

# --- MAIN APP ROUTER ---
if not st.session_state.logged_in:
    login()
else:
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # --- SIDEBAR THEME SLIDER ---
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1: st.write("☀️")
        with c2: is_dark_side = st.toggle("", value=st.session_state.dark_mode, key="sidebar_toggle", label_visibility="collapsed")
        with c3: st.write("🌙")
            
        if is_dark_side != st.session_state.dark_mode:
            st.session_state.dark_mode = is_dark_side
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
