
import streamlit as st
import pandas as pd
from datetime import date, timedelta

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="FitTrack | Workout Log",
    page_icon="💪",
    layout="wide"
)

# -----------------------------
# CUSTOM DESIGN
# -----------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0b1120, #111c30);
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #101b2d;
}

[data-testid="stSidebar"] * {
    color: white;
}

h1, h2, h3 {
    color: white;
    font-weight: 700;
}

p, label {
    color: #d1d9e6;
}

div[data-testid="stMetric"] {
    background-color: #18263b;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #263b55;
}

div[data-testid="stMetricValue"] {
    color: #4ade80;
}

.stButton > button {
    background-color: #22c55e;
    color: #071525;
    border: none;
    border-radius: 8px;
    font-weight: 700;
}

.stButton > button:hover {
    background-color: #16a34a;
    color: white;
}

.stProgress > div > div > div > div {
    background-color: #22c55e;
}

hr {
    border-color: #263b55;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# SESSION STORAGE
# -----------------------------

if "workouts" not in st.session_state:
    st.session_state.workouts = []

if "steps" not in st.session_state:
    st.session_state.steps = {}

if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = 10000


# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------

st.sidebar.title("💪 FitTrack")
st.sidebar.caption("YOUR PERSONAL FITNESS TRACKER")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Add Workout", "Workout History", "Step Tracker"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Stay consistent. Keep improving.")


# -----------------------------
# DASHBOARD
# -----------------------------

if page == "Dashboard":

    st.title("Welcome to FitTrack 👋")
    st.write("Track your progress, stay active, and reach your fitness goals.")

    st.markdown("---")

    workouts = st.session_state.workouts

    total_workouts = len(workouts)
    total_minutes = sum(w["Duration"] for w in workouts)
    total_calories = sum(w["Calories"] for w in workouts)
    total_miles = sum(w["Miles"] for w in workouts)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Workouts", total_workouts)
    col2.metric("Minutes Exercised", f"{total_minutes:,}")
    col3.metric("Calories Burned", f"{total_calories:,}")
    col4.metric("Miles Completed", f"{total_miles:.1f}")

    st.markdown("---")

    st.subheader("Your Weekly Activity")

    today = date.today()
    weekly_steps = []

    for i in range(6, -1, -1):

        current_day = today - timedelta(days=i)

        steps = st.session_state.steps.get(
            str(current_day), 0
        )

        weekly_steps.append({
            "Day": current_day.strftime("%a"),
            "Steps": steps
        })

    weekly_df = pd.DataFrame(weekly_steps)

    st.bar_chart(
        weekly_df.set_index("Day"),
        y="Steps"
    )

    st.markdown("---")

    st.subheader("Recent Workouts")

    if workouts:

        recent = pd.DataFrame(workouts).tail(5)

        st.dataframe(
            recent,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "You haven't added any workouts yet. "
            "Go to Add Workout to get started!"
        )

    st.markdown("---")

    st.subheader("Today's Step Progress")

    today_steps = st.session_state.steps.get(str(today), 0)
    goal = st.session_state.daily_goal

    progress = min(today_steps / goal, 1.0)

    st.progress(progress)

    st.write(f"**{today_steps:,} / {goal:,} steps**")

    st.caption(
        f"{progress * 100:.1f}% of your daily goal completed."
    )


# -----------------------------
# ADD WORKOUT
# -----------------------------

elif page == "Add Workout":

    st.title("Add a Workout 🏋️")
    st.write("Record your exercise and keep track of your progress.")

    st.markdown("---")

    with st.form("workout_form"):

        exercise = st.selectbox(
            "Workout Type",
            [
                "Weight Training",
                "Running",
                "Walking",
                "Cycling",
                "Swimming",
                "Yoga",
                "Pilates",
                "Other"
            ]
        )

        workout_date = st.date_input(
            "Workout Date",
            value=date.today()
        )

        st.subheader("Workout Details")

        col1, col2 = st.columns(2)

        with col1:

            duration = st.number_input(
                "Duration (minutes)",
                min_value=1,
                max_value=600,
                value=30
            )

            miles = st.number_input(
                "Distance (miles)",
                min_value=0.0,
                max_value=200.0,
                value=0.0,
                step=0.1
            )

        with col2:

            calories = st.number_input(
                "Calories Burned",
                min_value=0,
                max_value=10000,
                value=200,
                step=25
            )

            intensity = st.select_slider(
                "Workout Intensity",
                options=[
                    "Light",
                    "Moderate",
                    "Hard",
                    "Very Hard"
                ]
            )

        st.markdown("---")

        st.subheader("Strength Training Details")

        sets = st.number_input(
            "Sets",
            min_value=0,
            max_value=100,
            value=0
        )

        reps = st.number_input(
            "Repetitions",
            min_value=0,
            max_value=500,
            value=0
        )

        weight = st.number_input(
            "Weight (lbs)",
            min_value=0.0,
            max_value=2000.0,
            value=0.0,
            step=5.0
        )

        notes = st.text_area(
            "Workout Notes",
            placeholder="How did your workout go?"
        )

        submitted = st.form_submit_button(
            "Save Workout",
            use_container_width=True
        )

        if submitted:

            workout = {
                "Exercise": exercise,
                "Date": workout_date,
                "Duration": int(duration),
                "Miles": float(miles),
                "Calories": int(calories),
                "Intensity": intensity,
                "Sets": int(sets),
                "Reps": int(reps),
                "Weight": float(weight),
                "Notes": notes
            }

            st.session_state.workouts.append(workout)

            st.success("Your workout was successfully saved! 🎉")


# -----------------------------
# WORKOUT HISTORY
# -----------------------------

elif page == "Workout History":

    st.title("Workout History 📅")
    st.write("Review your previous workouts and track your consistency.")

    st.markdown("---")

    workouts = st.session_state.workouts

    if workouts:

        df = pd.DataFrame(workouts)

        exercises = ["All"] + sorted(
            df["Exercise"].unique().tolist()
        )

        selected_exercise = st.selectbox(
            "Filter by Workout Type",
            exercises
        )

        if selected_exercise != "All":

            df = df[
                df["Exercise"] == selected_exercise
            ]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        st.subheader("Workout Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Miles",
            f"{df['Miles'].sum():.1f}"
        )

        col2.metric(
            "Total Calories",
            f"{df['Calories'].sum():,}"
        )

        col3.metric(
            "Total Minutes",
            f"{df['Duration'].sum():,}"
        )

        st.markdown("---")

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Workout History",
            data=csv,
            file_name="workout_history.csv",
            mime="text/csv"
        )

    else:

        st.info("No workouts recorded yet. Add your first workout!")


# -----------------------------
# STEP TRACKER
# -----------------------------

elif page == "Step Tracker":

    st.title("Daily Step Tracker 👟")
    st.write("Keep moving! Track your daily steps and work toward your goals.")

    st.markdown("---")

    st.subheader("Your Daily Goal")

    st.session_state.daily_goal = st.number_input(
        "Set your daily step goal",
        min_value=1000,
        max_value=50000,
        value=st.session_state.daily_goal,
        step=500
    )

    goal = st.session_state.daily_goal

    st.markdown("---")

    st.subheader("Log Your Steps")

    step_date = st.date_input(
        "Select Date",
        value=date.today(),
        key="step_date"
    )

    existing_steps = st.session_state.steps.get(
        str(step_date), 0
    )

    with st.form("step_form"):

        step_count = st.number_input(
            "How many steps did you walk?",
            min_value=0,
            max_value=100000,
            value=int(existing_steps),
            step=500
        )

        save_steps = st.form_submit_button(
            "Save Daily Steps",
            use_container_width=True
        )

        if save_steps:

            st.session_state.steps[str(step_date)] = int(step_count)

            st.success("Your steps were successfully saved! 🎉")

    st.markdown("---")

    st.subheader("Today's Progress")

    today = date.today()

    today_steps = st.session_state.steps.get(
        str(today), 0
    )

    progress = min(today_steps / goal, 1.0)

    remaining = max(goal - today_steps, 0)

    col1, col2 = st.columns(2)

    col1.metric(
        "Steps Today",
        f"{today_steps:,}"
    )

    col2.metric(
        "Steps Remaining",
        f"{remaining:,}"
    )

    st.progress(progress)

    st.write(
        f"**{progress * 100:.1f}% of your daily goal completed**"
    )

    if today_steps >= goal:

        st.success(
            "🏆 Congratulations! You've reached your daily step goal!"
        )

    else:

        st.info(
            f"Keep going! You have {remaining:,} steps left."
        )

    st.markdown("---")

    st.subheader("Your Weekly Step Progress")

    weekly_data = []

    for i in range(6, -1, -1):

        current_day = today - timedelta(days=i)

        steps = st.session_state.steps.get(
            str(current_day), 0
        )

        weekly_data.append({
            "Date": current_day.strftime("%a"),
            "Steps": steps
        })

    weekly_df = pd.DataFrame(weekly_data)

    st.bar_chart(
        weekly_df.set_index("Date"),
        y="Steps"
    )

    recorded_days = [
        st.session_state.steps[
            str(today - timedelta(days=i))
        ]
        for i in range(7)
        if str(today - timedelta(days=i))
        in st.session_state.steps
    ]

    weekly_average = (
        sum(recorded_days) / len(recorded_days)
        if recorded_days else 0
    )

    st.metric(
        "Average Daily Steps This Week",
        f"{weekly_average:,.0f}"
    )

    st.caption(
        "Average calculated from days with recorded step counts."
    )

    st.markdown("---")

    st.subheader("Daily Step History")

    if st.session_state.steps:

        history = pd.DataFrame([
            {"Date": d, "Steps": s}
            for d, s in sorted(
                st.session_state.steps.items(),
                reverse=True
            )
        ])

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Start logging your steps to see your history here!"
        )


# -----------------------------
# FOOTER
# -----------------------------

st.markdown("---")

st.markdown(
    "<p style='text-align:center; color:#94a3b8;'>"
    "FitTrack | Your Fitness Journey Starts Here 💚"
    "</p>",
    unsafe_allow_html=True
)
