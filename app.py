import streamlit as st
import pandas as pd
import sqlite3
import os
import json
from datetime import datetime

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Factory Compliance Dashboard",
    page_icon="🏭",
    layout="wide"
)

# ==================================================
# HEADER
# ==================================================

st.title("🏭 Factory Compliance Dashboard")

st.markdown("---")

# ==================================================
# DATABASE CONNECTION
# ==================================================

DB_PATH = "database/compliance.db"

def load_data():

    try:

        conn = sqlite3.connect(DB_PATH)

        df = pd.read_sql(
            "SELECT * FROM violations",
            conn
        )

        conn.close()

        return df

    except:

        return pd.DataFrame()

# ==================================================
# LOAD DATA
# ==================================================

df = load_data()

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("Filters")

severity_filter = st.sidebar.multiselect(

    "Severity",

    ["LOW","MEDIUM","HIGH","CRITICAL"]

)

behavior_filter = st.sidebar.multiselect(

    "Behavior",

    [
        "walkway_violation",
        "unauthorized_intervention",
        "opened_panel",
        "forklift_overload"
    ]
)

# ==================================================
# FILTER DATA
# ==================================================

filtered_df = df.copy()

if len(severity_filter) > 0:

    filtered_df = filtered_df[
        filtered_df["severity"].isin(
            severity_filter
        )
    ]

if len(behavior_filter) > 0:

    filtered_df = filtered_df[
        filtered_df["behavior_class"].isin(
            behavior_filter
        )
    ]

# ==================================================
# KPI SECTION
# ==================================================

st.subheader("System Statistics")

col1,col2,col3,col4 = st.columns(4)

total_events = len(df)

low_count = len(
    df[df["severity"]=="LOW"]
) if not df.empty else 0

medium_count = len(
    df[df["severity"]=="MEDIUM"]
) if not df.empty else 0

critical_count = len(
    df[df["severity"]=="CRITICAL"]
) if not df.empty else 0

col1.metric(
    "Total Events",
    total_events
)

col2.metric(
    "Low Risk",
    low_count
)

col3.metric(
    "Medium Risk",
    medium_count
)

col4.metric(
    "Critical Risk",
    critical_count
)

st.markdown("---")

# ==================================================
# TABS
# ==================================================

tab1,tab2,tab3 = st.tabs(

    [
        "📹 Live Feed",
        "🚨 Alert Timeline",
        "📋 Historical Logs"
    ]
)

# ==================================================
# TAB 1
# ==================================================

with tab1:

    st.subheader(
        "Live Feed Monitor"
    )

    video_path = "data/sample.mp4"

    if os.path.exists(video_path):

        st.video(video_path)

    else:

        st.warning(
            "Video not found"
        )

    st.markdown("### Current System Status")

    if not df.empty:

        latest = df.iloc[-1]

        severity = latest["severity"]

        if severity == "CRITICAL":

            st.error(
                f"CRITICAL ALERT : {latest['behavior_class']}"
            )

        elif severity == "HIGH":

            st.warning(
                f"HIGH ALERT : {latest['behavior_class']}"
            )

        elif severity == "MEDIUM":

            st.info(
                f"MEDIUM ALERT : {latest['behavior_class']}"
            )

        else:

            st.success(
                "System Safe"
            )

# ==================================================
# TAB 2
# ==================================================

with tab2:

    st.subheader(
        "Alert Timeline Stream"
    )

    if filtered_df.empty:

        st.info(
            "No Events Found"
        )

    else:

        timeline = filtered_df.sort_values(
            by="timestamp",
            ascending=False
        )

        for _,row in timeline.iterrows():

            severity = row["severity"]

            message = (
                f"{row['timestamp']} | "
                f"{row['behavior_class']} | "
                f"{severity}"
            )

            if severity == "CRITICAL":

                st.error(message)

            elif severity == "HIGH":

                st.warning(message)

            elif severity == "MEDIUM":

                st.info(message)

            else:

                st.success(message)

# ==================================================
# TAB 3
# ==================================================

with tab3:

    st.subheader(
        "Historical Logs"
    )

    if filtered_df.empty:

        st.warning(
            "No Data Available"
        )

    else:

        st.dataframe(

            filtered_df,

            use_container_width=True
        )

        csv = filtered_df.to_csv(
            index=False
        )

        st.download_button(

            label="Download CSV",

            data=csv,

            file_name="compliance_log.csv",

            mime="text/csv"
        )

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Factory Compliance & Alert Escalation System"
)