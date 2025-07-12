import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv("dashboard/bike.csv")

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("🚲 Bike Sharing Dashboard")
st.markdown("Visualisasi data peminjaman sepeda berdasarkan data harian dan jam.")

# ==========================
# 1. Bar chart: Casual vs Registered User per Hari
# ==========================
st.subheader("📊 Daily Casual and Registered Users")
daily = df.groupby("day")[["casual_user", "registered_user"]].sum().reset_index()
daily = pd.melt(daily, id_vars="day", value_vars=["casual_user", "registered_user"], var_name="variable", value_name="value")

fig1 = px.bar(
    daily,
    x="day",
    y="value",
    color="variable",
    barmode="group",
    title="Daily Casual Users and Registered Users",
    labels={"value": "Jumlah Pengguna", "day": "Hari", "variable": "Tipe Pengguna"},
    color_discrete_sequence=px.colors.qualitative.Set2,
    width=800,
    height=500,
)
fig1.update_traces(hovertemplate="Day: %{x}<br>Tipe: %{legendgroup}<br>Jumlah: %{y:,}")
st.plotly_chart(fig1, use_container_width=True)

# ==========================
# 2. Comparison Total User by Season & Weather
# ==========================
st.subheader("🌦️ Comparison of Total User by Season and Weather")
compare = pd.concat([
    df.groupby("season")["total_user"].sum().reset_index().assign(type="Season").rename(columns={"season": "category"}),
    df.groupby("weather")["total_user"].sum().reset_index().assign(type="Weather").rename(columns={"weather": "category"}),
])

fig2 = px.bar(
    compare,
    x="category",
    y="total_user",
    color="type",
    text="total_user",
    barmode="group",
    labels={"category": "Category", "total_user": "Total User", "type": "Tipe"},
    title="Comparison of Total User by Season and Weather",
    color_discrete_sequence=px.colors.qualitative.Set2,
    width=1000,
    height=500
)
fig2.update_traces(
    texttemplate="%{text:,}",
    textposition="outside",
    hovertemplate="Kategori: %{x}<br>Tipe: %{legendgroup}<br>Total: %{y:,}"
)
st.plotly_chart(fig2, use_container_width=True)

# ==========================
# 3. Interactive Usage per Hour
# ==========================
st.subheader("⏰ Interactive Average Number of Bicycle Users per Hour")
hourly_usage = df.groupby(df.index % 24).agg({
    "casual_user": "mean",
    "registered_user": "mean",
    "total_user": "mean"
}).reset_index().rename(columns={"index": "hour"})

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=hourly_usage.index, y=hourly_usage["total_user"], mode="lines+markers", name="Total"))
fig3.add_trace(go.Scatter(x=hourly_usage.index, y=hourly_usage["casual_user"], mode="lines+markers", name="Casual"))
fig3.add_trace(go.Scatter(x=hourly_usage.index, y=hourly_usage["registered_user"], mode="lines+markers", name="Registered"))
fig3.update_layout(
    title="Interactive Average Number of Bicycle Users per Hour",
    xaxis_title="Jam",
    yaxis_title="Jumlah",
    xaxis=dict(tickmode='linear', tickvals=list(range(0, 24))),
    template="plotly_white",
    width=1000,
    height=500
)
st.plotly_chart(fig3, use_container_width=True)

# ==========================
# 4. Avg Rentals per Season
# ==========================
st.subheader("🍂 Rata-rata Peminjaman Sepeda per Musim")
avg_rentals_season = df.groupby("season")[["total_user"]].mean().reset_index().rename(columns={"total_user": "Average Rentals"})

fig4 = px.bar(
    avg_rentals_season,
    x="season",
    y="Average Rentals",
    color="season",
    text="Average Rentals",
    title="Rata-rata Peminjaman Sepeda per Musim",
    color_discrete_sequence=px.colors.qualitative.Plotly,
    width=600,
    height=500
)
fig4.update_traces(
    texttemplate="%{text:.0f}",
    textposition="outside",
    hovertemplate="Musim: %{x}<br>Rata-rata: %{y:.2f}"
)
st.plotly_chart(fig4, use_container_width=False)

# ==========================
# 5. Monthly Average Number Users
# ==========================
st.subheader("📅 Monthly Average Number Users")
month_mapping = {
    'january': 1, 'february': 2, 'march': 3, 'april': 4,
    'may': 5, 'june': 6, 'july': 7, 'august': 8,
    'september': 9, 'october': 10, 'november': 11, 'december': 12
}

monthly_usage = df.groupby("month")[["total_user"]].mean().reset_index()
monthly_usage["month_num"] = monthly_usage["month"].map(month_mapping)
monthly_usage = monthly_usage.sort_values("month_num")

fig5 = px.bar(
    monthly_usage,
    x="month",
    y="total_user",
    color="month_num",
    color_continuous_scale="Viridis",
    text="total_user",
    labels={"month": "Month", "total_user": "Users Average Number"},
    title="Monthly Average Number Users",
    width=900,
    height=500
)
fig5.update_layout(template="plotly_white", coloraxis_showscale=False)
fig5.update_traces(
    texttemplate="%{text:.0f}",
    textposition="outside",
    hovertemplate="Month: %{x}<br>User: %{y:.0f}"
)
st.plotly_chart(fig5, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Created with ❤️ using Streamlit & Plotly. Data source: `bike.csv`.")
