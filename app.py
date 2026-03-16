import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Electude Africa Analytics",
    layout="wide"
)

st.title("🌍 Electude Africa TVET Analytics Dashboard")

# ----------------------------
# Load Data
# ----------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("electude_data.csv")
    return df

@st.cache_data
def load_survey_data():
    try:
        # Assumes survey data has 'Institution', 'Satisfaction Score', 'Feedback'
        survey_df = pd.read_csv("survey_data.csv")
        return survey_df
    except FileNotFoundError:
        return pd.DataFrame()

df = load_data()
survey_df = load_survey_data()

# ----------------------------
# Data Cleaning
# ----------------------------

df["Institution"] = df["Institution"].fillna(method="ffill")
df["Electude Domain"] = df["Electude Domain"].fillna(method="ffill")
df["Language"] = df["Language"].fillna(method="ffill")

df["Number of Students"] = pd.to_numeric(
    df["Number of Students"], errors="coerce"
).fillna(0)

df["Teacher / Trainer"] = df["Teacher / Trainer"].fillna("Unknown")

# Extract country automatically
df["Country"] = df["Institution"].str.split("-").str[-1]

# ----------------------------
# Sidebar Filters
# ----------------------------

st.sidebar.header("Filters")

language_filter = st.sidebar.multiselect(
    "Language",
    df["Language"].unique(),
    default=df["Language"].unique()
)

country_filter = st.sidebar.multiselect(
    "Country",
    df["Country"].unique(),
    default=df["Country"].unique()
)

filtered = df[
    (df["Language"].isin(language_filter)) &
    (df["Country"].isin(country_filter))
]

# ----------------------------
# Metrics
# ----------------------------

total_students = int(filtered["Number of Students"].sum())
total_teachers = filtered["Teacher / Trainer"].count()
institutions = filtered["Institution"].nunique()

avg_students = round(total_students / institutions, 1) if institutions > 0 else 0

avg_satisfaction = "N/A"
if not survey_df.empty:
    # Filter survey data based on the main filters as well
    filtered_survey = survey_df[survey_df['Institution'].isin(filtered['Institution'].unique())]
    if not filtered_survey.empty and "Satisfaction Score" in filtered_survey.columns:
        avg_satisfaction_score = filtered_survey["Satisfaction Score"].mean()
        avg_satisfaction = f"{avg_satisfaction_score:.2f} / 5"

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Students", total_students)
c2.metric("Teachers", total_teachers)
c3.metric("Institutions", institutions)
c4.metric("Avg Students / Institution", avg_students)
c5.metric("Avg. Satisfaction", avg_satisfaction)

st.divider()

# ----------------------------
# Charts
# ----------------------------

col1, col2 = st.columns(2)

students_inst = (
    filtered.groupby("Institution")["Number of Students"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    students_inst,
    x="Institution",
    y="Number of Students",
    title="Students per Institution",
    labels={'Number of Students': 'Number of Students', 'Institution': 'Institution Name'},
    template="plotly_white",
    color="Number of Students"
)

col1.plotly_chart(fig1, use_container_width=True)

lang_dist = (
    filtered.groupby("Language")
    .size()
    .reset_index(name="Count")
)

fig2 = px.pie(
    lang_dist,
    names="Language",
    values="Count",
    title="Language Distribution",
    template="plotly_white",
    color="Language"
)

col2.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# Top Institutions
# ----------------------------

st.subheader("🏫 Top Institutions by Students")

top_inst = students_inst.sort_values(
    by="Number of Students",
    ascending=False
).head(10)

fig3 = px.bar(
    top_inst,
    x="Number of Students",
    y="Institution",
    orientation="h",
    title="Top 10 Institutions by Number of Students",
    template="plotly_white",
    color="Number of Students"
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# Teacher Distribution
# ----------------------------

teachers_inst = (
    filtered.groupby("Institution")["Teacher / Trainer"]
    .count()
    .reset_index(name="Teachers")
)

fig4 = px.bar(
    teachers_inst,
    x="Institution",
    y="Teachers",
    title="Teachers per Institution",
    template="plotly_white",
    color="Teachers"
)

st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ----------------------------
# User Satisfaction Analysis
# ----------------------------

st.subheader("⭐ User Satisfaction Analysis")

if 'filtered_survey' in locals() and not filtered_survey.empty:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("#### Satisfaction Score by Institution")
        satisfaction_by_inst = (
            filtered_survey.groupby("Institution")["Satisfaction Score"]
            .mean()
            .sort_values(ascending=True)
            .reset_index()
        )

        fig5 = px.bar(
            satisfaction_by_inst,
            x="Satisfaction Score",
            y="Institution",
            orientation="h",
            title="Average Satisfaction Score per Institution",
            template="plotly_white",
            color="Satisfaction Score",
            color_continuous_scale=px.colors.sequential.Greens,
            range_color=[1,5]
        )
        st.plotly_chart(fig5, use_container_width=True)

    with col2:
        st.write("#### Score Distribution")
        fig6 = px.histogram(
            filtered_survey,
            x="Satisfaction Score",
            title="Distribution of All Scores",
            template="plotly_white",
            color_discrete_sequence=['#2ca02c']
        )
        st.plotly_chart(fig6, use_container_width=True)

    st.write("#### Qualitative Feedback Browser")
    st.dataframe(filtered_survey[['Institution', 'Feedback', 'Satisfaction Score']], use_container_width=True)
else:
    st.warning("No survey data found or data does not match filters. Please add a `survey_data.csv` file to the project directory.")

# ----------------------------
# AI Insights
# ----------------------------

st.subheader("🤖 AI Data Insights")

top_school = top_inst.iloc[0]["Institution"]
top_students = int(top_inst.iloc[0]["Number of Students"])

most_language = lang_dist.sort_values(
    by="Count",
    ascending=False
).iloc[0]["Language"]

st.info(f"""
📊 **Key Insights**

• The institution with the highest number of students is **{top_school}** with **{top_students} students**

• The most used learning language is **{most_language}**

• There are **{institutions} active institutions** in the Electude Africa network.

• The network currently serves **{total_students} students**.
""")

# ----------------------------
# Teacher Directory
# ----------------------------

st.subheader("👨‍🏫 Teacher Directory")

search = st.text_input("Search teacher")

directory = filtered[
    filtered["Teacher / Trainer"].str.contains(
        search,
        case=False,
        na=False
    )
]

st.dataframe(
    directory[
        [
            "Institution",
            "Teacher / Trainer",
            "EMAIL",
            "Phone number",
            "Number of Students"
        ]
    ],
    use_container_width=True
)

# ----------------------------
# Data Quality Panel
# ----------------------------

st.subheader("🧹 Data Quality")

missing_email = df["EMAIL"].isna().sum()
missing_phone = df["Phone number"].isna().sum()

q1, q2 = st.columns(2)

q1.metric("Missing Emails", missing_email)
q2.metric("Missing Phone Numbers", missing_phone)

# ----------------------------
# Download Data
# ----------------------------

st.download_button(
    label="Download Clean Data",
    data=filtered.to_csv(index=False),
    file_name="electude_clean_data.csv",
    mime="text/csv"
)