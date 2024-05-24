
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

def initScrapper():
    # Get the directory of the current file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the credentials file
    cred_path = os.path.join(base_dir, 'credentials', 'producthuntscraper-firebase-adminsdk-o82so-12e0513927.json')
    cred = credentials.Certificate(cred_path)
    app = firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://producthuntscraper-default-rtdb.europe-west1.firebasedatabase.app/'
    })
    return app

def closeConnectionScrapper(app):
    firebase_admin.delete_app(app)


#def addToFirebaseScrapper(projectLink, founderLinks):



def getTheData(projects):
    url = "https://api.apify.com/v2/acts/lhotanova~product-hunt-profile-scraper/run-sync-get-dataset-items?token=apify_api_m6MWCkR27D3lhenLdTPIKdrXw6gLon08aF9V"
    
    for project in projects:
        projectLink, founderLinks, dateOfPosting = project
        
        input_data = {
            "profileUrls": founderLinks
        }

        response = requests.post(url, json=input_data)

        try:
            dataset_items = response.json()
        except ValueError:
            print("Failed to parse JSON response for project:", projectLink)
            continue

        print("Dataset Items for project:", projectLink, dataset_items)

        if not isinstance(dataset_items, list):
            print("Unexpected data format for project:", projectLink, dataset_items)
            continue

        main_ref = db.reference('/projects')

        project_ids = {}
        nameOfProject = ""
        for profile_data in dataset_items:
            project_name = projectLink.split("/")[-1].split("#")[0]

            try:
                profile_id = profile_data['id']
            except (KeyError, TypeError):
                print(f"Error processing profile data: {profile_data}")
                continue

            project_ref = main_ref.child(project_name)
            profile_ref = project_ref.child(profile_id)

            existing_projects = main_ref.get() or {}

            for profile_data in dataset_items:
                project_name = projectLink.split("/")[-1].split("#")[0]

                if project_name in existing_projects:
                    print(f"Project {project_name} already exists, skipping...")
                    continue


            print("Project Name is", project_name)
            logging.info("Project Name is", project_name)

            profile_ref.set(profile_data)
            project_ref.update({'date': dateOfPosting})

            if project_name in project_ids:
                project_ids[project_name].add(profile_id)
            else:
                project_ids[project_name] = {profile_id}
            nameOfProject = project_name

        print("The project name is", nameOfProject)
        print("Profiles uploaded successfully to Firebase Realtime Database.")

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

chrome_path = "/app/.chrome-for-testing/chrome-linux64/chrome"
chromedriver_path = "/app/.chrome-for-testing/chromedriver-linux64/chromedriver"
chrome_options.binary_location = chrome_path

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get('https://www.producthunt.com')

base_dir = os.path.dirname(os.path.abspath(__file__))
cookies_file = os.path.join(base_dir, 'credentials', 'producthunt_cookies.txt')

logging.basicConfig(level=logging.INFO)

with open(cookies_file, 'r') as f:
    cookies = f.readlines()

for cookie in cookies:
    if not cookie.startswith("#"):
        parts = cookie.strip().split('\t')
        if len(parts) >= 7:
            cookie_dict = {
                'domain': parts[0],
                'secure': parts[1] == 'TRUE',
                'path': parts[2],
                'httpOnly': parts[3] == 'TRUE',
                'expiry': int(parts[4]) * 1000,
                'name': parts[5],
                'value': parts[6]
            }
            driver.add_cookie(cookie_dict)
        else:
            print("Skipping malformed cookie:", cookie.strip())

driver.refresh()
time.sleep(5)
driver.set_window_size(1920, 1080)

def scrollDown():
    window_height = driver.execute_script("return window.innerHeight;")
    scroll_amount = int(window_height * 0.11)
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
    print("the window height is", window_height, " And scroll amount is", scroll_amount)

day = 1
projects = []
while True:
    time.sleep(3)
    driver.get('https://www.producthunt.com/leaderboard/daily/2023/5/' + str(day) + '/all')
    time.sleep(3)
    
    first = 1
    howManydaysWithoutProduct = 0
    for i in range(1, 300):
        if howManydaysWithoutProduct > 5:
            break
        height = driver.execute_script("return document.body.scrollHeight")
        print("We're at ", i, "and page height is", height)
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
        projectLink = driver.current_url
        haveWeFoundSomeone = False

        for j in range(3, 60):
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
                        haveWeFoundSomeone = True
                        break
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
                logging.info(link)
                founderLinks.append("https://www.producthunt.com/" + str(link))

        dateOfPosting = str(day) + "/05/2023"

        if haveWeFoundSomeone and founderLinks:
            projects.append((projectLink, founderLinks, dateOfPosting))

        if len(projects) >= 10:
            app = initScrapper()
            getTheData(projects)
            closeConnectionScrapper(app)
            projects = []

        time.sleep(1)

    if projects:
        app = initScrapper()
        getTheData(projects)
        closeConnectionScrapper(app)
        projects = []

    day += 1
    

    