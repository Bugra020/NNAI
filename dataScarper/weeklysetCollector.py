import time
import requests
from bs4 import BeautifulSoup

import CONFIG
teamsData_dict = CONFIG.teamsData_dict
URL_dict = CONFIG.URL_dict
weekdate = CONFIG.weeknumber

"""
each matchs data set is 44 length

[0:4] home last 5 match result
[5:9] home last 5 match goals scored
[10:14] home last 5 match goals conceded
[15:19] home last 5 h/a
[20] home avg goals scored
[21] home avg goals conceded

[22:26] away last 5 match result
[27:31] away last 5 match goals scored
[32:36] away last 5 match goals conceded
[37:41] away last 5 h/a
[42] away avg goals scored
[43] away avg goals conceded

"""


class Collector:

    def __init__(self):
        self.fixtures = 'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures'
        self.matches_html = 0
        self.final_data = []

    # look all the table rows' find the wanted week's matches
    def get_data_set(self):
        page = requests.get(self.fixtures)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find("tbody")
        rows = table.find_all("tr")
        time.sleep(0.5)

        self.matches_html = 0
        for row in rows:
            game_week = row.find("th")  # gives week number

            opposings = []  # array for teams

            if game_week.text is not None:
                if int(game_week.text) == self.week_index:
                    self.matches_html += 1

                    hometeam = row.find_all("td", class_="right")[1].find("a").text
                    time.sleep(0.5)
                    awayteam = row.find_all("td", class_="left")[2].find("a").text
                    time.sleep(0.5)

                    match hometeam:
                        case "Nott'ham Forest":
                            opposings.append("Nottingham Forest")
                        case "Tottenham":
                            opposings.append("Tottenham Hotspur")
                        case "Sheffield Utd":
                            opposings.append("Sheffield")
                        case "Manchester Utd":
                            opposings.append("Manchester United")
                        case "Newcastle Utd":
                            opposings.append("Newcastle")
                        case _:
                            opposings.append(hometeam)

                    match awayteam:
                        case "Nott'ham Forest":
                            opposings.append("Nottingham Forest")
                        case "Tottenham":
                            opposings.append("Tottenham Hotspur")
                        case "Sheffield Utd":
                            opposings.append("Sheffield")
                        case "Manchester Utd":
                            opposings.append("Manchester United")
                        case "Newcastle Utd":
                            opposings.append("Newcastle")
                        case _:
                            opposings.append(awayteam)

                    self.get_match(opposings)

                if self.matches_html == 10:
                    break

                time.sleep(0.5)

    # get teams' data for every match
    def get_match(self, arg_opposings):

        opposingUrls = []
        opposingUrls.append(URL_dict.get(arg_opposings[0]))
        opposingUrls.append(URL_dict.get(arg_opposings[1]))

        matchdata = []

        for teamurl in opposingUrls:
            page = requests.get(teamurl)
            soup1 = BeautifulSoup(page.content, "html.parser")
            table = soup1.find("table", id="matchlogs_for")
            time.sleep(0.5)

            rows = table.find_all("tr")
            time.sleep(0.5)

            # getting the last 5 matches' result data for each team
            for row in range(weekdate-5, weekdate):
                result = rows[row].find("td", class_="center")

                match result.text:
                    case "W":
                        matchdata.append(1)
                    case "D":
                        matchdata.append(0)
                    case "L":
                        matchdata.append(-1)
            time.sleep(0.5)

            # getting the scored goals for every match and average
            avg_scored = 0
            for row in range(weekdate-5, weekdate):
                result = rows[row].find_all("td", class_="right")

                if result[1].text == "":
                    matchdata.append(-1)
                    avg_scored += -1
                else:
                    matchdata.append(int(result[1].text))
                    avg_scored += int(result[1].text)
            avg_scored /= 5
            time.sleep(0.5)

            # getting the conceded goals for every match and average
            avg_conceded = 0
            for row in range(weekdate-5, weekdate):
                result = rows[row].find_all("td", class_="right")

                if result[2].text == "":
                    matchdata.append(-1)
                    avg_conceded += -1
                else:
                    matchdata.append(int(result[2].text))
                    avg_conceded += int(result[2].text)
            avg_conceded /= 5
            time.sleep(0.5)

            # getting the venue for every match
            for row in range(weekdate-5, weekdate):
                result = rows[row].find_all("td", class_="left")
                match result[2].text:
                    case "Home":
                        matchdata.append(1)
                    case "Away":
                        matchdata.append(-1)
            time.sleep(0.5)

            # adding the avg goal last 5
            matchdata.append(avg_scored)
            matchdata.append(avg_conceded)

        self.final_data.append(matchdata)
