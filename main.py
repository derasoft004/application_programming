import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request


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


for i in range(5):
    if len(full_list_tiger) <= 1000:
        make_driver_with_link(URLs_tiger[i], "//img[@class='serp-item__thumb justifier__thumb']", "tiger")
        time.sleep(10)
    if len(full_list_leopard) <= 1000:
        make_driver_with_link(URLs_leopard[i], "//img[@class='serp-item__thumb justifier__thumb']", "leopard")
        time.sleep(10)


if not os.path.exists('dataset'): os.mkdir('dataset')
if not os.path.exists('dataset/tiger'): os.mkdir('dataset/tiger')
if not os.path.exists('dataset/leopard'): os.mkdir('dataset/leopard')


def make_name(value):
    return '0'*(4-len(str(value))) + str(value)
def save_pictures():
    global full_list_tiger, full_list_leopard
    directory_tiger, directory_leopard = "dataset/tiger", "dataset/leopard"
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

save_pictures()