from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time


PATH = "C:\\Drive\\chromeDriver\\chromedriver.exe"
driver = webdriver.Chrome(PATH)

ODDSPATH = "https://www.oddsportal.com/basketball/usa/nba-2020-2021/results/#/page/"

pages = [29, 30, 30, 24, 30, 30, 30, 30, 30, 29, 29, 26, 26]

for _ in range(8, 21):
    ODDSPATH = "https://www.oddsportal.com/basketball/usa/nba-" + str(2000 + _) + "-" + str(2000+_+1) + "/results/#/page/"

    with open(str(2000 + _) + "-" + str(2000+_+1) + '.csv', 'w', newline='') as csvfile:
        wr = csv.writer(csvfile)
        wr.writerow(['Date', 'Home Team', 'Away Team', 'Home Score', 'Away Score', 'Home Odds', 'Away Odds', 'Who Won', 'Playoffs', 'Preseason'])
        for i in range(1, pages[_-8]):
            print(i)
            tempPath = ODDSPATH + str(i) + "/"
            driver.get(tempPath)
            time.sleep(2.5)
            table = driver.find_element(by=By.CLASS_NAME, value="table-main")
            date = ''
            for row in table.find_elements(by=By.CSS_SELECTOR, value='tr'):
                header = [d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='th')]
                info = [d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='td')]
                if header != []:
                    date = header[0].split('-')
                if info != [] and info[0] != '':
                    output = list()
                    playoffs = 0
                    preseason = 0
                    if len(date) > 1:
                        if len(date) > 2:
                            preseason = 1
                        else:
                            playoffs = 1
                    output.append(date[0].strip())
                    teams = info[1].strip().replace('\n', '')
                    output.append(teams.split('-')[0].strip())
                    output.append(teams.split('-')[1].strip())
                    score = info[2].replace(' OT', '').strip()
                    if score == 'canc.':
                        continue
                    output.append(score.split(':')[0])
                    output.append(score.split(':')[1])
                    output.append(info[3])
                    output.append(info[4])
                    output.append(int(score.split(':')[0])//int(score.split(':')[1]))
                    output.append(playoffs)
                    output.append(preseason)
                    wr.writerow(output)
