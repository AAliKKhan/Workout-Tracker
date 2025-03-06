import streamlit as st
import pandas as pd
import datetime
import plotly.express as px  
import os  

CSV_FILE = "workout_data.csv"

# ✅ Load Data Function
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE, parse_dates=["Date"])
    return pd.DataFrame(columns=["Date", "Title", "Exercise", "Weight (kg)", "Reps", "Sets"])

# ✅ Save Data Function
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# ✅ Initialize session state with saved data
if "workout_data" not in st.session_state:
    st.session_state.workout_data = load_data()

st.title("🏋️ Gym Workout Tracker")

# 🎯 Select Date & Title
st.subheader("🗓️ Select Workout Date & Title")
date = st.date_input("Workout Date", datetime.date.today())
title = st.text_input("Workout Title (e.g., Chest Day, Leg Day)", key="workout_title")

# 🎯 Log Workout Data
st.subheader("🏋️ Log Your Set")
exercise = st.text_input("Exercise Name (e.g., Squat, Deadlift)")
weight = st.number_input("Weight (kg)", min_value=0, step=1)
reps = st.number_input("Reps", min_value=1, max_value=100, step=1)
sets = st.number_input("Sets", min_value=1, max_value=10, step=1)

if st.button("➕ Add Set"):
    if exercise and title:
        new_entry = pd.DataFrame(
            [[date, title, exercise, weight, reps, sets]],
            columns=["Date", "Title", "Exercise", "Weight (kg)", "Reps", "Sets"]
        )
        st.session_state.workout_data = pd.concat([st.session_state.workout_data, new_entry], ignore_index=True)
        save_data(st.session_state.workout_data)
        st.success("✅ Set logged successfully!")
    else:
        st.warning("⚠️ Please enter both a Workout Title and Exercise Name.")

# 🎯 Display Today's Workout
st.subheader("📜 Today's Workout")

if not st.session_state.workout_data.empty:
    # ✅ Fix Date Format
    st.session_state.workout_data["Date"] = pd.to_datetime(
        st.session_state.workout_data["Date"], errors="coerce", format="%Y-%m-%d"
    ).dt.date

    todays_workouts = st.session_state.workout_data[st.session_state.workout_data["Date"] == date]

    if not todays_workouts.empty:
        for title in todays_workouts["Title"].unique():
            st.markdown(f"### 🏷️ {title}")
            filtered_workouts = todays_workouts[todays_workouts["Title"] == title]
            st.dataframe(filtered_workouts[["Exercise", "Weight (kg)", "Reps", "Sets"]])
    else:
        st.info("No workouts logged for today yet.")
else:
    st.info("No workout history available. Start logging your workouts!")

# 🎯 Display All Logged Workouts
st.subheader("📜 All Logged Workouts")
if not st.session_state.workout_data.empty:
    st.dataframe(st.session_state.workout_data.sort_values(by="Date", ascending=False))
else:
    st.info("No workouts logged yet.")

# 🎯 Progress Over Time
st.subheader("📈 Progress Over Time")

if not st.session_state.workout_data.empty:
    # ✅ Fix Date Format for Progress Chart
    st.session_state.workout_data["Date"] = pd.to_datetime(
        st.session_state.workout_data["Date"], errors="coerce", format="%Y-%m-%d"
    )

    fig = px.line(st.session_state.workout_data, x="Date", y=["Reps", "Weight (kg)"], color="Exercise", title="Workout Progress Over Time")
    st.plotly_chart(fig, use_container_width=True)

    # 🎯 Show Personal Bests
    st.subheader("🏆 Personal Bests")
    best_per_exercise = st.session_state.workout_data.groupby("Exercise")["Weight (kg)"].max()
    st.write(best_per_exercise)
else:
    st.info("No workout data to display progress.")
