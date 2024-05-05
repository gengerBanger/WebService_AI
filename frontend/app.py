import numpy as np
import streamlit as st
from eda import gluing_tables

from graphs import *
from backend.model import preprocessing, create_model_fit, test_model, get_top_weights, get_predict_proba

@st.cache_data
def load_data():
    return gluing_tables()


def main_process() -> None:
    set_config()
    eda_tab, model_tab = set_tabs()
    data = load_data()
    X_train, X_test, y_train, y_test, columns = preprocessing(data)

    charts(eda_tab, data)
    corr_and_tables(eda_tab, data)

    top_weights(model_tab, X_train, y_train, columns)
    test_with_limit(model_tab, X_test, y_test)
    predict_part(model_tab, data)

def set_config() -> None:
    st.set_page_config(page_title="EDA Clients",
                       page_icon=":guardsman:",
                       layout="wide")

def set_tabs():
    tab1, tab2 = st.tabs(["Data", "Model"])
    return tab1, tab2

def charts(tab, data) -> None:
    with tab:
        st.title("Данные о клиентах банка")
        st.divider()
        st.markdown('Данные очищены от пропусков и дубликатов')

        with st.container():
            col1, col2 = st.columns(2)
            with col2:
                st.subheader("Параметры отображения")
                select_graph_distribution = st.selectbox(
                    label='Признак',
                    options=['Возраст', 'Доход', 'Образование', 'Семейное положение']
                )

                select_hue = st.radio(
                    label='Сравнить распределения по категориям',
                    options=['Наличие отклика', 'Пол', 'Трудовой статус', 'Пенсионный статус']
                )
            with col1:
                st.subheader('Распределения признаков')

                if select_graph_distribution in ['Возраст', 'Доход']:
                    st.pyplot(get_plot_continuous_feature(data, select_graph_distribution, select_hue))
                else:
                    st.pyplot(get_plot_categorical_feature(data, select_graph_distribution, select_hue))

def corr_and_tables(tab, data) -> None:
    with tab:
        st.divider()
        with st.container():
            st.subheader('Матрица корреляций')
            st.pyplot(get_corr_map(data))

            st.subheader('Числовые характеристики числовых столбцов')
            st.dataframe(data.drop('ID_CLIENT', axis=1).describe())

            st.subheader('Числовые характеристики текстовых столбцов')
            st.dataframe(data.describe(include='object'))

def top_weights(tab, X_train, y_train, columns) -> None:
    with tab:
        st.title('Тестирование модели')
        st.divider()

        create_model_fit(X_train, y_train)

        st.subheader('Признаки с большим влиянием на результат работы модели')
        st.table(get_top_weights(columns))

def test_with_limit(tab, X_test, y_test) -> None:
    with tab:
        st.divider()
        st.subheader('Настройте значение порога')
        col1, col2 = st.columns(2)

        with col1:
            limit = st.select_slider(
                'Порог уверенности модели для класса "Есть отклик"',
                options=np.arange(0, 1, .01)
            )
            matrix, report = test_model(X_test, y_test, limit)

        with col2:
            st.subheader('Результаты классификации')

        col21, col22 = st.columns(2)
        with col21:
            st.pyplot(get_confusion_map(matrix))
        with col22:
            st.table(report)

def predict_part(tab, data) -> None:
    with tab:
        st.divider()
        st.subheader('Прогноз модели на выбранной конфигурации')
        col31, col32, col33, col34 = st.columns(4)
        with col31:
            gender = st.selectbox(
                'Выберете гендер',
                options=['Мужчина', 'Женщина']
            )
            age = st.number_input('Введите возраст',
                                  min_value=0,
                                  value=30)
            education = st.selectbox(
                'Выберете уровень образования',
                options=data['EDUCATION'].unique()
            )
        with col32:
            family_status = st.selectbox(
                'Выберете семейный статус',
                options=data['MARITAL_STATUS'].unique()
            )
            child = st.number_input('Введите количество детей',
                                    min_value=0,
                                    value='min')
            dependat = st.number_input('Введите количество иждивенцов',
                                       min_value=0,
                                       value='min')
        with col33:
            income = st.number_input('Введите доход',
                                     min_value=0,
                                     value=20000)
            work = st.selectbox(
                'Выберете рабочий статус',
                options=['Есть работа', 'Безработный'],

            )
            pens = st.selectbox(
                'Выберете пенсионный статус',
                options=['Не Пенсионер', 'Пенсионер']
            )
        with col34:
            loans = st.number_input('Введите количество задолжностей',
                                    min_value=0,
                                    value='min')
            closed_loans = st.number_input('Введите количество погашенных задолжностей',
                                           min_value=0,
                                           value='min')
        work = 1 if work == 'Есть работа' else 0
        pens = 1 if pens == 'Пенсионер' else 0
        gender = 1 if gender == 'Мужчина' else 0

        features = [age, gender, education, family_status,
                    child, dependat, work, pens, income, loans, closed_loans]

        st.success(get_predict_proba(features))

if __name__ == "__main__":
    main_process()