from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd

from translators import *
def get_plot_continuous_feature(data, column: str, category: str) -> Figure:
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.kdeplot(data, x=rus_eng_columns[column], hue=rus_eng_categories[category], fill=True, ax=ax)
    plt.grid()
    plt.title(f'{column} клиентов')
    plt.legend(feature_values[category])
    plt.xticks(rotation=45)
    if column == 'Доход':
        plt.xlim((0, 50000))

    return fig

def get_plot_categorical_feature(data, column: str, category: str) -> Figure:
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.countplot(data, x=rus_eng_columns[column], hue=rus_eng_categories[category], ax=ax)
    plt.grid()
    plt.title(f'{column} клиентов')
    plt.legend(feature_values[category])
    plt.xticks(rotation=90)

    return fig

def get_corr_map(data) -> Figure:
    fig, ax = plt.subplots(figsize=(8, 4))
    num_data = data[data.select_dtypes(include=['int64', 'float64']).columns]
    num_data = num_data.drop('ID_CLIENT', axis=1)

    sns.heatmap(num_data.corr(),
                annot=True,
                fmt=".3f",
                annot_kws={"size": 5})

    return fig

def get_confusion_map(matrix) -> Figure:
    class_names = ['Нет отклика', 'Есть отклик']

    fig, ax = plt.subplots(figsize=(8, 4))
    cm_df = pd.DataFrame(matrix, index=class_names, columns=class_names)

    sns.heatmap(cm_df, annot=True, fmt='d')
    plt.xlabel('Предсказанный класс')
    plt.ylabel('Фактический класс')

    return fig