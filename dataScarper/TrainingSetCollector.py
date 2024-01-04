import time
import requests
from bs4 import BeautifulSoup

import CONFIG
teamsData_dict = CONFIG.teamsData_dict
URL_dict = CONFIG.URL_dict

"""
dict for every team has an array of data
[0:19] = results of last 20 matches (-1 = L, D = 0, W = 1). last match -> first match
[20:39] = scored goals for every last matches. last match -> first match
[40:59] = away goals for every last matches. last match -> first match
[60:79] = home or away for last 20 matches (-1 = Away, 1 = Home). last match -> first match
"""

def get_datas():
    for team in teamsData_dict.keys():
        page = requests.get(URL_dict.get(team))
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find("table", id="matchlogs_for")
        rows = table.find_all("tr")
        # print(rows)

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

        # getting the scored goals for every match
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
