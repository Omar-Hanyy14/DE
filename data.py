import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
uri = 'https://api.football-data.org/v4/matches?season=2024&limit=5'
headers = {'X-Auth-Token' : os.getenv("api_token")} 

response = requests.get(uri, headers=headers)
print(f"Status code is: {response.status_code}")
print(f"Response keys are: {list(response.json().keys())}")
print(f"Number of matches: {len(response.json()['matches'])}")
top_six_teams = [57, 66, 61, 65, 64, 73]

for match in response.json()['matches']:
    print(match) 

if len(response.json()['matches']) == 0:
    print("No matches were found")
