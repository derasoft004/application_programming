import os
import time
import random
import cv2
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

if not os.path.exists('dataset'):
    os.mkdir('dataset')
if not os.path.exists('dataset/tiger'):
    os.mkdir('dataset/tiger')

def driver_scroller(driver_to_scroll, pix):
    sroll_range = 0
    while sroll_range < pix:
        driver_to_scroll.execute_script(f"window.scrollTo(0, {sroll_range});")  # ширина, высота
        sroll_range += 3  # скорость

full_list = []
count_pictures = 0

def print_driver():
    for i in range(len(full_list)):
        print(i, full_list[i].get_attribute('src'))
        if i == 1000-1: break

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

for i in range(1):
    make_driver_with_link(URLs[i], "//img[@class='serp-item__thumb justifier__thumb']")
    time.sleep(2)

print_driver()



# <img class="serp-item__thumb justifier__thumb" src="//avatars.mds.yandex.net/i?id=c70d0921910fddeadd2472175e09821dc812c505-10927571-images-thumbs&amp;n=13" data-error-handler="serpItemError" alt="Скачать картинку тигра\33." style="height: 185.8px; width: 279.5px;">
# while pictures_count < 1000:
#
#
#     URL = "https://yandex.ru/images/search?text=leopard"
#     page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
#                                      "Referer": 'https://www.google.ru/'},
#                        params={"text": "leopard"})
#     if page.status_code == 200:
#         print(page.url)
#         page_count += 1
#
#         soup = BeautifulSoup(page.text, 'html.parser')
#         images = soup.findAll('img')
#         for im in images:
#             pictures_count += 1
#             print('https:' + im.get("src"))
#         print(pictures_count)
#         time.sleep(random.randint(15, 21))





# прочтение изображения из файла, path_to_file - путь до файла-изображения
# cv2.imwrite(path_to_save_image, image)
# сохранение изображения по заданному пути, например, path_to_folder/image_name.jpg
#
# print(image.shape)  # распечатать размер прочитанного изображения
#
# # инструкции для просмотра изображения
# cv2.imshow(window_name, image)
# cv2.waitKey(0)


#
# url = "https://yandex.ru/images/search?text=tiger" # https://yandex.ru/images/search?lr=11135&text=tiger
# page = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
#
# # postik = requests.post(url, 'tiger')
# soup = BeautifulSoup(page.text, 'html.parser')
# print(soup)
# classes = soup.findAll('img', class_='serp-item__thumb justifier__thumb')
# print(len(classes))
# for i in classes:
#     print(i.text)

# class WebSiteMaker(object):
#     def __init__(self, page_name_continue):
#         self.text = page_name_continue
#
#
#     def make_link(self):
#         global url
#         return url + self.text


# page1 = WebSiteMaker('search?lr=11135&text=tiger').make_link()
# page_get = requests.get(page1, headers={"User-Agent":"Mozilla/5.0"})
# soup = BeautifulSoup(page_get.text, "html.parser")



# image = cv2.imread(path_to_file)  # прочтение изображения из файла, path_to_file - путь до файла-изображения
# cv2.imwrite(path_to_save_image, image)  # сохранение изображения по заданному пути, например, path_to_folder/image_name.jpg
#
# print(image.shape)  # распечатать размер прочитанного изображения
#
# # инструкции для просмотра изображения
# cv2.imshow(window_name, image)
# cv2.waitKey(0)


# import os
# import requests
# from bs4 import BeautifulSoup
# from PIL import Image
# from io import BytesIO
# import cv2
#
#
# if not os.path.exists('dataset'):
#     os.mkdir('dataset')
# if not os.path.exists('dataset/tiger'):
#     os.mkdir('dataset/tiger')
#
# url = 'https://yandex.ru/images/search'
#
# params = {'text': 'tiger'}
#
# desired_image_count = 1000
# current_image_count = 0
#
# page_number = 0
#
# while current_image_count < desired_image_count:
#     page_number += 1
#     # params['p'] = str(page_number)
#
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         images = soup.find_all('img')
#
#         for img in images:
#             img_url = img.get('src')
#             if img_url and img_url.startswith('https://'):
#
#                 image_data = requests.get(img_url)
#                 print(image_data)
#                 image_data_content = image_data.content
#                 i = Image.open(BytesIO(image_data_content))
#                 with open(f'dataset/tiger/image{current_image_count + 1}.jpg', 'wb') as img_file:
#                     img_file.write(image_data_content)
#                 current_image_count += 1
#
#                 if current_image_count >= desired_image_count:
#                     break
#
#         print(f'download {current_image_count} pic')
#     else:
#         print(f'error {page_number}')
#         break
#
# print('dawnload done')














































