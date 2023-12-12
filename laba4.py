import pandas as pd
import numpy as np
from main import list_dataset
import os
from PIL import Image
from typing import Tuple, List
import cv2
import matplotlib.pyplot as plt




"""
data - [[строчка]
        [строчка]
        [строчка]]
index - [индексы вертикально]
columns - [индексы горизонтально]

df.loc['mark'] доступ по метке к группе элементов
df[df['mark']==...] для сортировки по конкретной колонке
df['height'].value_counts() счетчик одинаковых значений
"""

tiger_list, leopard_list = \
        [x for x in list_dataset('dataset', 'tiger/')[0]], \
        [x for x in list_dataset('dataset', 'leopard/')[0]]
animals_list = []
for lists_i in range(max(len(tiger_list), len(leopard_list))):
    if lists_i < len(tiger_list): animals_list.append(tiger_list[lists_i])
    if lists_i < len(leopard_list): animals_list.append(leopard_list[lists_i])

def task12() -> (pd.DataFrame, list):
    global animals_list
    """
    создаем датафрейм с колонками: [абсолютный путь, класс]
    :return dataframe with 2 columns:
    """
    df_list = []
    for x in animals_list:
        df_list.append([x, x.split('/')[-2]])
    df = pd.DataFrame(df_list, columns=['absolute_path', 'animal'])
    return df, df_list

# print(task12()[0])

def task3(df: pd.DataFrame, df_list: list) -> pd.DataFrame:
    """
    создаем третью колонку с метками 0 и 1
    :param df:
    :param df_list:
    :return dataframe with 3 columns:
    """
    df_list_temp = [x[1] for x in df_list]
    df['mark'] = [0 if x == 'tiger' else 1 for x in df_list_temp]
    return df

# print(task3(task12()[0], task12()[1]))

def task4(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавить в DataFrame три столбца, первый из которых содержит информацию о высоте изображения,
    второй о ширине, а третий о глубине (количество каналов).
    :param df:
    :return:
    """
    global animals_list
    # открываем изображение
    width_list, height_list, depth_list = [], [], []
    for pic in animals_list:
        img = Image.open(pic)
        width, height = img.size
        depth = img.mode
        if depth == 'RGB':
            depth_list.append(8)
        elif depth == 'PNG':
            depth_list.append(16)
        width_list.append(width)
        height_list.append(height)

    df['width'] = width_list
    df['height'] = height_list
    df['depth'] = depth_list

    return df

# print(task4(task3(task12()[0], task12()[1])))
full_params_df = task4(task3(task12()[0], task12()[1]))

def task5(df: pd.DataFrame) -> pd.DataFrame:
    """
    считает средние статистические данные
    :param df:
    :return: dataframe со статистикой по всем данным
    """
    statistic_tiger = df[df['mark'] == 0].describe()
    statistic_leopard = df[df['mark'] == 1].describe()
    eps = 10
    balanced_flag = '\nset is balanced\n'
    if abs(statistic_tiger['width'].mean() - statistic_leopard['width'].mean()) >= eps:
        balanced_flag = '\nset is not balanced\n'
    return df[['width', 'height']].describe()

# print(task5(task4(task3(task12()[0], task12()[1]))))

def task_6_new_df(df: pd.DataFrame, mark: int) -> pd.DataFrame:
    return df[df['mark'] == mark]

# print(task_6_new_df(full_params_df, 0))

def task_7(df: pd.DataFrame, mark: int, height_max: int, width_lim: int) -> pd.DataFrame:
    return df[(df['mark'] == mark) & (df['height'] <= height_max) & (df['width'] <= width_lim)]

# print(task_7(full_params_df, 0, full_params_df['height'].max(), full_params_df['width'].max()))

def task_8(df: pd.DataFrame) -> pd.DataFrame:
    """
    добавляем колонку с подсчетом пикселей
    :param df:
    :return:
    """
    df['pixels'] = df['width'] * df['height'] * df['depth']
    return df

full_params_df = task_8(full_params_df)

def task_9(df: pd.DataFrame) -> pd.DataFrame:
    """
    добавляем колонку с подсчетом пикселей
    :param df:
    :return:
    """
    grouped = df.groupby('animal').agg({'pixels': ['max', 'min', 'mean']})
    return grouped

# print(task_9(full_params_df))

def get_hists(df: pd.DataFrame, class_name: int) -> List[np.ndarray]:
    """
    Возвращает 3 массива значений гистограммы по каждому каналу(b, g, r)
    """
    class_df = task_6_new_df(df, class_name)
    img = cv2.imread(class_df['absolute_path'].sample().values[0])
    hists = []
    for i in range(3):
        hist = cv2.calcHist([img], [i], None, [256], [0, 256])
        hists.append(hist)
    return hists

print(get_hists(full_params_df, 0))

hists = get_hists(full_params_df, 1)
colors = ["Blue", "Green", "Red"]

for i in range(len(hists)):
    plt.plot(hists[i], color=colors[i], label=f"{colors[i]} Histogram")
    plt.xlim([0, 256])

plt.title("Histograms")
plt.xlabel('Intensity', fontsize=13)
plt.ylabel('Density Pixels', fontsize=13)
plt.legend()
plt.show()










