import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="NITJ Hostel Manager", layout="wide")

# --- TITLE & SIDEBAR ---
st.title("🏛️ NITJ Hostel & Mess Management System")
st.sidebar.header("Navigation")
menu = st.sidebar.radio("Go to:", ["Dashboard (Occupancy)", "Maintenance Requisition", "Mess Feedback", "Guest Meals"])

# --- MOCK DATA (Simulating Database) ---
# In a real app, this would connect to Google Sheets or SQL.
# For a 3-hour demo, we use static variables.

if 'complaints' not in st.session_state:
    st.session_state.complaints = []

if 'guests' not in st.session_state:
    st.session_state.guests = []

# --- 1. DASHBOARD (Occupancy & Visibility) ---
if menu == "Dashboard (Occupancy)":
    st.header("📊 Real-Time Hostel Occupancy (BH-2)")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Capacity", "500 Beds")
    col2.metric("Current Occupancy", "485 Students", "+2 this week")
    col3.metric("Vacant Beds", "15", "-2 this week")
    
    st.subheader("Communication Latency Monitor")
    st.info("System Status: All systems operational. Average ticket response time: 2.4 Hours.")
    
    # Simple Chart
    chart_data = pd.DataFrame({
        'Floors': ['Ground', '1st', '2nd', '3rd', '4th'],
        'Occupancy %': [98, 95, 88, 92, 100]
    })
    st.bar_chart(chart_data.set_index('Floors'))

# --- 2. MAINTENANCE REQUISITION (Workflows) ---
elif menu == "Maintenance Requisition":
    st.header("🛠️ Maintenance Requisition Workflow")
    
    with st.form("complaint_form"):
        col1, col2 = st.columns(2)
        name = col1.text_input("Student Name")
        room = col2.text_input("Room Number")
        category = st.selectbox("Issue Category", ["Electrical", "Plumbing", "Carpenter", "Wi-Fi"])
        priority = st.select_slider("Priority Level", options=["Low", "Medium", "High", "Critical"])
        desc = st.text_area("Description of Issue")
        
        submitted = st.form_submit_button("Submit Ticket")
        
        if submitted:
            # Automation Logic: Create a ticket
            ticket = {
                "ID": len(st.session_state.complaints) + 1,
                "Room": room,
                "Category": category,
                "Priority": priority,
                "Status": "Open",
                "Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.complaints.append(ticket)
            st.success(f"Ticket #{ticket['ID']} Created! Warden notified via Email (Simulated).")

    # Display Active Tickets
    st.subheader("Active Maintenance Tickets")
    if st.session_state.complaints:
        df = pd.DataFrame(st.session_state.complaints)
        st.dataframe(df)
    else:
        st.write("No active complaints.")

# --- 3. MESS FEEDBACK (Quality System) ---
elif menu == "Mess Feedback":
    st.header("🍛 Mess Food Quality Feedback")
    
    st.subheader("Today's Menu: Aloo Paratha (Breakfast)")
    
    rating = st.slider("Rate Today's Meal (1-5)", 1, 5, 3)
    feedback = st.text_input("Any specific comments?")
    
    if st.button("Submit Feedback"):
        if rating < 3:
            st.error("Low Rating Recorded. Alert sent to Mess Secretary.")
        else:
            st.success("Thank you for your feedback!")

# --- 4. GUEST MEAL COORDINATION ---
elif menu == "Guest Meals":
    st.header("👥 Guest Meal Coordination")
    
    with st.form("guest_form"):
        host_name = st.text_input("Host Student Name")
        guest_count = st.number_input("Number of Guests", min_value=1, max_value=5)
        meal_type = st.selectbox("Meal Type", ["Lunch", "Dinner"])
        date = st.date_input("Date")
        
        submit_guest = st.form_submit_button("Generate Coupon")
        
        if submit_guest:
            st.success(f"Coupon Generated for {guest_count} guest(s)!")
            st.balloons()
            st.code(f"COUPON CODE: NITJ-{date}-{host_name[:3].upper()}-001")
