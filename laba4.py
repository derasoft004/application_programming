import pandas as pd
from main import list_dataset
import os
from PIL import Image
from typing import Tuple


"""
data - [[строчка]
        [строчка]
        [строчка]]
index - [индексы вертикально]
columns - [индексы горизонтально]
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

print(task4(task3(task12()[0], task12()[1])))

# df.loc['r1'] доступ по метке к группе элементов

def task5(df: pd.DataFrame) -> pd.DataFrame:
    """
    values = (height, width, depth, mark)
    :param df:
    :return:
    """
    height, width, depth, mark = df['height'], df['width'], df['depth'], df['mark']
    values: Tuple = height.value_counts(), width.value_counts(), depth.value_counts(), mark.value_counts()
    print(len(height), len(width), len(depth), len(mark))
    print(len(values[0]), len(values[1]), len(values[2]), len(values[3]))
    mark_0, mark_1 = [], []
    for ind in range(len(height)):
        if mark[ind]: mark_1.append([height[ind], width[ind], depth[ind]])
        else: mark_0.append([height[ind], width[ind], depth[ind]])
    # print(mark_1, mark_0, sep='\n\n')

    return df

task5(task4(task3(task12()[0], task12()[1])))

















