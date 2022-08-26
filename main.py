from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
from datetime import date

from house import House

features = ["construction year", "building condition", "street frontage width", "number of frontages", "living area",
            "bedrooms", "bathrooms", "kitchen surface", "toilets", "basement", "attic", "primary energy consumption",
            "energy class", "heating type", "surface of the plot"]


def get_links():
    all_links = driver.find_elements(By.TAG_NAME, 'a')
    all_links = list(filter(lambda x: x.get_attribute("href") is not None, all_links))
    return list(
        filter(lambda x: "for-sale" in x.get_attribute("href") and "searchId" in x.get_attribute("href"), all_links))


def transform_specs(specs):
    specs_map = {}
    for feature in features:
        for spec in specs:
            if feature in spec.lower():
                specs_map[feature] = spec.lower().split(feature)[-1]
                break
    return specs_map


def get_next():
    all_links = driver.find_elements(By.TAG_NAME, 'a')
    all_links = list(filter(lambda x: x.get_attribute("href") is not None, all_links))
    return list(filter(lambda x: "next" in x.text.lower(), all_links))


def get_price():
    return driver.find_element(By.CLASS_NAME, "classified__price").text.split("\n")[-1]


def get_specs():
    specs = driver.find_elements(By.CLASS_NAME, "classified-table__row")
    specs = list(map(lambda spec: spec.text, specs))
    return transform_specs(specs)


def get_address():
    return driver.find_element(By.CLASS_NAME, 'classified__information--address').text


headers = ["price", "construction year", "building condition", "street frontage width (m)", "number of frontages",
           "living area (m²)", "bedrooms", "bathrooms", "kitchen surface (m²)", "toilets", "basement", "attic",
           "primary energy consumption (kwh/m²)", "energy class", "heating type", "surface of the plot (m²)", "address",
           "date"]

with open('data.csv', 'w', ) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    DRIVER_PATH = '/Users/sarrazin/GIT/immowebscraping/chromedriver/chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(
        'https://www.immoweb.be/en/search/house/for-sale/kortrijk/district?countries=BE&page=1&orderBy=relevance')
    house_list = []
    links_for_house = get_links()
    driver.get(links_for_house[0].get_attribute("href"))
    n = get_next()
    counter = 1
    while len(n) != 0:
        print("Number " + str(counter))
        time.sleep(1)
        address = get_address()
        price = get_price()
        specs = get_specs()
        house = House(price, address, specs)
        house_row = [house.get_price()] + list(map(lambda feature: house.get_spec(feature), features)) + [
            house.address] + [date.today()]
        if "from" not in house.price.lower():
            writer.writerow(house_row)
        driver.get(n[0].get_attribute("href"))
        n = get_next()
        counter += 1
    driver.close()
