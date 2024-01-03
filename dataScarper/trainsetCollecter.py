import time

import requests
from bs4 import BeautifulSoup

"""
dict for every team has an array of data
[0:20] = results of last 20 matches (-1 = L, D = 0, W = 1). last match -> first match
[21:40] = scored goals for every last matches. last match -> first match
[41:60] = away goals for every last matches. last match -> first match
[61:80] = home or away for last 20 matches (-1 = Away, 1 = Home). last match -> first match
"""

teamsData_dict = {
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

URL_dict = {
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

def get_datas():
    for team in teamsData_dict.keys():
        page = requests.get(URL_dict.get(team))
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find("table", id="matchlogs_for")
        rows = table.find_all("tr")
        #print(rows)

        # getting the last 20 matches' result data for each team
        print(f"\n{team}")
        for row in range(1, 21):
            result = rows[row].find("td", class_="center")

            match result.text:
                case "W":
                    teamsData_dict.get(team).append(1)
                case "D":
                    teamsData_dict.get(team).append(0)
                case "L":
                    teamsData_dict.get(team).append(-1)
            print(result.text, end=" "),
        time.sleep(0.1)

        #getting the scored goals for every match
        print("")
        for row in range(1, 21):
            result = rows[row].find_all("td", class_="right")
            print(result[1].text, end=" "),

            if result[1].text == "":
                teamsData_dict.get(team).append(-1)
            else:
                teamsData_dict.get(team).append(int(result[1].text))

        # getting the conceded goals for every match
        print("")
        for row in range(1, 21):
            result = rows[row].find_all("td", class_="right")
            print(result[2].text, end=" "),

            if result[2].text == "":
                teamsData_dict.get(team).append(-1)
            else:
                teamsData_dict.get(team).append(int(result[2].text))

        # getting the venue for every match
        print("")
        for row in range(1, 21):
            result = rows[row].find_all("td", class_="left")
            match result[2].text:
                case "Home":
                    teamsData_dict.get(team).append(1)
                    print("H", end=" "),
                case "Away":
                    teamsData_dict.get(team).append(-1)
                    print("A", end=" "),