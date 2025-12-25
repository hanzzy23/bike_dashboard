import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =============================
# Judul Dashboard
# =============================
st.title("Dashboard Bike-sharing Rental Sepeda")
st.markdown("Analisis Tren Penyewaan Sepeda Berdasarkan Hari dan Jam")

# =============================
# Load Data
# =============================
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")


# =============================
# Analisis Tren Harian
# =============================
st.subheader("Tren Jumlah Rental Sepeda per Hari")

# Pastikan dteday bertipe datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

sns.set_style("whitegrid")

fig, ax = plt.subplots(figsize=(14,6))

# Lineplot tren rental
sns.lineplot(data=day_df, x='dteday', y='cnt', marker='o', color='#2a9d8f', label='Jumlah Rental', ax=ax)

# Garis rata-rata
mean_cnt = day_df['cnt'].mean()
ax.axhline(mean_cnt, color='#f4a261', linestyle='--', label=f'Rata-rata ({int(mean_cnt)})')

# Highlight puncak rental
max_idx = day_df['cnt'].idxmax()
max_day = day_df.loc[max_idx, 'dteday']
max_value = day_df.loc[max_idx, 'cnt']

ax.scatter(max_day, max_value, color='#e63946', s=100, zorder=5, label='Puncak Rental')
ax.text(max_day, max_value + 5, f'{max_value}', color='#e63946', fontweight='bold')

# Judul dan label
ax.set_title("Tren Jumlah Rental Sepeda per Hari", fontsize=18, fontweight='bold')
ax.set_xlabel("Tanggal", fontsize=14)
ax.set_ylabel("Jumlah Rental", fontsize=14)

# Format tanggal di sumbu x
fig.autofmt_xdate()  # otomatis rotasi dan rapi
ax.legend()
st.pyplot(fig)

# =============================
# Analisis Per Jam (Opsional)
# =============================
st.subheader("Tren Penyewaan Sepeda Per Jam")
#Atur style seaborn agar lebih rapi sns.set_style("whitegrid")

fig, ax = plt.subplots(figsize=(14,6))

#Buat lineplot dengan marker untuk tiap titik data
sns.lineplot( 
data = hour_df, 
x='hr',
y='cnt', 
hue="weekday", 
palette='tab10',
marker='o'
)

#Judul dan label sumbu
plt.title("Tren Jumlah Rental sepeda per Jam berdasarkan Hari", fontsize=16, fontweight='bold') 
plt.xlabel("Jam (0-23)", fontsize=12) 
plt.ylabel("Jumlah Rental", fontsize=12)

#Tampilkan legend dengan judul

plt.legend(title="Hari", fontsize=10, title_fontsize=12)

#Tampilkan grid minor untuk membaca nilai lebih detail 
plt.minorticks_on() 
plt.grid(which='both', linestyle='--', linewidth = 0.5, alpha = 0.7)

plt.tight_layout()
st.pyplot(fig)

# =============================
# Analisis Weekday vs Weekend
# =============================
st.subheader("Perbedaan Jumlah Rental: Weekday vs Weekend")
day_df['is_weekend'] = day_df['weekday'].apply(lambda x: 1 if x>=5 else 0)

sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(8,5))

# Boxplot dengan warna berbeda
sns.boxplot(
    data=day_df,
    x='is_weekend',
    y='cnt',
    palette=['#1f77b4', '#ff7f0e'],  # Biru untuk weekday, oranye untuk weekend
    ax=ax
)

# Ganti label x-axis menjadi lebih jelas
ax.set_xticklabels(['Weekday', 'Weekend'])

# Judul dan label sumbu
ax.set_title("Perbedaan Jumlah Penyewaan Sepeda: Weekday vs Weekend", fontsize=14, fontweight='bold')
ax.set_xlabel("Tipe Hari", fontsize=12)
ax.set_ylabel("Jumlah Rental Sepeda", fontsize=12)

# Grid horizontal
ax.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7)

# Tambahkan median di atas box
medians = day_df.groupby('is_weekend')['cnt'].median().values
for i, median in enumerate(medians):
    ax.text(i, median + 2, f'{median:.0f}', ha='center', color='black', fontweight='bold')

plt.tight_layout()
st.pyplot(fig)

