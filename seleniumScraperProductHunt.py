
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time










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



def getTheData(projectLink, founderLinks):    
    # Define the URL for running the actor synchronously
    url = "https://api.apify.com/v2/acts/lhotanova~product-hunt-profile-scraper/run-sync-get-dataset-items?token=apify_api_idXFjAfQnn8AQcPIN1cWCAowPc39EJ0do8YL"

    # Define the input data (profile URLs)
    
    input_data = {
    "profileUrls": founderLinks}

    response = requests.post(url, json=input_data)
    # Make a POST request to run the actor synchronously with input data
    # Extract the dataset items from the response
    dataset_items = response.json()

    # Get a reference to your main node in the Firebase Realtime Database
    main_ref = db.reference('/projects')

    # Loop through each profile data and upload them under 'profiles' node
    project_ids = {}
    for profile_data in dataset_items:
        # Extract project name from the project link
        project_name = projectLink.split("/")[-1].split("#")[0]

        # Get the ID of the current profile
        try:
            profile_id = profile_data['id']
        except:
            print("Something Fucked Up in the DB process")
            break

        # Check if the project already exists in the dictionary
        if project_name in project_ids:
            # Check if the profile ID is already used in the project
            if profile_id in project_ids[project_name]:
                print(f"Profile {profile_id} already exists under project {project_name}, skipping...")
                continue

        # Create a new child node under the main node for the project if it doesn't exist
        if not main_ref.child(project_name).get():
            project_ref = main_ref.child(project_name)
        else:
            project_ref = main_ref.child(project_name)

        # Create a new child node under the project node for the profile
        profile_ref = project_ref.child(profile_id)

        # Set the profile data
        profile_ref.set(profile_data)

        # Add the profile ID to the set of used IDs for the project
        if project_name in project_ids:
            project_ids[project_name].add(profile_id)
        else:
            project_ids[project_name] = {profile_id}



    print("Profiles uploaded successfully to Firebase Realtime Database.")




# Set the path to the Chrome WebDriver executable


# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Optional: run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-sh-usage")


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
time.sleep(3)
driver.get('https://www.producthunt.com/leaderboard/monthly/2024/1')
time.sleep(3)

def is_visible(element):
    return element.is_displayed() and element.is_enabled()

# Function to scroll down to the bottom of the page

# Navigate to the page


# Pause for initial loading
time.sleep(5)


def scrollDown():
    window_height = driver.execute_script("return window.innerHeight;")
    
    # Scroll down by 10% of the window height
    scroll_amount = int(window_height * 0.1)
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")

# Loop to click on each item
first = 0
while True:
    # Go trough first 1000 projects
    for i in range(1, 1000):  # Assuming there are 84 elements on the page
        print("We're at ", i)
        if first == 0:
            time.sleep(5)
            first = 1
        xpath = '//*[@id="__next"]/div/main/div/div[2]/div[' + str(i) + ']/div/div[1]/a[1]/div'
       
        attempt = 0
        # Find the element of project
        haveWeFoundAProduct = True
        while attempt < 3:
            try:
                # Wait until the project element is clickable
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                element = driver.find_element(By.XPATH, xpath)
                # Click on the element
                element.click()
                break  # Break the loop if click succeeds

            except :
                # Increment the attempt counter
                attempt += 1

                if attempt < 3:
                    print(f"Click intercepted. Retrying in 2 seconds (attempt {attempt}/{3})...")
                    time.sleep(2)  # Wait for 5 seconds before retrying
                else:
                    haveWeFoundAProduct= False
                    print("Maximum retry attempts reached for this element. Continuing with next element...")
                    continue
        if haveWeFoundAProduct == False:
            continue
        # Wait a little bit for the page to load
        time.sleep(2)
        potentialLinks = []
        projectLink = ""
        haveWeFoundSomeone = False
        
        for j in range(3, 60):  #Checking up to 57 founders for each project
            next_xpath = '//*[@id="about"]/div[3]/div[' + str(j) + ']'

            try:
                print(1)
                WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, next_xpath)))
                print(2)
                next_element = driver.find_element(By.XPATH, next_xpath)
                print(3)

                next_a_element = next_element.find_element(By.TAG_NAME, 'a')
                nextFounderLink = next_a_element.get_attribute("href")
                potentialLinks.append(nextFounderLink)
                projectLink = driver.current_url
                time.sleep(1)
                print(4)
                haveWeFoundSomeone = True
                #Now were in the founders profile
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
                founderLinks.append(str(link))
        if haveWeFoundSomeone == True and len(founderLinks)>0:
            app = initScrapper()
            getTheData(projectLink, founderLinks)
            closeConnectionScrapper(app)
        time.sleep(1)
        
            
        


    
    # Scroll down to load more items


    