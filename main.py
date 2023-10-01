import os
import time
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request


def driver_scroller(driver_to_scroll, pix):
    sroll_range = 0
    while sroll_range < pix:
        driver_to_scroll.execute_script(f"window.scrollTo(0, {sroll_range});")  # ширина, высота
        sroll_range += 3  # скорость


full_list = []
count_pictures = 0

URLs = ["https://ya.ru/images/search?from=tabbar&text=tiger",
        "https://ya.ru/images/search?from=tabbar&lr=11135&p=10&rpt=image&text=tiger",
        "https://ya.ru/images/search?from=tabbar&lr=11135&p=20&rpt=image&text=tiger",
        "https://ya.ru/images/search?from=tabbar&lr=11135&p=30&rpt=image&text=tiger"]

pictures_count, page_count = 0, 1

# def find_button_next_page(driver): не находит хотя кнопка есть
#     button = driver.find_element(By.XPATH, "//a[@class='button2 button2_size_l button2_theme_action button2_type_link button2_view_classic more__button i-bem button2_js_inited']")
#     print(button)


def make_driver_with_link(link, path_name):
    global full_list, count_pictures
    driver = webdriver.Chrome()
    driver.get(link)
    print(driver.title)
    time.sleep(4)
    driver_scroller(driver, 15000)
    list_pictures = driver.find_elements(By.XPATH, path_name)
    count_pictures += len(list_pictures)
    print(count_pictures)
    full_list += list_pictures


for i in range(4):
    make_driver_with_link(URLs[i], "//img[@class='serp-item__thumb justifier__thumb']")
    time.sleep(20)


if not os.path.exists('dataset'):
    os.mkdir('dataset')
if not os.path.exists('dataset/tiger'):
    os.mkdir('dataset/tiger')


def save_pictures():
    global full_list
    directory = "dataset/tiger"
    for i in range(len(full_list)):
        img = urllib.request.urlopen(full_list[i].get_attribute('src')).read()
        print(full_list[i].get_attribute('src'))
        out = open(f"{directory}/image{i+1}.jpg", "wb")
        out.write(img)
        out.close

save_pictures()













































