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
    "Tottenham Hotspur": [],
    "Everton": [],
    "Liverpool": [],
    "Chelsea": [],
    "Crystal Palace": [],
    "Manchester United": [],
    "Leeds United": [],
    "Southampton": [],
    "Manchester City": [],
    "West Ham": [],
    "Leicester City": [],
    "Wolves": [],
    "Brighton": [],
    "Arsenal": [],
    "Brentford": [],
    "Burnley": [],
    "Norwich": [],
    "Watford": [],
    "Newcastle": [],
    "Aston Villa": []
}

EPL_dict = {
    "Tottenham Hotspur": "https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats",
    "Everton": "https://fbref.com/en/squads/d3fd31cc/Everton-Stats",
    "Liverpool": "https://fbref.com/en/squads/822bd0ba/Liverpool-Stats",
    "Chelsea": "https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats",
    "Crystal Palace": "https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats",
    "Manchester United": "https://fbref.com/en/squads/19538871/Manchester-United-Stats",
    "Leeds United": "https://fbref.com/en/squads/5bfb9659/Leeds-United-Stats",
    "Southampton": "https://fbref.com/en/squads/33c895d4/Southampton-Stats",
    "Manchester City": "https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats",
    "West Ham": "https://fbref.com/en/squads/7c21e445/West-Ham-United-Stats",
    "Leicester City": "https://fbref.com/en/squads/a2d435b3/Leicester-City-Stats",
    "Wolves": "https://fbref.com/en/squads/8cec06e1/Wolverhampton-Wanderers-Stats",
    "Brighton": "https://fbref.com/en/squads/d07537b9/Brighton-and-Hove-Albion-Stats",
    "Arsenal": "https://fbref.com/en/squads/18bb7c10/Arsenal-Stats",
    "Brentford": "https://fbref.com/en/squads/cd051869/Brentford-Stats",
    "Burnley": "https://fbref.com/en/squads/943e8050/Burnley-Stats",
    "Norwich": "https://fbref.com/en/squads/1c781004/Norwich-City-Stats",
    "Watford": "https://fbref.com/en/squads/2abfe087/Watford-Stats",
    "Newcastle": "https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats",
    "Aston Villa": "https://fbref.com/en/squads/8602292d/Aston-Villa-Stats"
}

# getting the last 20 matches' result data for each team
for team in teamsData.keys():
    page = requests.get(EPL_dict.get(team))
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("table", id="matchlogs_for")
    rows = table.find_all("tr")

    print(f"{team}\n")
    for row in range(1, 21):
        result = rows[row].find("td", class_="center")
        print(result.text),
    time.sleep(0.1)
