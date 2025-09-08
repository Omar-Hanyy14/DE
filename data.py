import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("API_TOKEN")

if not token:
    raise RuntimeError("Missing API_Token in environment or .env file")

uri = 'https://api.football-data.org/v4/matches?season=2024&limit=5'
headers = {'X-Auth-Token' : os.getenv("API_TOKEN")} 

response = requests.get(uri, headers=headers)
print(f"Status code is: {response.status_code}")
print(f"Response keys are: {list(response.json().keys())}")
print(f"Number of matches: {len(response.json()['matches'])}")
top_six_teams = [57, 66, 61, 65, 64, 73]


def get_matches(team_id):
    uri = f"https://api.football-data.org/v4/teams/{team_id}/matches?competitions=PL&season=2024"
    response = requests.get(uri, headers=headers)
    data = response.json()
    
    result_set = data.get("resultSet", {})
    matches = data.get("matches", [])

    print(f"Team ID: {team_id}")
    print(f"Total number of matches {result_set.get('count', 0)}")
    print(f"Wins: {result_set.get('wins', 0)}")
    print(f"Draws: {result_set.get('draws', 0)}")
    print(f"Losses: {result_set.get('losses', 0)}")
    print(f"Matches returned: {len(matches)}")


for team_id in top_six_teams:
    get_matches(team_id)