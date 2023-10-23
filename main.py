import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request
import csv


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


def main():
    for i in range(5):
        if len(full_list_tiger) <= 1000:
            make_driver_with_link(URLs_tiger[i], "//img[@class='serp-item__thumb justifier__thumb']", "tiger")
            time.sleep(10)
        if len(full_list_leopard) <= 1000:
            make_driver_with_link(URLs_leopard[i], "//img[@class='serp-item__thumb justifier__thumb']", "leopard")
            time.sleep(10)
    save_pictures()


def list_dataset(animal):
    return [f'{os.getcwd()}/dataset/{animal}/{x}' for x in os.listdir(f'dataset/{animal}')], [f'dataset/{animal}/{x}' for x in os.listdir(f'dataset/{animal}')]


# def get_length(element):
#     return int(element.split('.')[0])
# def get_length_after_split(element):
#     return int(element.split('/')[-1].split('.')[0])
# def sort_path_list(path_list: list, type_):
#     if type_: return path_list.sort(key=get_length)
#     else: return path_list.sort(key=get_length_after_split)


def loop_for_writing(csvfile, full_list_: list, list_: list,  animal):
    for i in range(len(list_)):
        csvfile.writerow({'Full path': full_list_[i], 'Relative path': list_[i], 'class': animal})


def open_and_write(animal, listf, listr):
    with open(f'dataset/{animal}/annotation.csv', 'w', newline='') as csvfile:
        fieldnames = ['Full path', 'Relative path', 'class']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        loop_for_writing(writer, listf, listr, animal)


def annotation_maker():
    tig, leo = 'tiger', 'leopard'
    list_relative_path_images_tiger, list_relative_path_images_leopard = \
        list_dataset(tig)[1], list_dataset(leo)[1]
    list_full_path_images_tiger, list_full_path_images_leopard = \
        list_dataset(tig)[0], list_dataset(leo)[0]
    # open_and_write(tig, list_full_path_images_tiger, list_relative_path_images_tiger)
    # open_and_write(leo, list_full_path_images_leopard, list_relative_path_images_leopard)





if __name__ == "__main__":
    annotation_maker()
    # main()






















