"""
Customer Support Analytics Dashboard
Interactive Streamlit dashboard for analyzing customer support tickets
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from utils import (
    load_data, 
    clean_data, 
    filter_data, 
    calculate_kpis,
    get_satisfaction_by_group,
    get_resolution_by_group,
    get_volume_by_group
)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Customer Support Analytics",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for responsive design across all devices
st.markdown("""
    <style>
    /* Main container responsive padding */
    .main {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Responsive metrics */
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Responsive headings */
    h1 {
        color: #1f77b4;
        padding-bottom: 1rem;
        font-size: clamp(1.5rem, 4vw, 2.5rem);
    }
    h2 {
        color: #2c3e50;
        padding-top: 1rem;
        padding-bottom: 0.5rem;
        font-size: clamp(1.2rem, 3vw, 1.8rem);
    }
    
    /* Ensure charts don't overflow */
    .js-plotly-plot {
        width: 100% !important;
    }
    
    /* Mobile optimizations */
    @media (max-width: 768px) {
        .main {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        .stMetric {
            padding: 10px;
        }
    }
    </style>
""", unsafe_allow_html=True)


# ============================================================================
# LOAD AND CLEAN DATA
# ============================================================================

df_raw = load_data()
df = clean_data(df_raw)


# ============================================================================
# SIDEBAR - FILTERS
# ============================================================================

st.sidebar.header("🔍 Filters")

# Date Range Filter
st.sidebar.subheader("📅 Date Range")
if "Date of Purchase" in df.columns and df["Date of Purchase"].notna().any():
    min_date = df["Date of Purchase"].min()
    max_date = df["Date of Purchase"].max()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="date_range"
    )
    
    # Handle single date selection
    if isinstance(date_range, tuple) and len(date_range) == 2:
        selected_date_range = date_range
    else:
        selected_date_range = None
else:
    selected_date_range = None
    st.sidebar.info("No date information available")

# Priority Filter
st.sidebar.subheader("⚡ Priority")
all_priorities = df["Ticket Priority"].dropna().unique().tolist()
selected_priorities = st.sidebar.multiselect(
    "Select Priorities",
    options=all_priorities,
    default=all_priorities,
    key="priorities"
)

# Channel Filter
st.sidebar.subheader("📞 Channel")
all_channels = df["Ticket Channel"].dropna().unique().tolist()
selected_channels = st.sidebar.multiselect(
    "Select Channels",
    options=all_channels,
    default=all_channels,
    key="channels"
)

# Status Filter
st.sidebar.subheader("📊 Status")
all_statuses = df["Ticket Status"].dropna().unique().tolist()
selected_statuses = st.sidebar.multiselect(
    "Select Statuses",
    options=all_statuses,
    default=all_statuses,
    key="statuses"
)

# Product Filter
st.sidebar.subheader("🛍️ Product")
all_products = df["Product Purchased"].dropna().unique().tolist()
selected_products = st.sidebar.multiselect(
    "Select Products",
    options=all_products,
    default=all_products,
    key="products"
)


# ============================================================================
# APPLY FILTERS
# ============================================================================

df_filtered = filter_data(
    df,
    date_range=selected_date_range,
    priorities=selected_priorities,
    channels=selected_channels,
    statuses=selected_statuses,
    products=selected_products
)


# ============================================================================
# HEADER
# ============================================================================

st.title("🎫 Customer Support Analytics Dashboard")
st.markdown(f"**Showing {len(df_filtered):,} of {len(df):,} tickets**")
st.markdown("---")


# ============================================================================
# KPI METRICS
# ============================================================================

kpis = calculate_kpis(df_filtered)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📊 Total Tickets",
        value=f"{kpis['total_tickets']:,}"
    )

with col2:
    avg_sat = kpis['avg_satisfaction']
    st.metric(
        label="⭐ Avg Satisfaction",
        value=f"{avg_sat:.2f}/5.0" if pd.notna(avg_sat) else "N/A"
    )

with col3:
    avg_res = kpis['avg_resolution_time']
    st.metric(
        label="⏱️ Avg Resolution Time",
        value=f"{avg_res:.1f}h" if pd.notna(avg_res) else "N/A"
    )

with col4:
    st.metric(
        label="🔓 Open Tickets",
        value=f"{kpis['open_tickets']:,}"
    )

st.markdown("---")


# ============================================================================
# SATISFACTION ANALYSIS
# ============================================================================

st.header("📈 Satisfaction Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("By Ticket Type")
    sat_by_type = get_satisfaction_by_group(df_filtered, "Ticket Type")
    
    if not sat_by_type.empty:
        fig_type = px.bar(
            sat_by_type,
            x="Ticket Type",
            y="Average Satisfaction",
            text="Average Satisfaction",
            color="Average Satisfaction",
            color_continuous_scale="RdYlGn",
            hover_data={"Count": True}
        )
        fig_type.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_type.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="Ticket Type",
            yaxis_title="Average Satisfaction Rating",
            autosize=True,
            margin=dict(l=20, r=20, t=40, b=80),
            font=dict(size=11)
        )
        st.plotly_chart(fig_type, use_container_width=True)
    else:
        st.info("No satisfaction data available for this filter")

with col2:
    st.subheader("By Priority")
    sat_by_priority = get_satisfaction_by_group(df_filtered, "Ticket Priority")
    
    if not sat_by_priority.empty:
        fig_priority = px.bar(
            sat_by_priority,
            x="Ticket Priority",
            y="Average Satisfaction",
            text="Average Satisfaction",
            color="Average Satisfaction",
            color_continuous_scale="RdYlGn",
            hover_data={"Count": True}
        )
        fig_priority.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_priority.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="Ticket Priority",
            yaxis_title="Average Satisfaction Rating",
            autosize=True,
            margin=dict(l=20, r=20, t=40, b=80),
            font=dict(size=11)
        )
        st.plotly_chart(fig_priority, use_container_width=True)
    else:
        st.info("No satisfaction data available for this filter")

# Satisfaction by Channel
st.subheader("By Channel")
sat_by_channel = get_satisfaction_by_group(df_filtered, "Ticket Channel")

if not sat_by_channel.empty:
    fig_channel = px.bar(
        sat_by_channel,
        x="Ticket Channel",
        y="Average Satisfaction",
        text="Average Satisfaction",
        color="Average Satisfaction",
        color_continuous_scale="RdYlGn",
        hover_data={"Count": True}
    )
    fig_channel.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_channel.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="Support Channel",
        yaxis_title="Average Satisfaction Rating",
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=80),
        font=dict(size=11)
    )
    st.plotly_chart(fig_channel, use_container_width=True)
else:
    st.info("No satisfaction data available for this filter")

st.markdown("---")


# ============================================================================
# RESOLUTION TIME ANALYSIS
# ============================================================================

st.header("⏱️ Resolution Time Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Resolution Time vs Satisfaction")
    
    # Filter for valid data
    df_scatter = df_filtered[
        df_filtered["Time to Resolution"].notna() & 
        df_filtered["Customer Satisfaction Rating"].notna() &
        (df_filtered["Time to Resolution"] > 0)
    ]
    
    if not df_scatter.empty:
        fig_scatter = px.scatter(
            df_scatter,
            x="Time to Resolution",
            y="Customer Satisfaction Rating",
            color="Ticket Priority",
            hover_data=["Ticket Status", "Ticket Channel", "Product Purchased"],
            opacity=0.6
        )
        fig_scatter.update_layout(
            height=400,
            xaxis_title="Time to Resolution (hours)",
            yaxis_title="Satisfaction Rating",
            autosize=True,
            margin=dict(l=20, r=20, t=40, b=80),
            font=dict(size=11)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("No resolution time data available for this filter")

with col2:
    st.subheader("Avg Resolution Time by Priority")
    res_by_priority = get_resolution_by_group(df_filtered, "Ticket Priority")
    
    if not res_by_priority.empty:
        fig_res_priority = px.bar(
            res_by_priority,
            x="Ticket Priority",
            y="Average Resolution Time",
            text="Average Resolution Time",
            color="Average Resolution Time",
            color_continuous_scale="Reds_r",
            hover_data={"Count": True}
        )
        fig_res_priority.update_traces(texttemplate='%{text:.1f}h', textposition='outside')
        fig_res_priority.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="Ticket Priority",
            yaxis_title="Average Resolution Time (hours)",
            autosize=True,
            margin=dict(l=20, r=20, t=40, b=80),
            font=dict(size=11)
        )
        st.plotly_chart(fig_res_priority, use_container_width=True)
    else:
        st.info("No resolution time data available for this filter")

st.markdown("---")


# ============================================================================
# CHANNEL & VOLUME ANALYSIS
# ============================================================================

st.header("📊 Channel & Volume Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Ticket Volume by Channel")
    vol_by_channel = get_volume_by_group(df_filtered, "Ticket Channel")
    
    if not vol_by_channel.empty:
        fig_vol_channel = px.pie(
            vol_by_channel,
            names="Ticket Channel",
            values="Count",
            hole=0.4
        )
        fig_vol_channel.update_traces(textposition='inside', textinfo='percent+label')
        fig_vol_channel.update_layout(
            height=400,
            autosize=True,
            margin=dict(l=20, r=20, t=40, b=20),
            font=dict(size=11)
        )
        st.plotly_chart(fig_vol_channel, use_container_width=True)
    else:
        st.info("No channel data available")

with col2:
    st.subheader("Ticket Volume by Status")
    vol_by_status = get_volume_by_group(df_filtered, "Ticket Status")
    
    if not vol_by_status.empty:
        fig_vol_status = px.bar(
            vol_by_status,
            x="Ticket Status",
            y="Count",
            text="Count",
            color="Ticket Status"
        )
        fig_vol_status.update_traces(textposition='outside')
        fig_vol_status.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="Status",
            yaxis_title="Number of Tickets",
            autosize=True,
            margin=dict(l=20, r=20, t=40, b=80),
            font=dict(size=11)
        )
        st.plotly_chart(fig_vol_status, use_container_width=True)
    else:
        st.info("No status data available")

st.markdown("---")


# ============================================================================
# DATA EXPLORER
# ============================================================================

with st.expander("🔍 Data Explorer - View Filtered Data"):
    st.subheader("Filtered Ticket Data")
    
    # Select columns to display
    display_columns = [
        "Ticket ID", "Customer Name", "Product Purchased", 
        "Ticket Type", "Ticket Priority", "Ticket Status", 
        "Ticket Channel", "Customer Satisfaction Rating", 
        "Time to Resolution"
    ]
    
    # Filter to only existing columns
    available_columns = [col for col in display_columns if col in df_filtered.columns]
    
    st.dataframe(
        df_filtered[available_columns],
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name=f"customer_support_tickets_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
