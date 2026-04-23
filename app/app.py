import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------
# Page Config
# -----------------------------------

st.set_page_config(
    page_title="Customer Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------
# Custom Title
# -----------------------------------

st.markdown("""
# 📊 Customer Intelligence Dashboard
### Revenue Optimization & Customer Segmentation System
---
""")

# -----------------------------------
# Load Data
# -----------------------------------

df = pd.read_csv("../data/processed/cleaned_data.csv")
rfm = pd.read_csv("../data/processed/rfm_data.csv")

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

# -----------------------------------
# Sidebar Filters
# -----------------------------------

st.sidebar.header("🔍 Filters")

selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df["Country"].dropna().unique().tolist())
)

if selected_country != "All":
    df = df[df["Country"] == selected_country]

# -----------------------------------
# KPI Section
# -----------------------------------

total_revenue = df["TotalPrice"].sum()
total_customers = df["CustomerID"].nunique()
total_orders = df["InvoiceNo"].nunique()
best_customers = (rfm["Segment"] == "Best Customers").sum()

st.subheader("📌 Key Business Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
col2.metric("👥 Total Customers", total_customers)
col3.metric("🛒 Total Orders", total_orders)
col4.metric("🏆 Best Customers", best_customers)

st.markdown("---")

# -----------------------------------
# Monthly Sales Trend
# -----------------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Monthly Revenue Trend")

    monthly_sales = (
        df.groupby("Month")["TotalPrice"]
        .sum()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(
        data=monthly_sales,
        x="Month",
        y="TotalPrice",
        ax=ax
    )
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    st.subheader("🌍 Top 10 Countries")

    country_sales = (
        df.groupby("Country")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    country_sales.plot(kind="bar", ax=ax)
    st.pyplot(fig)

st.markdown("---")

# -----------------------------------
# Bottom Charts
# -----------------------------------

col3, col4 = st.columns(2)

with col3:
    st.subheader("👥 Customer Segments")

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.countplot(
        x="Segment",
        data=rfm,
        ax=ax
    )
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col4:
    st.subheader("🏆 Top 10 Customers")

    top_customers = (
        df.groupby("CustomerID")["TotalPrice"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    top_customers.plot(kind="bar", ax=ax)
    st.pyplot(fig)

st.markdown("---")
st.success("Dashboard Loaded Successfully ✅")