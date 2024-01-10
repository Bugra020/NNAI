import time
import requests
from bs4 import BeautifulSoup

import CONFIG

teamsData_dict = CONFIG.teamsData_dict
URL_dict = CONFIG.URL_dict

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

    def __init__(self):  # init method
        self.fixtures = 'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures'
        self.matches_html = 0
        self.final_data = []
        self.targets = []

    def get_data_set(self, weekdate):  # getting datas for specific match week
        page = requests.get(self.fixtures)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find("tbody")
        rows = table.find_all("tr")
        time.sleep(0.5)

        self.matches_html = 0
        for row in rows:
            game_week = row.find("th")  # gives week number

            opposings = []  # array for teams

            if game_week.text != "":
                if int(game_week.text) == weekdate:
                    self.matches_html += 1

                    hometeam = row.find_all("td", class_="right")[1].find("a").text
                    awayteam = row.find_all("td", class_="left")[2].find("a").text

                    self.get_targets(row)

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

                    self._get_match(opposings, weekdate)

                if self.matches_html == 10:
                    break

                time.sleep(0.1)

        return self.final_data

    # get teams' data for every match
    def _get_match(self, arg_opposings, weekdate):

        opposingUrls = []
        opposingUrls.append(URL_dict.get(arg_opposings[0]))
        opposingUrls.append(URL_dict.get(arg_opposings[1]))

        matchdata = []

        for teamurl in opposingUrls:
            page = requests.get(teamurl)
            soup1 = BeautifulSoup(page.content, "html.parser")
            table = soup1.find("table", id="matchlogs_for")
            time.sleep(0.1)

            rows = table.find_all("tr")

            # getting the last 5 matches' result data for each team
            for row in range(weekdate - 5, weekdate):
                result = rows[row].find("td", class_="center")

                match result.text:
                    case "W":
                        matchdata.append(1)
                    case "D":
                        matchdata.append(0)
                    case "L":
                        matchdata.append(-1)
                    case _:
                        matchdata.append(0)
            time.sleep(0.1)

            # getting the scored goals for every match and average
            avg_scored = 0
            for row in range(weekdate - 5, weekdate):
                result = rows[row].find_all("td", class_="right")

                if result[1].text == "":
                    matchdata.append(-1)
                    avg_scored += -1
                else:
                    matchdata.append(int(result[1].text))
                    avg_scored += int(result[1].text)
            avg_scored /= 5
            time.sleep(0.1)

            # getting the conceded goals for every match and average
            avg_conceded = 0
            for row in range(weekdate - 5, weekdate):
                result = rows[row].find_all("td", class_="right")

                if result[2].text == "":
                    matchdata.append(-1)
                    avg_conceded += -1
                else:
                    matchdata.append(int(result[2].text))
                    avg_conceded += int(result[2].text)
            avg_conceded /= 5
            time.sleep(0.1)

            # getting the venue for every match
            for row in range(weekdate - 5, weekdate):
                result = rows[row].find_all("td", class_="left")
                match result[2].text:
                    case "Home":
                        matchdata.append(1)
                    case "Away":
                        matchdata.append(-1)
            time.sleep(0.1)

            # adding the avg goal last 5
            matchdata.append(avg_scored)
            matchdata.append(avg_conceded)

        self.final_data.append(matchdata)

    def get_training_set(self):  # getting training data
        training_data = []
        for i in range(6, 22):
            for matchdata in self.get_data_set(i):
                training_data.append(matchdata)

        return training_data

    def get_targets(self, row):  # gets targets values for training data
        if row.find("td", class_="center").find("a") is not None:
            score = row.find("td", class_="center").find("a").text
            if int(score[0:1]) > int(score[2]):
                self.targets.append(1)
            elif int(score[0:1]) < int(score[2]):
                self.targets.append(-1)
            else:
                self.targets.append(0)
        else:
            self.targets.append(0)

    def save(self):  # saves all training data and target datas
        for i in range(0, len(self.final_data)):
            self._save_set(i)

        with open(f"database/training_set_targets.txt", "w") as file:
            for target in self.targets:
                file.write("%s\n" % target)

    def _save_set(self, index):  # helper method for saving
        with open(f"database/training_set{index}.txt", "w") as file:
            for data in self.final_data[index]:
                file.write("%s\n" % data)

    def read(self, choice):  # reads and returns targets or training datas by choice
        # choice is targets("t") or training values("d")
        big_set = []

        if choice == "d":
            for i in range(0, 150):
                big_set.append(self._read_set(i))

            return big_set

        elif choice == "t":
            with open(f"database/training_set_targets.txt", "r") as file:
                for line in file:
                    x = int(line[:-1])
                    big_set.append(x)

            return big_set

    def _read_set(self, index):  # helper method for read
        with open(f"database/training_set{index}.txt", "r") as file:
            x = []
            for line in file:
                value = float(line[:-1])
                x.append(value)

        return x
