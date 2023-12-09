import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request
import csv
from typing import Tuple, Optional
from random import randint

tig, leo = 'tiger', 'leopard'

def driver_scroller(driver_to_scroll, pix):
    sroll_range = 0
    while sroll_range < pix:
        driver_to_scroll.execute_script(f"window.scrollTo(0, {sroll_range});")  # ширина, высота
        sroll_range += 4  # скорость
    while sroll_range > 0:
        driver_to_scroll.execute_script(f"window.scrollTo(0, {sroll_range});")  # ширина, высота
        sroll_range -= 4


full_list_tiger, full_list_leopard = [], []
count_pictures = 0

URLs_tiger = ["https://ya.ru/images/search?from=tabbar&text=tiger",
            "https://ya.ru/images/search?from=tabbar&lr=11135&p=10&rpt=image&text=tiger",
            "https://ya.ru/images/search?from=tabbar&lr=11135&p=21&rpt=image&text=tiger",
            "https://ya.ru/images/search?from=tabbar&lr=11135&p=30&rpt=image&text=tiger",
            "https://ya.ru/images/search?from=tabbar&lr=11135&p=40&rpt=image&text=tiger"]

URLs_leopard = ["https://ya.ru/images/search?from=tabbar&text=leopard",
                "https://ya.ru/images/search?from=tabbar&lr=11135&p=10&rpt=image&text=leopard",
                "https://ya.ru/images/search?from=tabbar&lr=11135&p=20&rpt=image&text=leopard",
                "https://ya.ru/images/search?from=tabbar&lr=11135&p=30&rpt=image&text=leopard",
                "https://ya.ru/images/search?from=tabbar&lr=11135&p=40&rpt=image&text=leopard"]

pictures_count, page_count = 0, 1


def make_driver_with_link(link, path_name, animal):
    global full_list_tiger, full_list_leopard
    driver = webdriver.Chrome()
    driver.get(link)
    print(driver.title)
    time.sleep(4)
    driver_scroller(driver, 15000)
    list_pictures = driver.find_elements(By.XPATH, path_name)
    if animal == "tiger": full_list_tiger += list_pictures
    elif animal == "leopard": full_list_leopard += list_pictures
    print(len(full_list_tiger), len(full_list_leopard))


def make_name(value):
    return '0'*(4-len(str(value))) + str(value)


def directory_maker(directory_tiger, directory_leopard):
    if not os.path.exists('dataset'): os.mkdir('dataset')
    if not os.path.exists(directory_tiger): os.mkdir(directory_tiger)
    if not os.path.exists(directory_leopard): os.mkdir(directory_leopard)


def save_pictures() -> None:
    global full_list_tiger, full_list_leopard
    directory_tiger, directory_leopard = "dataset/tiger", "dataset/leopard"
    directory_maker(directory_tiger, directory_leopard)
    print(f'lens: {len(full_list_tiger)}, {len(full_list_leopard)}')
    for elem in range(len(full_list_tiger)):
        img = urllib.request.urlopen(full_list_tiger[elem].get_attribute('src')).read()
        out = open(f"{directory_tiger}/{make_name(elem)}.jpg", "wb")
        out.write(img)
        out.close
    for elem in range(len(full_list_leopard)):
        img2 = urllib.request.urlopen(full_list_leopard[elem].get_attribute('src')).read()
        out = open(f"{directory_leopard}/{make_name(elem)}.jpg", "wb")
        out.write(img2)
        out.close


def main_first() -> None:
    """
    main first function is launch pages wish pictures and saves it
    :return:
    """
    def parser():
        for i in range(5):
            if len(full_list_tiger) <= 1000:
                make_driver_with_link(URLs_tiger[i], "//img[@class='serp-item__thumb justifier__thumb']", "tiger")
                time.sleep(10)
            if len(full_list_leopard) <= 1000:
                make_driver_with_link(URLs_leopard[i], "//img[@class='serp-item__thumb justifier__thumb']", "leopard")
                time.sleep(10)
    # parser()
    # save_pictures()


def list_dataset(dataset, animal) -> Tuple:
    return [f'{os.getcwd()}/{dataset}/{animal}{x}' for x in os.listdir(f'{dataset}/{animal}')], [f'{dataset}/{animal}{x}' for x in os.listdir(f'{dataset}/{animal}')]
    # когда передаем animal - добавлять /, если пустое - ничего не добавлять

def loop_for_writing(csvfile, full_list_t: list, list_t: list,
                     full_list_l: list, list_l: list, t: str, l: str) -> None:
    """
    loop for writing in csv file
    :param csvfile:
    :param full_list_t:
    :param list_t:
    :param full_list_l:
    :param list_l:
    :param t:
    :param l:
    :return:
    """
    for i in range(max(len(list_t), len(list_l))):
        if i < len(list_t) and t in list_t[i]: csvfile.writerow({'Full path': full_list_t[i], 'Relative path': list_t[i], 'class': t})
        if i < len(list_l) and l in list_l[i]: csvfile.writerow({'Full path': full_list_l[i], 'Relative path': list_l[i], 'class': l})


def annotation_maker(dataset, path: str, t, l) -> None:
    """
    It makes annotations for some assignments

    :param dataset:
    :param path:
    :param t:
    :param l:
    :return:
    """
    list_relative_path_images_tiger, list_relative_path_images_leopard = \
        list_dataset(dataset, t)[1], list_dataset(dataset, l)[1]
    list_full_path_images_tiger, list_full_path_images_leopard = \
        list_dataset(dataset, t)[0], list_dataset(dataset, l)[0]
    with open(dataset+'/'+path, 'w', newline='') as csvfile:
        fieldnames = ['Full path', 'Relative path', 'class']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        loop_for_writing(writer, list_full_path_images_tiger, list_relative_path_images_tiger,
                         list_full_path_images_leopard, list_relative_path_images_leopard,
                         tig, leo)


def copy_dataset(animal, new_dataset) -> None:
    """
    по dataset/{animal} собирается и копируется все содержимое в new_dataset

    :param animal:
    :param new_dataset:
    :return:
    """
    dataset_path = f"dataset/{animal}"
    if not os.path.exists(new_dataset):
        os.mkdir(new_dataset)

    image_list = os.listdir(dataset_path)
    for image in image_list:
        shutil.copy(f'{dataset_path}/{image}', f'{new_dataset}/{animal}_{image.split(".")[0]}.jpg')


def copy_dataset_rand(new_dataset: str, path: str) -> None:
    """

    :param new_dataset:
    :param path:
    :return:
    """
    if not os.path.exists(new_dataset):
        os.mkdir(new_dataset)

    with open(new_dataset + '/' + path, 'w', newline='') as csvfile:
        fieldnames = ['Full path', 'Relative path', 'class']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for animal in [tig, leo]:
            dataset_path = f"dataset/{animal}"

            image_list = os.listdir(dataset_path)
            for image in image_list:
                num = randint(0, 10000)
                relative_path_animal = f'{new_dataset}/{num}.jpg'
                full_path_animal = f'{os.getcwd()}/{relative_path_animal}'
                shutil.copy(f'{dataset_path}/{image}', f'{new_dataset}/{num}.jpg')
                writer.writerow({'Full path': full_path_animal, 'Relative path': relative_path_animal, 'class': animal})


count_t, count_l = 0, 0
def return_next(animal) -> str:
    """
    The function runs through a list of values
    and returns the following on every call

    :param animal:
    :return:
    """
    global count_t, count_l
    if animal == tig:
        if count_t > len(os.listdir(f'{os.getcwd()}/dataset/{animal}')): return Optional[None]
        rstr = make_name(count_t)
        count_t += 1
    elif animal == leo:
        if count_l > len(os.listdir(f'{os.getcwd()}/dataset/{animal}')): return Optional[None]
        rstr = make_name(count_l)
        count_l += 1
    return f'{os.getcwd()}/dataset/{animal}/{rstr}.jpg'

# def func1(elem):
#     return int(elem.split('.')[0])
#
# def sotring(lst):
#     return lst.sort(key=func1)

class Iterator:
    '''
    class Iterator iterates through a list of values
    and returns the following on every call
    '''
    def __init__(self, animal_list, lim, animal):
        self.animal = animal
        self.animal_list = animal_list
        self.lim = lim
        self.count = 0

    def __next__(self):
        if self.count < self.lim:
            self.count += 1
            if self.animal == 't': return f'dataset/tiger/'+self.animal_list[self.count - 1]
            elif self.animal == 'l': return f'dataset/leopard/'+self.animal_list[self.count - 1]
        else:
            raise StopIteration


def main_second() -> None:
    """1"""
    # annotation_maker('dataset', 'annotation.csv', tig + '/', leo + '/')
    # """2"""
    # copy_dataset(tig, 'new_dataset_task_2')
    # copy_dataset(leo, 'new_dataset_task_2')
    # annotation_maker('new_dataset_task_2', '0new_dataset_annotation.csv', '', '')
    # """3"""
    # copy_dataset_rand('new_dataset_task_3', '0new_dataset_annotation.csv')
    """4"""
    # for i in range(1210):
    #     print(return_next(tig))
    # for i in range(5):
    #     print(return_next(leo))
    """5"""
    dir_t, dir_l = f'{os.getcwd()}/dataset/{tig}', f'{os.getcwd()}/dataset/{leo}'
    iterator_tiger = Iterator(os.listdir(dir_t), len(os.listdir(dir_t)), 't')
    iterator_leo = Iterator(os.listdir(dir_l), len(os.listdir(dir_l)), 'l')
    try:
        for i in range(1210):
            print(next(iterator_tiger))
    except StopIteration: print(None)
    try:
        for i in range(5):
            print(next(iterator_leo))
    except StopIteration: print(None)


if __name__ == "__main__":
    """
    function main_second launch any functions
    to complete the tasks 
    """
    main_second()

























