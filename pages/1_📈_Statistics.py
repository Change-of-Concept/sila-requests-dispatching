import asyncio
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from core.db import fetch_request_types, fetch_hardware_types, fetch_serial_numbers_statistics

st.title('Статистика заявок')

def plot_with_int_yaxis(counts, title, xlabel, ylabel, colors=None):
    fig, ax = plt.subplots(figsize=(6, 4))
    counts.plot(kind='bar', ax=ax, color=colors)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    ax.yaxis.get_major_locator().set_params(integer=True)
    
    plt.tight_layout()
    return fig


st.subheader('Распределение точек отказа')
request_types = asyncio.run(fetch_request_types())
counts = request_types['request_type'].value_counts()
fig = plot_with_int_yaxis(counts, 'Распределение точек отказа', 'Точка отказа', 'Количество')
st.pyplot(fig)


st.subheader('Распределение типов оборудования')
hardware_types = asyncio.run(fetch_hardware_types())
counts = hardware_types['hardware_type'].value_counts()
fig = plot_with_int_yaxis(counts, 'Распределение типов оборудования', 'Тип оборудования', 'Количество', colors=['#1f77b4'])
st.pyplot(fig)


st.subheader('Присутствие серийных номеров в заявке')
requests_df, serial_numbers_df = asyncio.run(fetch_serial_numbers_statistics())
has_serial = requests_df['id'].isin(serial_numbers_df['request_id'])
counts = pd.Series({
    "Есть серийный номер": has_serial.sum(),
    "Нет серийного номера": (~has_serial).sum()
})
fig = plot_with_int_yaxis(counts, "Присутствие серийных номеров в заявке", "Категория", "Количество заявок", colors=['#4CAF50', '#FF5722'])
st.pyplot(fig)
