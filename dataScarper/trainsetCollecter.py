import time

import requests
from bs4 import BeautifulSoup

"""
dict for every team has an array of data
[0:20] = results of last 20 matches (-1 = L, D = 0, W = 1)
[21:40] = scored goals for every last matches
[41:60] = away goals for every last matches
[61:80] = home or away for last 20 matches (-1 = A, 1 = H)
"""
"""
r = requests.get('https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures')
print(r.content)
page = requests.get(f"https://fbref.com/en/squads/18bb7c10/2023-2024/c9/Arsenal-Stats-Premier-League")
soup = BeautifulSoup(page.content, "html.parser")
table = soup.find("table", id="matchlogs_for")
matchResults = table.find_all("td", class_="center", csk="3")

rows = table.find_all("tr")
for row in range(1, 21):
    result = rows[row].find("td", class_="center")
    print(result.text, end="\n")
"""

teamsData = {
    "Arsenal": [],
    "Aston Villa": [],
    "Bournemouth": [],
    "Brentford": [],
    "Brighton & Hove Albion": [],
    "Burnley": [],
    "Chelsea": [],
    "Crystal Palace": [],
    "Everton": [],
    "Fulham": [],
    "Liverpool": [],
    "Luton Town": [],
    "Manchester City": [],
    "Manchester United": [],
    "Newcastle United": [],
    "Nottingham Forest": [],
    "Sheffield United": [],
    "Tottenham Hotspur": [],
    "West Ham United": [],
    "Wolverhampton Wanderers": []
}

# getting the last 20 matches' result data for each team

for team in teamsData.keys():
    page = requests.get(f"https://fbref.com/en/squads/18bb7c10/2023-2024/c9/{team}-Stats-Premier-League")
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("table", id="matchlogs_for")
    rows = table.find_all("tr")
    for row in range(1, 21):
        result = rows[row].find("td", class_="center")
        print(result.text, end="\n")
    time.sleep(1)