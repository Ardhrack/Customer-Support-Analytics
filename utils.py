"""
Utility functions for Customer Support Ticket Analysis
"""
import pandas as pd
from pathlib import Path
import streamlit as st


@st.cache_data
def load_data():
    """
    Load customer support tickets data from CSV file.
    Uses Streamlit caching for performance.
    
    Returns:
        pd.DataFrame: Raw customer support tickets data
    """
    BASE_DIR = Path(__file__).resolve().parent
    csv_path = BASE_DIR / "data" / "customer_support_tickets.csv"
    
    try:
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        st.error(f"❌ Data file not found at: {csv_path}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()


def clean_data(df):
    """
    Clean and prepare the data for analysis.
    
    Args:
        df (pd.DataFrame): Raw dataframe
        
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    df_clean = df.copy()
    
    # Convert satisfaction rating to numeric
    df_clean["Customer Satisfaction Rating"] = pd.to_numeric(
        df_clean["Customer Satisfaction Rating"], 
        errors="coerce"
    )
    
    # Convert date columns to datetime
    if "Date of Purchase" in df_clean.columns:
        df_clean["Date of Purchase"] = pd.to_datetime(
            df_clean["Date of Purchase"], 
            errors="coerce"
        )
    
    # Convert timestamp columns to datetime
    if "First Response Time" in df_clean.columns:
        df_clean["First Response Time"] = pd.to_datetime(
            df_clean["First Response Time"], 
            errors="coerce"
        )
    
    # CRITICAL FIX: Time to Resolution is a timestamp, not numeric hours
    # We need to calculate the actual resolution duration
    if "Time to Resolution" in df_clean.columns:
        # Convert to datetime first
        df_clean["Time to Resolution Timestamp"] = pd.to_datetime(
            df_clean["Time to Resolution"], 
            errors="coerce"
        )
        
        # Calculate actual resolution time in hours
        # Resolution Time = Time to Resolution - First Response Time
        if "First Response Time" in df_clean.columns:
            time_diff = (
                df_clean["Time to Resolution Timestamp"] - 
                df_clean["First Response Time"]
            )
            # Convert to hours and ensure positive values only
            df_clean["Time to Resolution"] = time_diff.dt.total_seconds() / 3600
            
            # Filter out negative or zero values (data quality issues)
            df_clean.loc[df_clean["Time to Resolution"] <= 0, "Time to Resolution"] = pd.NA
        else:
            # If no First Response Time, we can't calculate duration
            df_clean["Time to Resolution"] = pd.NA
    
    return df_clean


def filter_data(df, date_range=None, priorities=None, channels=None, 
                statuses=None, products=None):
    """
    Filter dataframe based on user selections.
    
    Args:
        df (pd.DataFrame): Dataframe to filter
        date_range (tuple): Start and end dates
        priorities (list): List of ticket priorities
        channels (list): List of ticket channels
        statuses (list): List of ticket statuses
        products (list): List of products
        
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    df_filtered = df.copy()
    
    # Date filter
    if date_range and "Date of Purchase" in df.columns:
        start_date, end_date = date_range
        df_filtered = df_filtered[
            (df_filtered["Date of Purchase"] >= pd.Timestamp(start_date)) &
            (df_filtered["Date of Purchase"] <= pd.Timestamp(end_date))
        ]
    
    # Priority filter
    if priorities and len(priorities) > 0:
        df_filtered = df_filtered[df_filtered["Ticket Priority"].isin(priorities)]
    
    # Channel filter
    if channels and len(channels) > 0:
        df_filtered = df_filtered[df_filtered["Ticket Channel"].isin(channels)]
    
    # Status filter
    if statuses and len(statuses) > 0:
        df_filtered = df_filtered[df_filtered["Ticket Status"].isin(statuses)]
    
    # Product filter
    if products and len(products) > 0:
        df_filtered = df_filtered[df_filtered["Product Purchased"].isin(products)]
    
    return df_filtered


def calculate_kpis(df):
    """
    Calculate key performance indicators.
    
    Args:
        df (pd.DataFrame): Dataframe to analyze
        
    Returns:
        dict: Dictionary of KPI values
    """
    kpis = {
        "total_tickets": len(df),
        "avg_satisfaction": df["Customer Satisfaction Rating"].mean(),
        "avg_resolution_time": df["Time to Resolution"].mean(),
        "open_tickets": len(df[df["Ticket Status"] == "Open"]) if "Open" in df["Ticket Status"].values else 0,
        "closed_tickets": len(df[df["Ticket Status"] == "Closed"]) if "Closed" in df["Ticket Status"].values else 0,
    }
    
    return kpis


def get_satisfaction_by_group(df, group_column):
    """
    Calculate average satisfaction rating grouped by a column.
    
    Args:
        df (pd.DataFrame): Dataframe to analyze
        group_column (str): Column name to group by
        
    Returns:
        pd.DataFrame: Grouped satisfaction data
    """
    # Filter out rows with missing satisfaction ratings
    df_valid = df[df["Customer Satisfaction Rating"].notna()]
    
    if len(df_valid) == 0:
        return pd.DataFrame()
    
    grouped = (
        df_valid.groupby(group_column, dropna=False)["Customer Satisfaction Rating"]
        .agg(["mean", "count"])
        .reset_index()
        .sort_values("mean", ascending=False)
    )
    
    grouped.columns = [group_column, "Average Satisfaction", "Count"]
    
    return grouped


def get_resolution_by_group(df, group_column):
    """
    Calculate average resolution time grouped by a column.
    
    Args:
        df (pd.DataFrame): Dataframe to analyze
        group_column (str): Column name to group by
        
    Returns:
        pd.DataFrame: Grouped resolution time data
    """
    # Filter out rows with missing or zero resolution times
    df_valid = df[
        df["Time to Resolution"].notna() & 
        (df["Time to Resolution"] > 0)
    ]
    
    if len(df_valid) == 0:
        return pd.DataFrame()
    
    grouped = (
        df_valid.groupby(group_column, dropna=False)["Time to Resolution"]
        .agg(["mean", "count"])
        .reset_index()
        .sort_values("mean", ascending=True)
    )
    
    grouped.columns = [group_column, "Average Resolution Time", "Count"]
    
    return grouped


def get_volume_by_group(df, group_column):
    """
    Calculate ticket volume grouped by a column.
    
    Args:
        df (pd.DataFrame): Dataframe to analyze
        group_column (str): Column name to group by
        
    Returns:
        pd.DataFrame: Grouped volume data
    """
    volume = (
        df[group_column]
        .value_counts(dropna=False)
        .reset_index()
    )
    
    volume.columns = [group_column, "Count"]
    
    return volume
