import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import seaborn as sns
from eda import gluing_tables

@st.cache_data
def load_data():
    return gluing_tables()

def get_plot_continuous_feature(column: str, category: str) -> Figure:
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.kdeplot(data, x=rus_eng_columns[column], hue=rus_eng_categories[category], fill=True, ax=ax)
    plt.grid()
    plt.title(f'{column} клиентов')
    plt.legend(feature_values[category])
    plt.xticks(rotation=45)
    if column == 'Доход':
        plt.xlim((0, 50000))

    return fig

def get_plot_categorical_feature(column: str, category: str) -> Figure:
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.countplot(data, x=rus_eng_columns[column], hue=rus_eng_categories[category], ax=ax)
    plt.grid()
    plt.title(f'{column} клиентов')
    plt.legend(feature_values[category])
    plt.xticks(rotation=90)

    return fig

def get_corr_map() -> Figure:
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(data[data.select_dtypes(include=['int64', 'float64']).columns].corr())

    return fig

st.set_page_config(page_title="EDA Clients", page_icon=":guardsman:", layout="wide")

data = load_data()

rus_eng_categories = {'Наличие отклика': 'TARGET',
                      'Пол': 'GENDER',
                      'Трудовой статус': 'SOCSTATUS_WORK_FL',
                      'Пенсионный статус': 'SOCSTATUS_PENS_FL'}

rus_eng_columns = {'Возраст': 'AGE',
                   'Доход': 'PERSONAL_INCOME',
                    'Образование': 'EDUCATION',
                   'Семейное положение': 'MARITAL_STATUS'
                   }

feature_values = {'Наличие отклика': ['Зарегистрирован отклик', 'Отклика нет'],
                  'Пол': ['Муж','Жен'],
                  'Трудовой статус': ['Трудоустроен','Безработный'],
                  'Пенсионный статус': ['Пенсионер','Не пенсионер']}

st.title("Данные о клиентах банка")
st.markdown('Данные очищены от пропусков и дубликатов')

with st.container():

    st.sidebar.title("Визуализация распределений признаков")
    select_graph_distribution = st.sidebar.selectbox(
        label='Признак',
        options=['Возраст', 'Доход','Образование', 'Семейное положение']
    )

    select_hue = st.sidebar.radio(
        label='Сравнить распределения по категориям',
        options=['Наличие отклика','Пол','Трудовой статус','Пенсионный статус']
    )

st.subheader('Распределения признаков')

if select_graph_distribution in ['Возраст','Доход'] :
    st.pyplot(get_plot_continuous_feature(select_graph_distribution, select_hue))
else:
    st.pyplot(get_plot_categorical_feature(select_graph_distribution, select_hue))

with st.container():
    st.subheader('Матрица корреляций')
    st.pyplot(get_corr_map())

    st.subheader('Числовые характеристики числовых столбцов')
    st.dataframe(data.drop('ID_CLIENT', axis = 1).describe())

    st.subheader('Числовые характеристики текстовых столбцов')
    st.dataframe(data.describe(include='object'))


