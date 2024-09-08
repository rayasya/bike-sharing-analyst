import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load merged data
@st.cache_data
def load_data():
    return pd.read_csv('dashboard/main_data.csv')

data = load_data()

# Data preparation
temp_min, temp_max = 0.02, 1
hum_min, hum_max = 0, 1
windspeed_min, windspeed_max = 0, 0.8507

data['temp_actual'] = data['temp_hourly'] * (temp_max - temp_min) + temp_min
data['hum_actual'] = data['hum_hourly'] * 100
data['windspeed_actual'] = data['windspeed_hourly'] * (windspeed_max - windspeed_min) + windspeed_min

# Streamlit UI
st.title('Bike Sharing Data Analysis')

with st.sidebar:
    # Date Range Picker
    min_date = pd.to_datetime(data['dteday']).min()
    max_date = pd.to_datetime(data['dteday']).max()
    start_date, end_date = st.date_input(
        label='Rentang Waktu', 
        min_value=min_date, 
        max_value=max_date, 
        value=[min_date, max_date]
    )

# Filter data by selected date range
filtered_data = data[(data['dteday'] >= str(start_date)) & (data['dteday'] <= str(end_date))]

st.write(f'Data dari {start_date} hingga {end_date}')
st.write(filtered_data)

# Analysis for holiday vs. workingday
st.header('Analisis Penggunaan Sepeda berdasarkan Jenis Hari')

# Aggregate by holiday and workingday
day_type_analysis = filtered_data.groupby(['holiday', 'workingday']).agg({
    'cnt_daily': 'mean'
}).reset_index()
day_type_analysis['day_type'] = day_type_analysis.apply(
    lambda row: 'Hari Libur' if row['holiday'] == 1 else 'Hari Kerja', axis=1
)

# Plot usage by day type
fig_day_type, ax_day_type = plt.subplots(figsize=(10, 6))
sns.barplot(data=day_type_analysis, x='day_type', y='cnt_daily', ax=ax_day_type, palette='coolwarm')
ax_day_type.set_title('Rata-rata Penggunaan Sepeda berdasarkan Jenis Hari')
ax_day_type.set_xlabel('Jenis Hari')
ax_day_type.set_ylabel('Rata-rata Penggunaan Sepeda')
st.pyplot(fig_day_type)

# Plot for temperature, humidity, windspeed vs. bike usage
st.header('Dampak Cuaca terhadap Penggunaan Sepeda')

fig_weather, axs = plt.subplots(2, 2, figsize=(14, 10))

# Temperature vs. Daily Bike Usage
sns.scatterplot(data=filtered_data, x='temp_actual', y='cnt_daily', color='blue', ax=axs[0, 0])
sns.regplot(data=filtered_data, x='temp_actual', y='cnt_daily', scatter=False, color='blue', ax=axs[0, 0], line_kws={'label': 'Tren Suhu'})
axs[0, 0].set_title('Suhu vs. Penggunaan Sepeda Harian')
axs[0, 0].set_xlabel('Suhu Rata-rata (°C)')
axs[0, 0].set_ylabel('Total Penggunaan Sepeda per Hari')

# Humidity vs. Daily Bike Usage
sns.scatterplot(data=filtered_data, x='hum_actual', y='cnt_daily', color='green', ax=axs[0, 1])
sns.regplot(data=filtered_data, x='hum_actual', y='cnt_daily', scatter=False, color='green', ax=axs[0, 1], line_kws={'label': 'Tren Kelembapan'})
axs[0, 1].set_title('Kelembapan vs. Penggunaan Sepeda Harian')
axs[0, 1].set_xlabel('Kelembapan Rata-rata (%)')
axs[0, 1].set_ylabel('Total Penggunaan Sepeda per Hari')

# Wind Speed vs. Daily Bike Usage
sns.scatterplot(data=filtered_data, x='windspeed_actual', y='cnt_daily', color='red', ax=axs[1, 0])
sns.regplot(data=filtered_data, x='windspeed_actual', y='cnt_daily', scatter=False, color='red', ax=axs[1, 0], line_kws={'label': 'Tren Kecepatan Angin'})
axs[1, 0].set_title('Kecepatan Angin vs. Penggunaan Sepeda Harian')
axs[1, 0].set_xlabel('Kecepatan Angin Rata-rata (m/s)')
axs[1, 0].set_ylabel('Total Penggunaan Sepeda per Hari')

# Adjust layout
plt.tight_layout()
st.pyplot(fig_weather)

# Combined Analysis Plot
st.header('Analisis Gabungan Cuaca dan Penggunaan Sepeda')

fig_combined, axs_combined = plt.subplots(2, 2, figsize=(14, 10))

# Temperature vs. Daily Bike Usage
sns.scatterplot(data=filtered_data, x='temp_actual', y='cnt_daily', color='blue', ax=axs_combined[0, 0])
sns.regplot(data=filtered_data, x='temp_actual', y='cnt_daily', scatter=False, color='blue', ax=axs_combined[0, 0], line_kws={'label': 'Tren Suhu'})
axs_combined[0, 0].set_title('Suhu vs. Penggunaan Sepeda Harian')
axs_combined[0, 0].set_xlabel('Suhu Rata-rata (°C)')
axs_combined[0, 0].set_ylabel('Total Penggunaan Sepeda per Hari')

# Humidity vs. Daily Bike Usage
sns.scatterplot(data=filtered_data, x='hum_actual', y='cnt_daily', color='green', ax=axs_combined[0, 1])
sns.regplot(data=filtered_data, x='hum_actual', y='cnt_daily', scatter=False, color='green', ax=axs_combined[0, 1], line_kws={'label': 'Tren Kelembapan'})
axs_combined[0, 1].set_title('Kelembapan vs. Penggunaan Sepeda Harian')
axs_combined[0, 1].set_xlabel('Kelembapan Rata-rata (%)')
axs_combined[0, 1].set_ylabel('Total Penggunaan Sepeda per Hari')

# Wind Speed vs. Daily Bike Usage
sns.scatterplot(data=filtered_data, x='windspeed_actual', y='cnt_daily', color='red', ax=axs_combined[1, 0])
sns.regplot(data=filtered_data, x='windspeed_actual', y='cnt_daily', scatter=False, color='red', ax=axs_combined[1, 0], line_kws={'label': 'Tren Kecepatan Angin'})
axs_combined[1, 0].set_title('Kecepatan Angin vs. Penggunaan Sepeda Harian')
axs_combined[1, 0].set_xlabel('Kecepatan Angin Rata-rata (m/s)')
axs_combined[1, 0].set_ylabel('Total Penggunaan Sepeda per Hari')

# Adjust layout
plt.tight_layout()
st.pyplot(fig_combined)

# RFM Analysis
st.header('Analisis RFM (Recency, Frequency, Monetary)')

# Calculate Recency, Frequency, and Monetary on filtered data
filtered_data['dteday'] = pd.to_datetime(filtered_data['dteday'])
last_date = filtered_data['dteday'].max()
filtered_data['recency'] = (last_date - filtered_data['dteday']).dt.days

rfm_data = filtered_data.groupby('instant').agg({
    'recency': 'min',
    'cnt_daily': ['mean', 'sum']
}).reset_index()
rfm_data.columns = ['user_id', 'recency', 'frequency', 'monetary']

st.write('Data RFM:')
st.write(rfm_data)

# Plot RFM Results
fig_rfm, axs_rfm = plt.subplots(1, 3, figsize=(18, 6))

# Recency
sns.histplot(rfm_data['recency'], bins=30, kde=True, ax=axs_rfm[0], color='blue')
axs_rfm[0].set_title('Distribusi Recency')
axs_rfm[0].set_xlabel('Recency (days)')
axs_rfm[0].set_ylabel('Frequency')

# Frequency
sns.histplot(rfm_data['frequency'], bins=30, kde=True, ax=axs_rfm[1], color='green')
axs_rfm[1].set_title('Distribusi Frequency')
axs_rfm[1].set_xlabel('Frequency')
axs_rfm[1].set_ylabel('Frequency')

# Monetary
sns.histplot(rfm_data['monetary'], bins=30, kde=True, ax=axs_rfm[2], color='red')
axs_rfm[2].set_title('Distribusi Monetary')
axs_rfm[2].set_xlabel('Monetary')
axs_rfm[2].set_ylabel('Frequency')

plt.tight_layout()
st.pyplot(fig_rfm)

st.caption('Copyright (c) 2024 Muhammad Rayasya Dziqi Cahyana')
