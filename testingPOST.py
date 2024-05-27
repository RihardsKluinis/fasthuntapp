import requests


import firebase_admin
from firebase_admin import credentials, db


import firebase_admin
from firebase_admin import credentials, db
import requests
from datetime import datetime

def initScrapperr():
    cred = credentials.Certificate(r"C:\Users\Rihards\Desktop\gothAI\DMResponder\producthuntscraper-firebase-adminsdk-o82so-12e0513927.json")
    app = firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://producthuntscraper-default-rtdb.europe-west1.firebasedatabase.app/'
    })
    return app

def closeConnectionScrapper(app):
    firebase_admin.delete_app(app)

# def addToFirebaseScrapper(projectLink, founderLinks):
# Implement your addToFirebaseScrapper function here if needed

def getTheData(projectLink, founderLinks):
    url = "https://api.apify.com/v2/acts/lhotanova~product-hunt-profile-scraper/run-sync-get-dataset-items?token=apify_api_0ivyOVbeaMX1Eza81T2cQWBnEP26hb3iJWGh"

    input_data = {
        "profileUrls": [
            founderLinks
        ]
    }
    response = requests.post(url, json=input_data)
    dataset_items = response.json()

    main_ref = db.reference('/projects')
    for profile_data in dataset_items:
        project_name = str(projectLink)
        project_ref = main_ref.child(project_name)
        profile_id = profile_data['id']
        profile_ref = project_ref.child(profile_id)
        profile_ref.set(profile_data)

    print("Profiles uploaded successfully to Firebase Realtime Database.")
    print(response.text)

def countData():
    app = initScrapperr()
    main_ref = db.reference('/projects')

    num_projects = 0
    num_profiles = 0

    projects_by_date = {}
    projects_without_date = 0

    for project_key, project_snap in main_ref.get().items():
        num_projects += 1
        project_date = project_snap.get('date', 'no_date')

        if project_date == 'no_date':
            projects_without_date += 1
        else:
            if project_date not in projects_by_date:
                projects_by_date[project_date] = 0
            projects_by_date[project_date] += 1

        for profile_snap in project_snap.values():
            num_profiles += 1

    closeConnectionScrapper(app)

    return num_projects, num_profiles, projects_by_date, projects_without_date

def main():
    num_projects, num_profiles, projects_by_date, projects_without_date = countData()

    print("Number of projects:", num_projects)
    print("Number of profiles:", num_profiles)
    print("Projects by date:")

    sorted_projects_by_date = sorted(
        projects_by_date.items(),
        key=lambda x: datetime.strptime(x[0], "%d/%m/%Y")
    )

    for date, count in sorted_projects_by_date:
        print(f"{date}: {count}")

    print("Projects without date:", projects_without_date)

if __name__ == "__main__":
    main()
