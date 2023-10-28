import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request
import csv

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


def save_pictures():
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


def main_first():
    for i in range(5):
        if len(full_list_tiger) <= 1000:
            make_driver_with_link(URLs_tiger[i], "//img[@class='serp-item__thumb justifier__thumb']", "tiger")
            time.sleep(10)
        if len(full_list_leopard) <= 1000:
            make_driver_with_link(URLs_leopard[i], "//img[@class='serp-item__thumb justifier__thumb']", "leopard")
            time.sleep(10)
    save_pictures()
    annotation_maker('dataset/annotation.csv')


def list_dataset(animal):
    return [f'{os.getcwd()}/dataset/{animal}/{x}' for x in os.listdir(f'dataset/{animal}')], [f'dataset/{animal}/{x}' for x in os.listdir(f'dataset/{animal}')]


def loop_for_writing(csvfile, full_list_t: list, list_t: list,
                     full_list_l: list, list_l: list, t, l):
    for i in range(max(len(list_t), len(list_l))):
        if i < len(list_t): csvfile.writerow({'Full path': full_list_t[i], 'Relative path': list_t[i], 'class': t})
        if i < len(list_l): csvfile.writerow({'Full path': full_list_l[i], 'Relative path': list_l[i], 'class': l})


def annotation_maker(path: str):
    global tig, leo
    list_relative_path_images_tiger, list_relative_path_images_leopard = \
        list_dataset(tig)[1], list_dataset(leo)[1]
    list_full_path_images_tiger, list_full_path_images_leopard = \
        list_dataset(tig)[0], list_dataset(leo)[0]
    with open(path, 'w', newline='') as csvfile:
        fieldnames = ['Full path', 'Relative path', 'class']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        loop_for_writing(writer, list_full_path_images_tiger, list_relative_path_images_tiger,
                         list_full_path_images_leopard, list_relative_path_images_leopard,
                         tig, leo)


def copy_dataset(animal): # по animal копируется все содержимое в new_dataset
    dataset_path, new_dataset = f"dataset/{animal}", "new_dataset"
    if not os.path.exists(new_dataset):
        os.mkdir(new_dataset)

    image_list = os.listdir(dataset_path)
    for image in image_list:
        shutil.copy(f'{dataset_path}/{image}', f'{new_dataset}/{animal}_{image.split(".")[0]}.jpg')


def main_second():
    copy_dataset(tig)
    copy_dataset(leo)
    annotation_maker('new_dataset/1new_dataset_annotation.csv')


if __name__ == "__main__":
    # main_first()

    main_second()

























