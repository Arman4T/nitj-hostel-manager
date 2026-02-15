import streamlit as st
import pandas as pd
import time
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NITJ Hostel & Mess Automation",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE (The "Memory" of the app) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'tickets' not in st.session_state:
    st.session_state.tickets = [
        {"ID": 101, "Room": "BH2-204", "Issue": "Fan Regulator Broken", "Status": "Open", "Priority": "Medium"},
        {"ID": 102, "Room": "BH2-108", "Issue": "Leaking Tap", "Status": "Resolved", "Priority": "Low"},
        {"ID": 103, "Room": "BH2-305", "Issue": "Wi-Fi Router Dead", "Status": "Open", "Priority": "High"}
    ]

# --- LOGIN SYSTEM ---
def login():
    st.markdown("## 🔐 Login to NITJ Hostel Portal")
    st.markdown("*(For Buildathon Demo: Password is 'admin')*")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/en/e/e6/NIT_Jalandhar_Logo.png", width=150)
    
    with col2:
        role = st.selectbox("Select Role", ["Student", "Warden", "Mess Manager"])
        username = st.text_input("Roll Number / Employee ID")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", type="primary"):
            if password == "admin":  # Simple check for demo
                st.session_state.logged_in = True
                st.session_state.role = role
                st.session_state.username = username
                st.success("Login Successful!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Invalid Password. Try 'admin'")

# --- LOGOUT ---
def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.rerun()

# --- DASHBOARDS ---
def student_dashboard():
    st.title(f"👋 Welcome, {st.session_state.username}")
    
    tab1, tab2, tab3 = st.tabs(["📝 Maintenance", "🍛 Mess Feedback", "🎟️ Guest Pass"])
    
    with tab1:
        st.subheader("Report an Issue")
        with st.form("ticket_form"):
            issue = st.selectbox("Issue Type", ["Electrical", "Plumbing", "Carpenter", "Internet"])
            desc = st.text_area("Description")
            uploaded_file = st.file_uploader("Upload Photo (Optional)")
            submitted = st.form_submit_button("Submit Ticket")
            
            if submitted:
                new_ticket = {"ID": random.randint(104, 999), "Room": "BH2-Current", "Issue": f"{issue} - {desc}", "Status": "Open", "Priority": "Medium"}
                st.session_state.tickets.append(new_ticket)
                st.toast("Ticket Submitted Successfully! Warden notified.", icon="✅")
    
    with tab2:
        st.subheader("Rate Today's Meal")
        col1, col2 = st.columns(2)
        with col1:
            st.info("Today's Menu: Rajma Chawal & Curd")
            sentiment = st.feedback("stars")
        if sentiment is not None:
            st.toast("Feedback recorded! Analytics updated.", icon="📊")

    with tab3:
        st.subheader("Guest Meal Coordination")
        st.write("Generate a digital pass for your guest.")
        if st.button("Generate QR Code"):
            st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=NITJ-GUEST-PASS", caption="Scan at Mess Counter")

def warden_dashboard():
    st.title("🛡️ Warden Dashboard (BH-2)")
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Occupancy", "485/500", "+2")
    col2.metric("Pending Tickets", "5", "High Latency Alert", delta_color="inverse")
    col3.metric("Avg Resolution Time", "4.2 Hrs", "-1.5 Hrs")
    col4.metric("Mess Rating (Today)", "4.2/5.0", "Good")
    
    st.divider()
    
    # Ticket Management
    st.subheader("🚨 Maintenance Requisition Workflow")
    
    df_tickets = pd.DataFrame(st.session_state.tickets)
    st.dataframe(df_tickets, use_container_width=True)
    
    col_act1, col_act2 = st.columns(2)
    with col_act1:
        ticket_id = st.number_input("Enter Ticket ID to Close", min_value=100, step=1)
    with col_act2:
        if st.button("Mark as Resolved"):
            # Logic to update ticket status
            for t in st.session_state.tickets:
                if t['ID'] == ticket_id:
                    t['Status'] = 'Resolved'
            st.success(f"Ticket #{ticket_id} closed!")
            st.balloons()
            time.sleep(1)
            st.rerun()

def mess_manager_dashboard():
    st.title("👨‍🍳 Mess Operations Center")
    st.warning("⚠️ Inventory Alert: Milk stock low (below 20L)")
    
    st.subheader("Consumption Analytics")
    chart_data = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "Wastage (kg)": [12, 10, 25, 8, 15]
    })
    st.bar_chart(chart_data.set_index("Day"))

# --- MAIN APP ROUTER ---
if not st.session_state.logged_in:
    login()
else:
    with st.sidebar:
        st.header("Navigation")
        st.write(f"Logged in as: **{st.session_state.role}**")
        if st.button("Logout", type="secondary"):
            logout()
            
    if st.session_state.role == "Student":
        student_dashboard()
    elif st.session_state.role == "Warden":
        warden_dashboard()
    elif st.session_state.role == "Mess Manager":
        mess_manager_dashboard()
