import streamlit as st
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(page_title="Eldercare Reminder App", page_icon="💊", layout="centered")

# --- CUSTOM STYLE ---
st.markdown("""
    <style>
        body { background-color: #f4f6f9; }
        .main {
            background-color: #ffffff;
            border-radius: 16px;
            padding: 25px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        }
        .stButton>button {
            border-radius: 10px;
            height: 3em;
            width: 100%;
            background-color: #4CAF50;
            color: white;
            border: none;
            font-weight: 600;
        }
        .stButton>button:hover { background-color: #45a049; }
        .title {
            text-align: center;
            font-size: 2rem;
            color: #2c3e50;
            font-weight: 700;
            margin-bottom: 20px;
        }
        .section-title {
            color: #16a085;
            font-weight: 600;
            font-size: 1.3rem;
            margin-top: 20px;
        }
        .reminder-card {
            background: #e8f6f3;
            padding: 10px 15px;
            border-radius: 12px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- STATE INIT ---
if "reminders" not in st.session_state:
    st.session_state.reminders = []

# --- TITLE ---
st.markdown("<div class='title'>🧓 Eldercare Reminder App</div>", unsafe_allow_html=True)

# --- ADD REMINDER ---
st.markdown("<div class='section-title'>➕ Add New Reminder</div>", unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    message = st.text_input("Reminder Message", placeholder="e.g., Take medicine, drink water")

with col2:
    time_str = st.text_input("Enter Time (HH:MM)", placeholder="e.g., 14:30")

if st.button("Add Reminder"):
    if not message.strip():
        st.error("Please enter a reminder message.")
    elif not time_str.strip():
        st.error("Please enter a time.")
    else:
        try:
            # Convert string time to datetime.time object
            time_input = datetime.strptime(time_str, "%H:%M").time()
            st.session_state.reminders.append({
                "message": message,
                "time": time_input,
                "done": False
            })
            st.success(f"✅ Reminder '{message}' set for {time_input.strftime('%H:%M')}")
        except ValueError:
            st.error("Invalid time format! Please use HH:MM (24-hour format).")

# --- LIST REMINDERS ---
st.markdown("<div class='section-title'>🕒 Scheduled Reminders</div>", unsafe_allow_html=True)
if not st.session_state.reminders:
    st.info("No reminders added yet.")
else:
    for idx, rem in enumerate(st.session_state.reminders):
        bg = "#d1f2eb" if not rem["done"] else "#ecf0f1"
        st.markdown(f"""
            <div class='reminder-card' style='background:{bg}'>
                <b>{rem['message']}</b><br>
                ⏰ Time: {rem['time'].strftime('%H:%M')}<br>
                Status: {'✅ Done' if rem['done'] else '⏰ Pending'}
            </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button(f"Mark Done ✅ {idx}", key=f"done_{idx}"):
                rem["done"] = True
                st.experimental_rerun()
        with c2:
            if st.button(f"Remind Later (5 min) 🔁 {idx}", key=f"later_{idx}"):
                new_time = (datetime.combine(datetime.today(), rem["time"]) + timedelta(minutes=5)).time()
                rem["time"] = new_time
                st.experimental_rerun()

# --- ALERT SECTION ---
st.markdown("<div class='section-title'>🔔 Active Alerts</div>", unsafe_allow_html=True)
current_time = datetime.now().time()
alert_found = False

for rem in st.session_state.reminders:
    if not rem["done"] and rem["time"].hour == current_time.hour and rem["time"].minute == current_time.minute:
        st.warning(f"🔔 Reminder Time! {rem['message']}")
        alert_found = True

if not alert_found:
    st.info("No current alerts. All good! ✅")

# --- FOOTER ---
st.markdown("""
    <hr>
    <div style='text-align:center; color:grey; font-size:0.9rem'>
        Built with ❤️ using Streamlit | CareAide Eldercare App
    </div>
""", unsafe_allow_html=True)
