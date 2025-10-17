import streamlit as st
from datetime import datetime, timedelta

# Initialize session state
if "reminders" not in st.session_state:
    st.session_state.reminders = []

st.title("🧓 Eldercare Reminder App")

# ---- Add New Reminder ----
st.header("Add New Reminder")
message = st.text_input("Reminder Message")
time_input = st.time_input("Reminder Time")

if st.button("Add Reminder"):
    reminder = {
        "message": message,
        "time": time_input,
        "done": False
    }
    st.session_state.reminders.append(reminder)
    st.success(f"Reminder '{message}' added at {time_input.strftime('%H:%M')}!")

# ---- Show All Reminders ----
st.header("Scheduled Reminders")
if st.session_state.reminders:
    for idx, rem in enumerate(st.session_state.reminders):
        status = "✅ Done" if rem["done"] else "⏰ Pending"
        st.write(f"{idx+1}. {rem['message']} at {rem['time'].strftime('%H:%M')} - {status}")
else:
    st.write("No reminders added yet.")

# ---- Check for Due Reminders ----
st.header("Alerts")
current_time = datetime.now().time()

for idx, rem in enumerate(st.session_state.reminders):
    if not rem["done"] and rem["time"].hour == current_time.hour and rem["time"].minute == current_time.minute:
        st.warning(f"🔔 Reminder: {rem['message']}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Mark Done: {rem['message']}", key=f"done_{idx}"):
                rem["done"] = True
                st.experimental_rerun()
        with col2:
            if st.button(f"Remind Later (5 min): {rem['message']}", key=f"later_{idx}"):
                new_time = (datetime.combine(datetime.today(), rem["time"]) + timedelta(minutes=5)).time()
                rem["time"] = new_time
                st.experimental_rerun()

# ---- Instructions ----
st.info("⏱️ To see alerts, keep this Streamlit tab open and click 'Rerun' (top-right) or refresh manually every minute.")
