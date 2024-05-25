
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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def getTheData(projectLink, founderLinks, dateOfPosting):
    url = "https://api.apify.com/v2/acts/lhotanova~product-hunt-profile-scraper/run-sync-get-dataset-items?token=apify_api_m6MWCkR27D3lhenLdTPIKdrXw6gLon08aF9V"
    input_data = {
        "profileUrls": founderLinks
    }

    logging.info("Sending request to Apify API")
    response = requests.post(url, json=input_data)

    if response.status_code != 200 and response.status_code != 201:
        logging.error(f"Error: Received status code {response.status_code}")
        return

    try:
        dataset_items = response.json()
    except ValueError:
        logging.error("Failed to parse JSON response")
        logging.debug("Response content: %s", response.text)
        return

    if not isinstance(dataset_items, list):
        logging.error("Unexpected data format: %s", dataset_items)
        return

    main_ref = db.reference('/projects')
    logging.info("Retrieved main Firebase reference")

    # Get the current data from Firebase to check for duplicates
    existing_projects = main_ref.get() or {}
    logging.info("Fetched existing projects from Firebase")

    project_ids = {}
    nameOfProject = ""
    for profile_data in dataset_items:
        project_name = projectLink.split("/")[-1].split("#")[0]
        logging.info("Processing project: %s", project_name)

        if project_name in existing_projects:
            logging.info("Project %s already exists, skipping...", project_name)
            continue

        try:
            profile_id = profile_data['id']
        except (KeyError, TypeError):
            logging.error("Error processing profile data: %s", profile_data)
            continue

        if project_name in project_ids and profile_id in project_ids[project_name]:
            logging.info("Profile %s already exists under project %s, skipping...", profile_id, project_name)
            continue

        project_ref = main_ref.child(project_name)
        profile_ref = project_ref.child(profile_id)

        logging.info("Project Name is %s", project_name)

        profile_ref.set(profile_data)
        project_ref.update({'date': dateOfPosting})
        logging.info("Profile data and date uploaded for project %s", project_name)

        if project_name in project_ids:
            project_ids[project_name].add(profile_id)
        else:
            project_ids[project_name] = {profile_id}
        nameOfProject = project_name

    logging.info("The project name is %s", nameOfProject)
    logging.info("Profiles uploaded successfully to Firebase Realtime Database.")

 

# Set Chrome options
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

# Loop to click on each item




time.sleep(5)
# for i in range(1, 200):
#     xpath = '//*[@id="__next"]/div/main/div/div[2]/div[' + str(i) + ']/div/div[1]/a[1]/div'
#     try:
#         WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, xpath)))
#         print(i)
#     except:
#         print("bad element")
#     height = driver.execute_script("return document.body.scrollHeight")
#     print(height)

#     scrollDown()
#     time.sleep(0.2)

day = 1
while True:
    time.sleep(3)
    driver.get('https://www.producthunt.com/leaderboard/daily/2024/5/'+str(day)+'/all')
    time.sleep(3)
    
    first = 1
    howManydaysWithoutProduct = 0
    for i in range(1, 300):  # Assuming there are maximum 300 launches in a day
        if howManydaysWithoutProduct > 5:
            break
        height = driver.execute_script("return document.body.scrollHeight")
        print("We're at ", i, "and page height is", height)
        if first == 1:
            time.sleep(5)
            first = 2
        xpath = '//*[@id="__next"]/div/main/div/div[2]/div[' + str(i) + ']/div/div[1]/a[1]/div'
        

        # Find the element of project
        haveWeFoundAProduct = True
        time.sleep(2)
        try:
            # Wait until the project element is clickable
            WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element = driver.find_element(By.XPATH, xpath)
            # Click on the element
            element.click()
            howManydaysWithoutProduct = 0

        except :
            haveWeFoundAProduct= False


        if haveWeFoundAProduct == False:
            howManydaysWithoutProduct = howManydaysWithoutProduct + 1
            continue
        # Wait a little bit for the page to load
        time.sleep(2)
        potentialLinks = []
        projectLink = ""
        haveWeFoundSomeone = False
        
        for j in range(3, 60):  #Checking up to 57 founders for each project
            next_xpath = '//*[@id="about"]/div[3]/div[' + str(j) + ']'
            try:
                if i > 17:
                    next_xpath = '//*[@id="about"]/div[2]/div[' + str(j-1) + ']'

                WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, next_xpath)))

                next_element = driver.find_element(By.XPATH, next_xpath)

                    
                #next_a_element = next_element.find_element(By.TAG_NAME, 'a')
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
        # Wait for the page to load after navigating back
        for link in potentialLinks:
            if "@" in str(link):
                print(link)

                founderLinks.append("https://www.producthunt.com/"+str(link))


        dateOfPosting = str(day)+"/05/2024"

        if haveWeFoundSomeone == True and len(founderLinks)>0:

            app = initScrapper()
            getTheData(projectLink, founderLinks, dateOfPosting)
            closeConnectionScrapper(app)
        time.sleep(1)

    day = day + 1
        
            
    

    