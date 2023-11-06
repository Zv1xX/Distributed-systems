import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Устанавливаем соединение с базой данных
conn = sqlite3.connect('log.db')

# Заголовок приложения
st.title('Анализ данных')

# Боковая панель для настройки параметров
st.sidebar.header('Параметры анализа')

# Параметр 1: Интервал анализа данных в диапазоне
start_date = st.sidebar.date_input("Начальная дата", datetime(2023, 1, 1))
end_date = st.sidebar.date_input("Конечная дата", datetime(2023, 12, 31))

# Преобразование начальной и конечной даты в формат datetime
start_date = datetime(start_date.year, start_date.month, start_date.day)
end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

# Параметр 2: Интервал разбиения/группировки данных гистограммы в часах
histogram_interval = st.sidebar.slider("Интервал разбиения/группировки данных (часы)", 1, 24, 4)

# Параметр 3: Тип операции
operation_type = st.sidebar.text_input("Тип операции", "")

# Запрос данных из базы данных
cur = conn.cursor()
cur.execute('SELECT event_created, event_type FROM event_logs')
data = cur.fetchall()

# Преобразование данных в DataFrame
data_df = pd.DataFrame(data, columns=['event_created', 'event_type'])

# Преобразование столбца 'event_created' в формат datetime
data_df['event_created'] = pd.to_datetime(data_df['event_created'])

# Фильтрация данных на основе параметров
filtered_data = data_df[(data_df['event_created'] >= start_date) & (data_df['event_created'] <= end_date)]

if operation_type:
    filtered_data = filtered_data[filtered_data['event_type'].str.contains(operation_type, case=False)]

# Создание гистограммы
if not filtered_data.empty:
    st.header('Гистограмма количества вызовов для типов операций')

    # Группировка данных по типам операций и подсчет количества вызовов
    operation_counts = filtered_data.groupby('event_type').size().reset_index(name='count')

    # Строим гистограмму
    fig, ax = plt.subplots()
    ax.bar(operation_counts['event_type'], operation_counts['count'])
    ax.set_xlabel('Тип операции')
    ax.set_ylabel('Количество вызовов')
    ax.set_title('Гистограмма количества вызовов для типов операций')

    # Отображение гистограммы в Streamlit
    st.pyplot(fig)
else:
    st.warning('Нет данных для отображения с выбранными параметрами.')

# Закрываем соединение с базой данных
conn.close()