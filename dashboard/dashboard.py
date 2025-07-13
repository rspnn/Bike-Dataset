
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================
# Load & Prepare Data
# =====================
df = pd.read_csv("./bike.csv")
df["date"] = pd.to_datetime(df["date"])
df["day_name"] = df["date"].dt.day_name().str.lower()
df["month_name"] = df["date"].dt.month_name().str.lower()
df["month_num"] = df["date"].dt.month

month_order = ['january','february','march','april','may','june','july','august','september','october','november','december']
day_order = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']

# =====================
# Sidebar Filter
# =====================
st.set_page_config(page_title="Bike Dashboard", layout="wide")
st.sidebar.header("🔽 Filter")
df["year"] = df["date"].dt.year
selected_year = st.sidebar.selectbox("Pilih Tahun", options=["All", 2011, 2012])

if selected_year != "All":
    df = df[df["year"] == selected_year]

# =====================
# Header
# =====================
st.title("🚴 Bike Sharing Dashboard")
st.caption("Data visualisasi penggunaan sepeda berdasarkan dataset `bike.csv`.")

# =====================
# Statistik Ringkas
# =====================
st.subheader("📌 Statistik Ringkas Pengguna Sepeda")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Users", f"{df['total_user'].sum():,}")
    st.metric("Average Daily Users", f"{df['total_user'].mean():,.2f}")
with col2:
    st.metric("Max Daily Users", f"{df['total_user'].max():,}")
    st.metric("Min Daily Users", f"{df['total_user'].min():,}")
with col3:
    st.metric("Total Casual Users", f"{df['casual_user'].sum():,}")
    st.metric("Total Registered Users", f"{df['registered_user'].sum():,}")

st.markdown("---")

# =====================
# 1. Total Users Daily & Monthly
# =====================
st.subheader("1️⃣ Total Casual vs Registered Users (Daily & Monthly)")
st.markdown("Visualisasi ini membandingkan jumlah total pengguna casual dan registered berdasarkan hari dan bulan.")

daily_sum = df.groupby("day_name")[["casual_user", "registered_user"]].sum().reset_index()
daily_sum["day_name"] = pd.Categorical(daily_sum["day_name"], categories=day_order, ordered=True)
daily_sum = daily_sum.sort_values("day_name")

monthly_sum = df.groupby("month_name")[["casual_user", "registered_user"]].sum().reset_index()
monthly_sum["month_num"] = monthly_sum["month_name"].map({m: i for i, m in enumerate(month_order, 1)})
monthly_sum = monthly_sum.sort_values("month_num")

col1, col2 = st.columns(2)
with col1:
    fig1 = px.bar(daily_sum.melt(id_vars="day_name", var_name="Tipe", value_name="Total"),
                  x="day_name", y="Total", color="Tipe", barmode="group",
                  color_discrete_sequence=px.colors.sequential.Tealgrn,
                  title="Total Casual vs Registered per Day")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(monthly_sum.melt(id_vars=["month_name", "month_num"], var_name="Tipe", value_name="Total"),
                  x="month_name", y="Total", color="Tipe", barmode="group",
                  color_discrete_sequence=px.colors.sequential.Tealgrn,
                  title="Total Casual vs Registered per Month")
    st.plotly_chart(fig2, use_container_width=True)

# =====================
# 2. Season & Weather Visualizations
# =====================
st.subheader("2️⃣ Rata-rata Peminjaman dan Komposisi Total Pengguna")
st.markdown("Empat grafik ini menunjukkan rata-rata dan total penggunaan sepeda berdasarkan musim dan kondisi cuaca.")

season_avg = df.groupby("season")[["total_user"]].mean().reset_index()
weather_avg = df.groupby("weather")[["total_user"]].mean().reset_index()
season_total = df.groupby("season")["total_user"].sum().reset_index()
weather_total = df.groupby("weather")["total_user"].sum().reset_index()

fig3 = px.bar(season_avg, x="season", y="total_user", color="season", text="total_user",
              color_discrete_sequence=px.colors.sequential.Tealgrn,
              title="Rata-rata Pengguna per Musim")
fig3.update_traces(texttemplate="%{text:.0f}", textposition="outside")

fig4 = px.bar(weather_avg, x="weather", y="total_user", color="weather", text="total_user",
              color_discrete_sequence=px.colors.sequential.Tealgrn,
              title="Rata-rata Pengguna per Cuaca")
fig4.update_traces(texttemplate="%{text:.0f}", textposition="outside")

fig5 = px.pie(season_total, names="season", values="total_user", hole=0.3,
              color_discrete_sequence=px.colors.sequential.Tealgrn,
              title="Total Users by Season")

fig6 = px.pie(weather_total, names="weather", values="total_user", hole=0.3,
              color_discrete_sequence=px.colors.sequential.Cividis,
              title="Total Users by Weather")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.plotly_chart(fig3, use_container_width=True)
with col2:
    st.plotly_chart(fig4, use_container_width=True)
with col3:
    st.plotly_chart(fig5, use_container_width=True)
with col4:
    st.plotly_chart(fig6, use_container_width=True)

# =====================
# 3. Average per Day & Month
# =====================
st.subheader("3️⃣ Rata-rata Casual vs Registered Users per Hari dan Bulan")
st.markdown("Perbandingan rata-rata pengguna casual dan registered baik secara harian maupun bulanan.")

daily_avg = df.groupby("day_name")[["casual_user", "registered_user"]].mean().reset_index()
daily_avg["day_name"] = pd.Categorical(daily_avg["day_name"], categories=day_order, ordered=True)
daily_avg = daily_avg.sort_values("day_name")

monthly_avg = df.groupby("month_name")[["casual_user", "registered_user"]].mean().reset_index()
monthly_avg["month_num"] = monthly_avg["month_name"].map({m: i for i, m in enumerate(month_order, 1)})
monthly_avg = monthly_avg.sort_values("month_num")

col1, col2 = st.columns(2)
with col1:
    fig7 = px.bar(daily_avg.melt(id_vars="day_name", var_name="Tipe", value_name="Average"),
                  x="day_name", y="Average", color="Tipe", barmode="group",
                  color_discrete_sequence=px.colors.sequential.Cividis,
                  title="Average Casual vs Registered per Day")
    st.plotly_chart(fig7, use_container_width=True)

with col2:
    fig8 = px.bar(monthly_avg.melt(id_vars=["month_name", "month_num"], var_name="Tipe", value_name="Average"),
                  x="month_name", y="Average", color="Tipe", barmode="group",
                  color_discrete_sequence=px.colors.sequential.Cividis,
                  title="Average Casual vs Registered per Month")
    st.plotly_chart(fig8, use_container_width=True)

# =====================
# 4. Tren Prediksi Bulanan
# =====================
st.subheader("4️⃣ Tren dan Prediksi Jumlah Pengguna Sepeda per Bulan")
st.markdown("Visualisasi tren pengguna sepeda bulanan dengan garis prediksi sederhana untuk melihat pola tahunan.")

monthly_trend = df.groupby("month_num")["total_user"].mean().reset_index()
fig9 = px.line(monthly_trend, x="month_num", y="total_user", markers=True,
               title="Tren Rata-rata Pengguna Sepeda per Bulan",
               labels={"month_num": "Bulan", "total_user": "Rata-rata Pengguna"},
               color_discrete_sequence=["#2a9d8f"])
fig9.add_trace(go.Scatter(
    x=monthly_trend["month_num"],
    y=monthly_trend["total_user"].rolling(2).mean(),
    mode='lines', name='Prediksi Tren',
    line=dict(dash='dash', color='#264653')
))
st.plotly_chart(fig9, use_container_width=True)

# =====================
# Footer
# =====================
st.markdown("---")
st.caption(f"Data yang ditampilkan untuk tahun: {'Semua Tahun' if selected_year == 'All' else selected_year}")
