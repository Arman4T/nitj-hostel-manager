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

# --- GLOBAL STATE (CACHE BUSTER V2 applied) ---
class HostelData_V2:
    def __init__(self):
        self.menu = {
            "Breakfast": "Aloo Paratha & Curd",
            "Lunch": "Rajma Chawal",
            "Dinner": "Mix Veg & Chapati"
        }
        self.poll = {"active": False, "question": "", "options": [], "votes": {}}
        self.tickets = [
            {"ID": 101, "Room": "204", "Issue": "Fan Broken", "Priority": "Medium", "Status": "Open"}
        ]
        self.wastage = [{"Day": "Monday", "Waste (kg)": 12}]
        self.announcements = [] # This caused the error before, fixed now in V2

# Renaming this function forces Streamlit to reset the cache
@st.cache_resource
def get_data_v2():
    return HostelData_V2()

shared_data = get_data_v2()

# --- THEME LOGIC ---
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

# --- LOCAL SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'has_voted' not in st.session_state:
    st.session_state.has_voted = False

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
    
    # SAFE ANNOUNCEMENT CHECK
    if hasattr(shared_data, 'announcements') and shared_data.announcements:
        st.error(f"📢 **NOTICE:** {shared_data.announcements[0]}")

    if shared_data.poll['active'] and not st.session_state.has_voted:
        st.info("🗳️ **New Poll Active:** The Mess Manager wants your opinion!")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Maintenance", "Mess Feedback", "Guest Pass", "Vote"])
    
    with tab1:
        st.subheader("Report an Issue")
        c1, c2 = st.columns(2)
        room_no = c1.text_input("Room Number", placeholder="e.g. 305")
        cat = c2.selectbox("Category", ["Electrical", "Plumbing", "Carpenter", "Wi-Fi"])
        desc = st.text_area("Description")
        priority = st.select_slider("Priority", ["Low", "Medium", "High", "Critical"])
        
        if st.button("Submit Ticket"):
            if room_no and desc:
                # Safe ID Generation
                new_id = len(shared_data.tickets) + 101
                new_ticket = {
                    "ID": new_id,
                    "Room": room_no,
                    "Issue": f"{cat} - {desc}",
                    "Priority": priority,
                    "Status": "Open"
                }
                shared_data.tickets.append(new_ticket)
                st.success(f"Ticket #{new_id} Sent! Warden can see it instantly.")
            else:
                st.error("Please fill details.")
            
    with tab2:
        st.subheader("Today's Menu (Live)")
        c1, c2, c3 = st.columns(3)
        c1.info(f"**Breakfast:**\n{shared_data.menu['Breakfast']}")
        c2.info(f"**Lunch:**\n{shared_data.menu['Lunch']}")
        c3.info(f"**Dinner:**\n{shared_data.menu['Dinner']}")
        st.write("Rate Today's Food:")
        st.feedback("stars")
        
    with tab3:
        if st.button("Generate Gate Pass"):
            st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=NITJ-PASS-123", width=150)

    with tab4:
        st.header("Community Poll")
        if shared_data.poll['active']:
            st.write(f"### {shared_data.poll['question']}")
            if not st.session_state.has_voted:
                vote = st.radio("Choose:", shared_data.poll['options'])
                if st.button("Submit Vote"):
                    shared_data.poll['votes'][vote] += 1
                    st.session_state.has_voted = True
                    st.rerun()
            else:
                st.success("You voted!")
                chart_data = pd.DataFrame(list(shared_data.poll['votes'].items()), columns=["Option", "Votes"])
                st.bar_chart(chart_data.set_index("Option"))
        else:
            st.write("No active polls.")

def warden_dashboard():
    st.title("Warden Dashboard")
    
    # ANNOUNCEMENT SYSTEM
    with st.expander("📢 Make Announcement (Broadcast)", expanded=True):
        new_announce = st.text_input("Message for Students", placeholder="e.g. Water Supply cut from 2-4 PM")
        if st.button("Broadcast"):
            if not hasattr(shared_data, 'announcements'):
                shared_data.announcements = []
            shared_data.announcements.insert(0, new_announce)
            st.success("Announcement Live!")
            st.rerun()

    c1, c2, c3 = st.columns(3)
    c1.metric("Occupancy", "485/500", "97%")
    open_tickets = [t for t in shared_data.tickets if t['Status'] == 'Open']
    c2.metric("Open Tickets", str(len(open_tickets)), "Action Required")
    c3.metric("Mess Rating", "3.8/5", "-0.4")
    
    st.divider()
    st.subheader("🚨 Ticket Management")
    
    col_list, col_action = st.columns([2, 1])
    
    with col_list:
        st.write("### Active Issues")
        if open_tickets:
            # SAFETY: Ensure ID exists
            safe_tickets = []
            for t in open_tickets:
                if 'ID' not in t: t['ID'] = 999
                safe_tickets.append(t)
            
            df = pd.DataFrame(safe_tickets)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.success("No Open Tickets! All Good.")

    with col_action:
        st.write("### Resolve Ticket")
        if open_tickets:
            # Create list for dropdown safely
            ticket_options = [f"#{t.get('ID', 999)} - Room {t['Room']}" for t in open_tickets]
            selected_str = st.selectbox("Select Ticket", ticket_options)
            
            if st.button("Mark as Closed"):
                try:
                    selected_id = int(selected_str.split(" ")[0].replace("#", ""))
                    for t in shared_data.tickets:
                        if t.get('ID') == selected_id:
                            t['Status'] = "Closed"
                    st.success(f"Ticket #{selected_id} Closed!")
                    time.sleep(0.5)
                    st.rerun()
                except:
                    st.error("Error closing ticket. Try refreshing.")
        else:
            st.info("No tickets to close.")

def mess_manager_dashboard():
    st.title("Mess Operations Center")
    
    # SAFE ANNOUNCEMENT CHECK
    if hasattr(shared_data, 'announcements') and shared_data.announcements:
        st.error(f"📢 **WARDEN NOTICE:** {shared_data.announcements[0]}")

    tab1, tab2, tab3 = st.tabs(["Update Menu", "Create Poll", "Wastage"])
    
    with tab1:
        st.subheader("Set Menu for Tomorrow")
        with st.form("menu_form"):
            c1, c2, c3 = st.columns(3)
            b_new = c1.text_input("Breakfast", value=shared_data.menu['Breakfast'])
            l_new = c2.text_input("Lunch", value=shared_data.menu['Lunch'])
            d_new = c3.text_input("Dinner", value=shared_data.menu['Dinner'])
            if st.form_submit_button("Update"):
                shared_data.menu['Breakfast'] = b_new
                shared_data.menu['Lunch'] = l_new
                shared_data.menu['Dinner'] = d_new
                st.success("Menu Updated for Everyone!")

    with tab2:
        st.subheader("Launch Student Poll")
        with st.form("poll_form"):
            q = st.text_input("Question")
            opt1 = st.text_input("Option 1")
            opt2 = st.text_input("Option 2")
            if st.form_submit_button("Start Poll"):
                shared_data.poll['active'] = True
                shared_data.poll['question'] = q
                shared_data.poll['options'] = [opt1, opt2]
                shared_data.poll['votes'] = {opt1: 0, opt2: 0}
                st.success("Poll LIVE on all devices!")
                st.rerun()
        
        if shared_data.poll['active']:
            st.divider()
            st.write("### Live Results")
            chart_data = pd.DataFrame(list(shared_data.poll['votes'].items()), columns=["Option", "Votes"])
            st.bar_chart(chart_data.set_index("Option"))
            if st.button("End Poll"):
                shared_data.poll['active'] = False
                st.rerun()

    with tab3:
        st.subheader("Wastage Analytics")
        with st.expander("Add New Data"):
            d = st.selectbox("Day", ["Wednesday", "Thursday", "Friday"])
            w = st.number_input("Kg", 0)
            if st.button("Add"):
                shared_data.wastage.append({"Day": d, "Waste (kg)": w})
        
        df = pd.DataFrame(shared_data.wastage)
        st.bar_chart(df.set_index("Day"))

# --- MAIN APP ROUTER ---
if not st.session_state.logged_in:
    login()
else:
    with st.sidebar:
        st.title("⚙️ Settings")
        
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
