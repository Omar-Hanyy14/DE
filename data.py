import requests
import os
from dotenv import load_dotenv
import json
import csv

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
# top_six_teams = [57, 66, 61, 65, 64, 73]
top_six_teams = {
                 "Arsenal": 57,
                 "Tottenham": 73,
                 "Chelsea": 61,
                 "Liverpool": 64,
                 "Man Utd": 66,
                 "Man City": 65 
                 }

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
    
    return matches

def analyze_matches(match, team_id):
    home_team_id = match['homeTeam']['id']
    away_team_id = match['awayTeam']['id']
    winner = match['score']['winner']
    home_score = match['score']['fullTime']['home']
    away_score = match['score']['fullTime']['away']

    if team_id == home_team_id:
        if winner == "HOME_TEAM":
            return "Win", "Home", home_score, away_score
        elif winner == "AWAY_TEAM":
            return "Loss", "Home", home_score, away_score
        else:
            return "Draw", "Home", home_score, away_score
    else:
        if winner == "AWAY_TEAM":
            return "Win", "Away",  home_score, away_score
        elif winner == "HOME_TEAM":
            return "Loss", "Away", home_score, away_score
        else:
            return "Draw", "Away", home_score, away_score
        
        
all_team_data = {}

for team_name, team_id in top_six_teams.items(): #.items method returns tuples that are iterable, we can unpack them into vars
    print(f"\n-{team_name}-")
    matches = get_matches(team_id)
    
    processed_matches = []

    for match in matches:
        result, venue, home_score, away_score = analyze_matches(match, team_id)
        opponent = match['awayTeam']['name'] if team_id == match['homeTeam']['id'] else match['homeTeam']['name']
        match_data = {
            "team": team_name,
            "result": result,
            "venue": venue,
            "opponent": opponent, 
            "home_score": home_score,
            "away_score": away_score,
            "date": match['utcDate'],
            "matchday": match['matchday'],
            "competition": match['competition']['name']
        }    
        processed_matches.append(match_data)
        print(f"{team_name}: {result} ({venue}) vs {opponent}")

    all_team_data[team_name] = processed_matches

print("Saving data to json...")

with open('top_six_matches.json', 'w') as f:
    json.dump(all_team_data, f, indent=2)

print("Data saved to 'top_six_matches.json'")

print("\nSaving data to CSV...")

csv_data = []
for team_name, matches in all_team_data.items():
    for match in matches:
        csv_data.append(match)

with open('top_six_matches.csv', 'w', newline='') as f:
    if csv_data:  # Make sure we have data
        fieldnames = csv_data[0].keys()  # Get column names from first row
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)

print("Data saved to 'top_six_matches.csv'")