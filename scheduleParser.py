from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import time

# constant for selenium
s = Service("geckodriver.exe")
driver = webdriver.Firefox(service=s)


# minor function
def get_source_html(url):
    try:
        driver.get(url=url)
        time.sleep(4)
        with open("html-files/site_practik.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as _ex:
        print(_ex)


def get_names_and_urls(file_path, status_station):  # 0 - отправление 1 - обратный
    with open(file_path, "r", encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")

    if status_station:
        items_div = soup.find("div", {"id": "tripB"})
    else:
        items_div = soup.find("div", {"id": "tripA"})

    names = []
    urls = []
    items_name = items_div.find_all("a", class_="list-group-item")
    for item in items_name:
        item_name = item.find("h6").get_text()
        item_url = item.get('href')
        names.append(item_name)
        urls.append(item_url)

    with open("txt-files/names.txt", "w", encoding="utf-8") as file:
        for name in names:
            file.write(f"{name}\n")

    with open("txt-files/urls.txt", "w", encoding="utf-8") as file:
        for url in urls:
            file.write(f"{url}\n")


def get_urls(file_path, number):
    with open(file_path, "r", encoding="utf-8") as file:
        urls = [["https://minsktrans.by/lookout_yard/Home/Index/region" + url.strip()] for url in file.readlines()]
        string = str(*urls[number - 1])
    return string


def get_selected_page(url):
    try:
        driver.get(url=url)
        time.sleep(4)
        with open("html-files/station.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as _ex:
        print(_ex)
    # finally:
    #     driver.close()
    #     driver.quit()


def get_schedule(file_path):
    with open(file_path, "r", encoding="UTF-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    items_div = soup.find("div", class_="section-schedule")
    times = []
    items_name = items_div.find("table", {"id": "schedule"})
    table_rasp = items_name.find_all("tr", class_="ng-scope")
    for tr in table_rasp:
        hour = tr.find("b").get_text()
        minutes = tr.find("span").get_text()
        times.append(f"{hour} часов {minutes} минут")
    return times


# main function
def get_main_file(status_route):
    get_source_html(url="https://minsktrans.by/lookout_yard/Home/Index/region#/routes/bus/223")
    get_names_and_urls("html-files/stations.html", status_route)


def get_schedule_station(number_station):
    path = get_urls("txt-files/urls.txt", number_station)
    get_selected_page(path)
    times = get_schedule("html-files/station.html")
    string = ''

    with open("txt-files/names.txt", 'r', encoding="utf-8") as file:
        names = [[name.strip()] for name in file.readlines()]
        string += f"{str(*names[number_station - 1])}\n"
    for i in range(len(times)):
        string += f"{i + 1}: {str(times[i])} \n"
    return string
