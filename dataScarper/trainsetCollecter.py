import time

import requests
from bs4 import BeautifulSoup

"""
dict for every team has an array of data
[0:20] = results of last 20 matches (-1 = L, D = 0, W = 1) last match -> first match
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
    "Burnley": [],
    "Sheffield": [],
    "Manchester City": [],
    "West Ham": [],
    "Luton Town": [],
    "Wolves": [],
    "Brighton": [],
    "Arsenal": [],
    "Brentford": [],
    "Fulham": [],
    "Bournemouth": [],
    "Nottingham Forest": [],
    "Newcastle": [],
    "Aston Villa": []
}

EPL_dict = {
    "Tottenham Hotspur": "https://fbref.com/en/squads/361ca564/2023-2024/matchlogs/c9/schedule/Tottenham-Hotspur-Scores-and-Fixtures-Premier-League",
    "Everton": "https://fbref.com/en/squads/d3fd31cc/2023-2024/matchlogs/c9/schedule/Everton-Scores-and-Fixtures-Premier-League",
    "Liverpool": "https://fbref.com/en/squads/822bd0ba/2023-2024/matchlogs/c9/schedule/Liverpool-Scores-and-Fixtures-Premier-League",
    "Chelsea": "https://fbref.com/en/squads/cff3d9bb/2023-2024/matchlogs/c9/schedule/Chelsea-Scores-and-Fixtures-Premier-League",
    "Crystal Palace": "https://fbref.com/en/squads/47c64c55/2023-2024/matchlogs/c9/schedule/Crystal-Palace-Scores-and-Fixtures-Premier-League",
    "Manchester United": "https://fbref.com/en/squads/19538871/2023-2024/matchlogs/c9/schedule/Manchester-United-Scores-and-Fixtures-Premier-League",
    "Burnley": "https://fbref.com/en/squads/943e8050/2023-2024/matchlogs/c9/schedule/Burnley-Scores-and-Fixtures-Premier-League",
    "Sheffield": "https://fbref.com/en/squads/1df6b87e/2023-2024/matchlogs/c9/schedule/Sheffield-United-Scores-and-Fixtures-Premier-League",
    "Manchester City": "https://fbref.com/en/squads/b8fd03ef/2023-2024/matchlogs/c9/schedule/Manchester-City-Scores-and-Fixtures-Premier-League",
    "West Ham": "https://fbref.com/en/squads/7c21e445/2023-2024/matchlogs/c9/schedule/West-Ham-United-Scores-and-Fixtures-Premier-League",
    "Luton Town": "https://fbref.com/en/squads/e297cd13/2023-2024/matchlogs/c9/schedule/Luton-Town-Scores-and-Fixtures-Premier-League",
    "Wolves": "https://fbref.com/en/squads/8cec06e1/2023-2024/matchlogs/c9/schedule/Wolverhampton-Wanderers-Scores-and-Fixtures-Premier-League",
    "Brighton": "https://fbref.com/en/squads/d07537b9/2023-2024/matchlogs/c9/schedule/Brighton-and-Hove-Albion-Scores-and-Fixtures-Premier-League",
    "Arsenal": "https://fbref.com/en/squads/18bb7c10/2023-2024/matchlogs/c9/schedule/Arsenal-Scores-and-Fixtures-Premier-League",
    "Brentford": "https://fbref.com/en/squads/cd051869/2023-2024/matchlogs/c9/schedule/Brentford-Scores-and-Fixtures-Premier-League",
    "Fulham": "https://fbref.com/en/squads/fd962109/2023-2024/matchlogs/c9/schedule/Fulham-Scores-and-Fixtures-Premier-League",
    "Bournemouth": "https://fbref.com/en/squads/4ba7cbea/2023-2024/matchlogs/c9/schedule/Bournemouth-Scores-and-Fixtures-Premier-League",
    "Nottingham Forest": "https://fbref.com/en/squads/e4a775cb/2023-2024/matchlogs/c9/schedule/Nottingham-Forest-Scores-and-Fixtures-Premier-League",
    "Newcastle": "https://fbref.com/en/squads/b2b47a98/2023-2024/matchlogs/c9/schedule/Newcastle-United-Scores-and-Fixtures-Premier-League",
    "Aston Villa": "https://fbref.com/en/squads/8602292d/2023-2024/matchlogs/c9/schedule/Aston-Villa-Scores-and-Fixtures-Premier-League"
}

# getting the last 20 matches' result data for each team
for team in teamsData.keys():
    page = requests.get(EPL_dict.get(team))
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("table", id="matchlogs_for")
    rows = table.find_all("tr")
    #print(rows)

    print(f"\n{team}")
    for row in range(1, 21):
        result = rows[row].find("td", class_="center")

        match result.text:
            case "W":
                teamsData.get(team).append(1)
            case "D":
                teamsData.get(team).append(0)
            case "L":
                teamsData.get(team).append(-1)

        print(result.text, end=" "),

    time.sleep(0.1)