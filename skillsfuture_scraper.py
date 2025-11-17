import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random

def scrape():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)

    # Each page has 24 courses. 
    # there are 1214 pages
    page_list = [x*24 for x in range(0, 1214)]
    for page_no in page_list:
        url = r"""https://www.myskillsfuture.gov.sg/content/portal/en/portal-search/portal-search.html?fq=Course_Supp_Period_To_1%3A%5B2025-11-10T00%3A00%3A00Z%20TO%20*%5D&fq=IsValid%3Atrue&q=*%3A*"""
        if page_no!=0:
            url += f"&start={page_no}"
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        with open("skillsfuture.txt", "a", encoding="utf-8") as f:
            f.write(html)
        print(page_no/24, "out of 1214 done.")

def scrape_course_info():
    # randomly select 1000 courses and download their information as a html page
    courses_pdf = pd.read_csv("AI Champions/skillsfuture_cleaned.csv")
    courses_pdf = courses_pdf.drop_duplicates(subset=["course_title"]).reset_index(drop=True)
    random.seed(22691)
    random_list = sorted(random.sample(range(0, len(courses_pdf)), 1100))
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    new_j = 274
    j=new_j
    for i in random_list[new_j:]:
        course_url = courses_pdf.iloc[i]["course_url"]
        course_title = courses_pdf.iloc[i]["course_title"]
        for invalid_token in [":", "/", "@"]:
            course_title = course_title.replace(invalid_token, " ")
        print(course_title)
        url = rf"""https://www.myskillsfuture.gov.sg{course_url}"""
        try:
            driver.get(url)
            time.sleep(7)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            with open(f"AI Champions/project folder/Project Documents/{course_title}.html", "w", encoding="utf-8") as f:
                f.write(html)
            print(j, "out of 1000 done.")
        except:
            print("Selenium Error")
        j+=1

if __name__ == "__main__":
    # scrape()
    scrape_course_info()