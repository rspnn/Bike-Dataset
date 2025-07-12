
import streamlit as st
import pandas as pd
import plotly.express as px

# =======================
# LOAD DATA
# =======================
@st.cache_data
def load_data():
    df = pd.read_csv("bike.csv")
    return df

df = load_data()

st.title("Dashboard Peminjaman Sepeda 🚴‍♂️")

# =======================
# PREPROCESSING
# =======================

# Mapping untuk musim
season_mapping = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}
df['Season'] = df['season'].map(season_mapping)

# Mapping untuk bulan
month_mapping = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}
df['month_name'] = df['mnth'].map(month_mapping)

# Hitung rata-rata pengguna per musim
avg_rentals_season = df.groupby('Season')['cnt'].mean().reset_index()
avg_rentals_season.rename(columns={'cnt': 'Average Rentals'}, inplace=True)

# Hitung rata-rata pengguna per bulan
avg_rentals_month = df.groupby('month_name')['cnt'].mean().reset_index()
avg_rentals_month['month_num'] = avg_rentals_month['month_name'].map({v: k for k, v in month_mapping.items()})
avg_rentals_month = avg_rentals_month.sort_values('month_num')

# =======================
# VISUALISASI
# =======================

# Chart 1: Rata-rata peminjaman per musim (Viridis)
st.subheader("Rata-rata Peminjaman Sepeda per Musim")

season_numeric = {'Spring': 1, 'Summer': 2, 'Fall': 3, 'Winter': 4}
avg_rentals_season['season_num'] = avg_rentals_season['Season'].map(season_numeric)

fig_season = px.bar(
    avg_rentals_season,
    x="Season",
    y="Average Rentals",
    text='Average Rentals',
    color='season_num',
    title='Rata-rata Peminjaman Sepeda per Musim',
    color_continuous_scale='Viridis'
)

fig_season.update_traces(
    texttemplate='%{text:.0f}',
    textposition='outside',
    hovertemplate='Musim: %{x}<br>Rata-rata: %{y:.0f}'
)

fig_season.update_layout(
    template='plotly_white',
    xaxis_title='Musim',
    yaxis_title='Rata-rata Jumlah Peminjaman',
    coloraxis_showscale=False
)

st.plotly_chart(fig_season)

# Chart 2: Rata-rata peminjaman per bulan (Viridis)
st.subheader("Rata-rata Peminjaman Sepeda per Bulan")

fig_month = px.bar(
    avg_rentals_month,
    x='month_name',
    y='cnt',
    text='cnt',
    color='month_num',
    title='Rata-rata Peminjaman Sepeda per Bulan',
    color_continuous_scale='Viridis',
    labels={'month_name': 'Bulan', 'cnt': 'Rata-rata Jumlah Pengguna'}
)

fig_month.update_traces(
    texttemplate='%{text:.0f}',
    textposition='outside',
    hovertemplate='Bulan: %{x}<br>User: %{y:.0f}'
)

fig_month.update_layout(
    template='plotly_white',
    width=850,
    height=500,
    xaxis_tickangle=-45,
    coloraxis_showscale=False
)

st.plotly_chart(fig_month)
