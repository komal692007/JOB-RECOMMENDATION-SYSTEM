import streamlit as st
import pandas as pd
import pickle
import base64
import random

if "selected_job" not in st.session_state:
    st.session_state.selected_job = ""

if "saved_jobs" not in st.session_state:
    st.session_state.saved_jobs = []


# adding a background image
def add_bg():

    with open("images/bg.jpg", "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        .job-card{{
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:20px;
            background:rgba(255,255,255,0.08);
            backdrop-filter:blur(18px);
            border-radius:16px;
            padding:22px;
            margin:14px 0;
            border:1px solid rgba(255,255,255,0.15);
            color:white;
            min-height:120px;
            width:100%;
        }}

        .job-details{{
            display:flex;
            flex-direction:column;
            gap:10px;
            width:100%;
        }}

        .job-title{{
            font-size:20px;
            font-weight:700;
            color:#00d4ff;
            margin-bottom:6px;
            line-height:1.3;
            max-width:100%;
        }}

        .job-meta{{
            display:flex;
            flex-wrap:wrap;
            gap:18px;
            align-items:center;
        }}

        .job-meta span{{
            font-size:15px;
            white-space:nowrap;
            color:#f2f2f2;
        }}

        .job-action{{
            display:flex;
            align-items:center;
            justify-content:center;
            width:100%;
            min-width:110px;
        }}

        .job-action button{{
            background:#00d4ff;
            color:black;
            border:none;
            padding:10px 18px;
            border-radius:10px;
            font-weight:700;
            cursor:pointer;
            min-width:90px;
        }}

        .job-action button:hover{{
            background:white;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

add_bg()


@st.dialog("📝 Job Application Form")
def application_form():
    st.write(f"Applying for: **{st.session_state.selected_job}**")
    with st.form("job_application"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        resume = st.file_uploader(
            "Upload Resume",
            type=["pdf", "doc", "docx"]
        )
        cover = st.text_area("Cover Letter")
        submit = st.form_submit_button("Submit Application")
        if submit:
            if name and email and phone and resume:
                st.success("Application Submitted Successfully!")
                st.balloons()
            else:
                st.error("Please fill all the fields.")

@st.dialog("👤 My Profile")
def profile_form():

    st.subheader("Personal Information")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")

    st.subheader("Education")

    college = st.text_input("College")
    degree = st.selectbox(
        "Degree",
        ["B.Tech","BCA","MCA","MBA","M.Tech"]
    )

    branch = st.text_input("Branch")

    cgpa = st.number_input(
        "CGPA",
        0.0,
        10.0,
        step=0.1
    )

    st.subheader("Skills")

    skills = st.multiselect(
        "Skills",
        [
            "Python",
            "Java",
            "SQL",
            "Machine Learning",
            "React",
            "Power BI",
            "Excel"
        ]
    )

    st.subheader("Resume")

    resume = st.file_uploader(
        "Upload Resume",
        type=["pdf","doc","docx"]
    )

    if st.button("💾 Save Profile"):
        st.success("Profile Saved Successfully!")



@st.dialog("⚙️ Settings")
def settings_popup():

    if "settings" not in st.session_state:

        st.session_state.settings = {
            "theme": "Dark",
            "email_notifications": True,
            "job_alerts": True,
            "application_updates": True,
            "location": "Anywhere",
            "salary": "5-10 LPA",
            "job_type": ["Full-Time"],
            "skills": [],
            "language": "English",
            "profile_visible": True,
            "resume_visible": True,
            "recommendation_frequency": "Daily"
        }

    settings = st.session_state.settings

    tab1, tab2, tab3 = st.tabs(
        [
            "🎨 Appearance",
            "🔔 Notifications",
            "🔒 Privacy"
        ]
    )

    #######################################################
    # TAB 1
    #######################################################

    with tab1:

        st.subheader("Appearance")

        settings["theme"] = st.radio(
            "Application Theme",
            ["Dark", "Light"],
            index=0 if settings["theme"]=="Dark" else 1
        )


    #######################################################
    # TAB 2
    #######################################################

    with tab2:

        st.subheader("Notifications")

        settings["email_notifications"] = st.toggle(
            "Email Notifications",
            value=settings["email_notifications"]
        )

        settings["job_alerts"] = st.toggle(
            "Job Alerts",
            value=settings["job_alerts"]
        )

        settings["application_updates"] = st.toggle(
            "Application Updates",
            value=settings["application_updates"]
        )

        settings["recommendation_frequency"] = st.radio(
            "Recommendation Frequency",
            [
                "Daily",
                "Weekly",
                "Monthly"
            ],
            index=[
                "Daily",
                "Weekly",
                "Monthly"
            ].index(settings["recommendation_frequency"])
        )

    #######################################################
    # TAB 3
    #######################################################

    with tab3:

        st.subheader("Privacy")

        settings["profile_visible"] = st.checkbox(
            "Allow recruiters to view my profile",
            value=settings["profile_visible"]
        )

        settings["resume_visible"] = st.checkbox(
            "Allow recruiters to download my resume",
            value=settings["resume_visible"]
        )

        st.markdown("---")

        st.subheader("Account")

        if st.button("🔑 Change Password"):
            st.info("Password change feature coming soon.")

        if st.button("🚪 Logout"):
            st.success("Logged Out Successfully")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💾 Save Settings",
            use_container_width=True
        ):

            st.session_state.settings = settings

            st.success("Settings Saved Successfully!")

    with col2:

        if st.button(
            "🔄 Reset Settings",
            use_container_width=True
        ):

            del st.session_state.settings

            st.rerun()


# adding the sidebar
with st.sidebar:
    st.image("images/logo.png", width=70)
    st.markdown("JOB RECOMMENDER")
    st.markdown("---")
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    if st.button("🏠 Dashboard"):
        st.session_state.page = "Dashboard"
    if st.button("❤️ Saved Jobs"):
        st.session_state.page = "Saved Jobs"
    if st.button("👤 Profile"):
        profile_form()
    if st.button("⚙️ Settings"):
        settings_popup()


    if st.session_state.page == "Dashboard":
        st.title("Dashboard")
    if st.session_state.page == "Saved Jobs":
        st.title("Saved Jobs")
    if st.session_state.page == "Profile":
        st.title("Profile")
    if st.session_state.page == "Settings":
        st.title("Settings")


df = pickle.load(open('jk.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def recommendation(title):
    idx = df[df['Title']==title].index[0]
    idx = df.index.get_loc(idx)
    distances= sorted(list(enumerate(similarity[idx])),reverse=True,key=lambda x:x[1])[1:20]

    jobs = []
    for i in distances:
        jobs.append(df.iloc[i[0]].Title)

    return jobs


# WEBSITE
st.title('JOB RECOMMENDATION SYSTEM')
title = st.selectbox('SEARCH JOB', df['Title'])

# Applying filters
st.sidebar.header("🎯 FILTERS")

if "filters_active" not in st.session_state:
    st.session_state.filters_active = False
    st.session_state.filter_values = {
        "location": "All",
        "salary": "All",
        "jobtype": "All",
    }

filtered_df = df.copy()

location = st.sidebar.selectbox(
    "Location",
    ["All"] + sorted(filtered_df["City"].dropna().unique().tolist())
)
if location != "All":
    filtered_df = filtered_df[
        filtered_df["City"] == location
    ]

salary = st.sidebar.selectbox(
    "Salary",
    ["All", "0-5 LPA", "5-10 LPA", "10-15 LPA", "15+ LPA"]
)
job_type = st.sidebar.selectbox(
    "Job Type",
    ["All", "Full-Time", "Part-Time", "Internship", "Remote"]
)
if job_type != "All":
    filtered_df = filtered_df[
        filtered_df["Employment.Type"]
        .astype(str)
        .str.contains(job_type, case=False, na=False)
    ]


apply_clicked = st.sidebar.button("Apply Filters")
reset_clicked = st.sidebar.button("Reset Filters")

if apply_clicked:
    st.session_state.filters_active = True
    st.session_state.filter_values = {
        "location": location,
        "salary": salary,
        "jobtype": job_type,
    }
    st.sidebar.success("Filters applied")

if reset_clicked:
    st.session_state.filters_active = False
    st.session_state.filter_values = {
        "location": "All",
        "salary": "All",
        "jobtype": "All",
    }
    st.sidebar.info("Filters reset")

companies=["Microsoft","Google","Amazon","TCS","Infosys","Deloitte","IBM","Adobe","Oracle"]

locations=["Bangalore","Delhi","Hyderabad","Mumbai","Pune"]

jobs = recommendation(title)

recommended_df = df[df["Title"].isin(jobs)].copy()
progress_value = 0
if st.session_state.filters_active:
    filters = st.session_state.filter_values
    if filters["location"] != "All":
        recommended_df = recommended_df[recommended_df["City"].str.contains(filters["location"], case=False, na=False)]
    if filters["jobtype"] != "All":
        recommended_df = recommended_df[recommended_df["Employment.Type"].str.contains(filters["jobtype"], case=False, na=False)]
    if filters["salary"] != "All":
    # Convert Salary column to numeric
        recommended_df["Salary_Num"] = (
        recommended_df["Salary"]
        .astype(str)
        .str.extract(r'(\d+)', expand=False)
        .fillna(0)
        .astype(int)
    )

    if filters["salary"] == "0-5 LPA":
        recommended_df = recommended_df[
            (recommended_df["Salary_Num"] >= 0) &
            (recommended_df["Salary_Num"] <= 5)
        ]

    elif filters["salary"] == "5-10 LPA":
        recommended_df = recommended_df[
            (recommended_df["Salary_Num"] >= 5) &
            (recommended_df["Salary_Num"] <= 10)
        ]

    elif filters["salary"] == "10-15 LPA":
        recommended_df = recommended_df[
            (recommended_df["Salary_Num"] >= 10) &
            (recommended_df["Salary_Num"] <= 15)
        ]

    elif filters["salary"] == "15+ LPA":
        recommended_df = recommended_df[
            recommended_df["Salary_Num"] >= 15
        ]

if recommended_df.empty:
    st.warning("No jobs found for the selected filters.")

for index, row in recommended_df.iterrows():
    company_name = row.get("Company") or random.choice(companies)
    city_name = row.get("City") or random.choice(locations)
    salary_value = row.get("Salary")
    if not salary_value or str(salary_value).strip() == "":
        salary_value = f"{random.randint(6,22)} LPA"
    match = random.randint(82,99)

    with st.container():
        job_col, apply_col, save_col = st.columns([5,1,1])
        job_col.markdown(f"""
            <div class="job-card">
                <div class="job-details">
                    <div class="job-title">{row['Title']}</div>
                    <div class="job-meta">
                        <span>🏢 {company_name}</span>
                        <span>📍 {city_name}</span>
                        <span>💰 {salary_value}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with apply_col:
        if st.button("Apply", key=f"apply_{index}"):

            st.session_state.selected_job = row["Title"]
            application_form()

    with save_col:

        already_saved = any(
            job["Title"] == row["Title"]
            for job in st.session_state.saved_jobs
        )

        if already_saved:
            st.success("❤️ Saved")

        else:
            if st.button("❤️ Save", key=f"save_{index}"):

                st.session_state.saved_jobs.append({
                    "Title": row["Title"],
                    "Company": company_name,
                    "City": city_name,
                    "Salary": salary_value
                })

                st.success("Job Saved!")
                st.rerun()

if st.session_state.page == "Saved Jobs":
    st.title("❤️ Saved Jobs")
    if len(st.session_state.saved_jobs) == 0:
        st.info("No saved jobs yet.")
    else:
        for i, job in enumerate(st.session_state.saved_jobs):
            col1, col2 = st.columns([5,1])
            with col1:
                st.markdown(f"""
                <div class="job-card">
                    <div class="job-details">
                        <div class="job-title">{job['Title']}</div>
                        <div class="job-meta">
                            <span>🏢 {job['Company']}</span>
                            <span>📍 {job['City']}</span>
                            <span>💰 {job['Salary']}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("❌ Remove", key=f"remove_{i}"):
                    st.session_state.saved_jobs.pop(i)
                    st.success("Removed")
                    st.rerun()


st.markdown("---")

st.markdown(
"""
<center>
Made by Komal
</center>
""",
unsafe_allow_html=True)