from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import firebase_admin
from firebase_admin import credentials, db
import os

def init_scraper():
    cred = credentials.Certificate(r"C:\Users\Rihards\Desktop\gothAI\DMResponder\producthuntscraper-firebase-adminsdk-o82so-12e0513927.json")
    app = firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://producthuntscraper-default-rtdb.europe-west1.firebasedatabase.app/'
    })
    return app

def close_connection_scraper(app):
    firebase_admin.delete_app(app)

def get_project_links():
    main_ref = db.reference('/projects')
    projects = main_ref.get()
    project_links = []
    for project_id in projects.keys():
        project_links.append(project_id)
    return project_links

def upload_scraped_data(project_id, scraped_data):
    main_ref = db.reference('/projects')
    project_ref = main_ref.child(project_id)
    project_ref.update(scraped_data)

def scrape_project_page(project_link):
    driver.get(project_link)
    time.sleep(3)  # Wait for the page to load
    success = True
    scraped_data = {}
    try:
        project_title = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]/div[2]/div[1]/h1').text
        scraped_data['title'] = project_title
        print(project_title)

        project_description = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/main/div/div/div[2]/div[2]').text
        scraped_data['description'] = project_description
        print(project_description)

        project_last_launch_element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/main/div/div/div[3]/div/div/div/div[3]/time')
        project_last_launch = project_last_launch_element.get_attribute('datetime')
        scraped_data['date'] = project_last_launch
        print(project_last_launch)

        project_website_element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div/div[1]/div/div[2]/a')
        project_website = project_website_element.get_attribute('href')
        scraped_data['website'] = project_website
        print(project_website)

        project_image_element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div/div[1]/div/div[1]/div[1]/img')
        project_image = project_image_element.get_attribute('src')
        scraped_data['image'] = project_image
        print(project_image)
    except Exception as e:
        print(f"Error scraping project")
        success = False

    return scraped_data, success

def main():
    app = init_scraper()
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")


    chrome_path = "/app/.chrome-for-testing/chrome-linux64/chrome"
    chromedriver_path = "/app/.chrome-for-testing/chromedriver-linux64/chromedriver"

    chrome_options.binary_location = chrome_path
    global driver
    # Initialize Chrome WebDriver with the ChromeDriver path and options
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # Initialize Chrome WebDriver

    # Open Google
    project_links = get_project_links()
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

    for project_link in project_links:
        project_name = project_link.split("/")[-1].split("#")[0]
        
        # Pause and wait for user input to continue
        time.sleep(2)
        #input("Press Enter to continue to the next project...")

        scraped_data, success = scrape_project_page(f"https://www.producthunt.com/products/{project_link}")
        if success == True:
            upload_scraped_data(project_link, scraped_data)
    
    driver.quit()
    close_connection_scraper(app)

if __name__ == "__main__":
    main()