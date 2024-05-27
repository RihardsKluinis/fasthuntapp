from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time





import logging




import requests


import firebase_admin
from firebase_admin import credentials, db
import os

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")



chrome_path = "/app/.chrome-for-testing/chrome-linux64/chrome"
chromedriver_path = "/app/.chrome-for-testing/chromedriver-linux64/chromedriver"

chrome_options.binary_location = chrome_path

# Initialize Chrome WebDriver with the ChromeDriver path and options
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
# Initialize Chrome WebDriver

# Open Google
driver.get('https://www.producthunt.com')
base_dir = os.path.dirname(os.path.abspath(__file__))
cookies_file = os.path.join(base_dir, 'credentials', 'producthunt_cookies.txt')

with open(cookies_file, 'r') as f:
    cookies = f.readlines()

# Parse and inject cookies into the session
for cookie in cookies:
    if not cookie.startswith("#"):  # Skip comment lines
        parts = cookie.strip().split('\t')
        if len(parts) >= 7:  # Ensure there are enough elements
            cookie_dict = {
                'domain': parts[0],
                'secure': parts[1] == 'TRUE',
                'path': parts[2],
                'httpOnly': parts[3] == 'TRUE',
                'expiry': int(parts[4]) * 1000,  # Convert to milliseconds
                'name': parts[5],
                'value': parts[6]
            }
            driver.add_cookie(cookie_dict)
        else:
            print("Skipping malformed cookie:", cookie.strip())

# Refresh the page to apply the cookies
driver.refresh()


# Navigate to the page

# Pause for initial loading
time.sleep(5)


driver.set_window_size(1920, 1080)

def scrollDown():
    window_height = driver.execute_script("return window.innerHeight;")
    # Scroll down by 10% of the window height
    scroll_amount = int(window_height * 0.11)
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
    print("the window height is", window_height, " And scroll amount is", scroll_amount)

# Firebase initialization functions
def initScrapper():
    cred = credentials.Certificate(r"C:\Users\Rihards\Desktop\gothAI\DMResponder\producthuntscraper-firebase-adminsdk-o82so-12e0513927.json")
    app = firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://producthuntscraper-default-rtdb.europe-west1.firebasedatabase.app/'
    })
    return app

def closeConnectionScrapper(app):
    firebase_admin.delete_app(app)

def getTheData(projectLink, founderLinks, dateOfPosting):    
    url = "https://api.apify.com/v2/acts/lhotanova~product-hunt-profile-scraper/run-sync-get-dataset-items?token=apify_api_0ivyOVbeaMX1Eza81T2cQWBnEP26hb3iJWGh"
    input_data = {"profileUrls": founderLinks}
    response = requests.post(url, json=input_data)
    dataset_items = response.json()
    main_ref = db.reference('/projects')
    project_ref = main_ref.child(projectLink)
    project_ref.child('date').set(dateOfPosting)
    
    for profile_data in dataset_items:
        profile_id = profile_data['id']
        profile_ref = project_ref.child(profile_id)
        profile_ref.set(profile_data)

    print("Profiles uploaded successfully to Firebase Realtime Database.")
    print(response.text)

def get_previous_date(day, month, year):
    day -= 1
    if day == 0:
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        if month in {1, 3, 5, 7, 8, 10, 12}:
            day = 31
        elif month in {4, 6, 9, 11}:
            day = 30
        elif month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                day = 29
            else:
                day = 28
    return day, month, year

day, month, year = 31, 3, 2024

while True:
    if year < 2023 or (year == 2023 and month == 1 and day < 1):
        break
    
    time.sleep(3)
    driver.get(f'https://www.producthunt.com/leaderboard/daily/{year}/{month}/{day}/all')
    time.sleep(3)

    first = 1
    howManydaysWithoutProduct = 0
    for i in range(1, 300):  # Assuming there are maximum 300 launches in a day
        if howManydaysWithoutProduct > 5:
            break
        height = driver.execute_script("return document.body.scrollHeight")
        print("We're at ", i, " page height is", height, "day is ", day, ", month is ", month, "and the year is ", year)
        if first == 1:
            time.sleep(5)
            first = 2
        xpath = '//*[@id="__next"]/div/main/div/div[2]/div[' + str(i) + ']/div/div[1]/a[1]/div'
        
        haveWeFoundAProduct = True
        time.sleep(2)
        try:
            WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element = driver.find_element(By.XPATH, xpath)
            element.click()
            howManydaysWithoutProduct = 0
        except:
            haveWeFoundAProduct = False

        if not haveWeFoundAProduct:
            howManydaysWithoutProduct += 1
            continue
        
        time.sleep(2)
        potentialLinks = []
        projectLink = ""
        haveWeFoundSomeone = False
        
        for j in range(3, 60):  # Checking up to 57 founders for each project
            next_xpath = '//*[@id="about"]/div[3]/div[' + str(j) + ']'
            try:
                if i > 17:
                    next_xpath = '//*[@id="about"]/div[2]/div[' + str(j-1) + ']'

                WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, next_xpath)))
                next_element = driver.find_element(By.XPATH, next_xpath)

                hrefs = driver.execute_script("""
                var element = arguments[0];
                var links = element.getElementsByTagName('*');
                var hrefs = [];
                for (var i = 0; i < links.length; i++) {
                    if (links[i].hasAttribute('href')) {
                        hrefs.push(links[i].getAttribute('href'));
                    }
                }
                return hrefs;
                """, next_element)

                for href in hrefs:
                    if href and "@" in href:
                        print(f"Found founder link with @: {href}")
                        potentialLinks.append(href)
                        projectLink = driver.current_url
                        time.sleep(1)
                        haveWeFoundSomeone = True
                        break  # Exit the inner loop if a valid link is found
                    else:
                        print(f"Found link does not contain @: {href}")

            except:
                print(f"that's it for now")
                backButton = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/a')
                backButton.click()
                break
            
            time.sleep(1)
        scrollDown()

        founderLinks = []
        for link in potentialLinks:
            if "@" in str(link):
                print(link)
                founderLinks.append("https://www.producthunt.com/" + str(link))

        dateOfPosting = f"{day:02d}/{month:02d}/{year}"

        if haveWeFoundSomeone and founderLinks:
            app = initScrapper()
            getTheData(projectLink, founderLinks, dateOfPosting)
            closeConnectionScrapper(app)
        time.sleep(1)

    day, month, year = get_previous_date(day, month, year)