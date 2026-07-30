import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG

st.set_page_config(
    page_title="PMO Command Center",
    page_icon="📊",
    layout="wide"
)

# LOAD DATA

projects = pd.read_csv("Data/projects.csv")
raid = pd.read_csv("Data/raid_log.csv")

# SIDEBAR

st.sidebar.title("📂 PMO Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "RAID Log",
        "Project Health",
        "Resource Allocation",
        "Executive Summary"
    ]
)

# DASHBOARD

if page == "Dashboard":

    st.title("📊 PMO Command Center")
    st.subheader("AI-Powered Project Portfolio Dashboard")

    st.divider()

    total_projects = len(projects)
    active = len(projects[projects["Status"]=="Active"])
    completed = len(projects[projects["Status"]=="Completed"])
    delayed = len(projects[projects["Status"]=="Delayed"])

    budget = projects["Budget"].sum()
    progress = round(projects["Progress"].mean(),1)

    c1,c2,c3,c4,c5,c6 = st.columns(6)

    c1.metric("Projects", total_projects)
    c2.metric("Active", active)
    c3.metric("Completed", completed)
    c4.metric("Delayed", delayed)
    c5.metric("Budget", f"${budget:,}")
    c6.metric("Avg Progress", f"{progress}%")

    st.divider()

    col1,col2 = st.columns(2)

    with col1:

        fig = px.pie(
            projects,
            names="Status",
            title="Project Status Distribution"
        )

        st.plotly_chart(fig,use_container_width=True)

    with col2:

        fig2 = px.bar(
            projects,
            x="Project_Name",
            y="Progress",
            color="Status",
            title="Project Progress"
        )

        st.plotly_chart(fig2,use_container_width=True)

    st.divider()

    fig3 = px.bar(
        projects,
        x="Project_Name",
        y="Budget",
        color="Department",
        title="Project Budget"
    )

    st.plotly_chart(fig3,use_container_width=True)

    st.divider()

    st.subheader("📁 Project Portfolio")

    st.dataframe(projects,use_container_width=True)

# RAID LOG

elif page == "RAID Log":

    st.title("⚠️ RAID Register")

    st.subheader("Risks • Issues • Assumptions • Dependencies")

    st.dataframe(raid,use_container_width=True)

# PROJECT HEALTH

elif page == "Project Health":

    st.title("🟢 Project Health Dashboard")

    health = projects[["Project_Name","Status","Progress"]].copy()

    def health_status(row):

        if row["Status"]=="Completed":
            return "🟢 Green"

        elif row["Progress"]>=70:
            return "🟢 Green"

        elif row["Progress"]>=40:
            return "🟡 Amber"

        else:
            return "🔴 Red"

    health["Health"] = health.apply(health_status,axis=1)

    st.dataframe(health,use_container_width=True)

# RESOURCE ALLOCATION

elif page == "Resource Allocation":

    st.title("👥 Resource Allocation")

    st.info("This module will be added next.")

# EXECUTIVE SUMMARY

elif page == "Executive Summary":

    st.title("🤖 AI Executive Summary")

    st.success("""
### Weekly Executive Summary

• 10 Projects are being monitored.

• 5 Projects are Active.

• 3 Projects require immediate attention.

• Budget utilization is within expected limits.

Recommendation:

Continue monitoring delayed projects and prioritize vendor-related risks.
""")