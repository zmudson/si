from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time


PATH = "C:\\Drive\\chromeDriver\\chromedriver.exe"
driver = webdriver.Chrome(PATH)

#2020-21
ODDSPATH = "https://www.oddsportal.com/basketball/usa/nba-2020-2021/results/#/page/"

with open('test.csv', 'w', newline='') as csvfile:
    wr = csv.writer(csvfile)
    wr.writerow(['Date', 'Home Team', 'Away Team', 'Home Score', 'Away Score', 'Home Odds', 'Away Odds', 'Who Won', 'Playoffs'])
    for i in range(1, 26):
        print(i)
        tempPath = ODDSPATH + str(i) + "/"
        driver.get(tempPath)
        time.sleep(2.5)
        table = driver.find_element(by=By.CLASS_NAME, value="table-main")
        date = ''
        for row in table.find_elements(by=By.CSS_SELECTOR, value='tr'):
            header = [d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='th')]
            info = [d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='td')]
            #print([d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='th')])
            if header != []:
                #print(header[0])
                date = header[0].split('-')
            if info != [] and info[0] != '':
                output = list()
                playoffs = 0
                if len(date) > 1:
                    playoffs = 1
                output.append(date[0].strip())
                teams = info[1].strip().replace('\n', '')
                output.append(teams.split('-')[0])
                output.append(teams.split('-')[1])
                score = info[2].replace(' OT', '').strip()
                output.append(score.split(':')[0])
                output.append(score.split(':')[1])
                output.append(info[3])
                output.append(info[4])
                output.append(int(score.split(':')[0])//int(score.split(':')[1]))
                output.append(playoffs)
                wr.writerow(output)
            #wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])

# #2019-20
# ODDSPATH = "https://www.oddsportal.com/basketball/usa/nba-2019-2020/results/#/page/"
#
# with open('2019-20.csv', 'w', newline='') as csvfile:
#     wr = csv.writer(csvfile)
#     for i in range(1, 26):
#         print(i)
#         tempPath = ODDSPATH + str(i) + "/"
#         driver.get(tempPath)
#         time.sleep(2.5)
#         table = driver.find_element(by=By.CLASS_NAME, value="table-main")
#         for row in table.find_elements(by=By.CSS_SELECTOR, value='tr'):
#             print([d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='td')])
#             wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
#
# #2018-19
# ODDSPATH = "https://www.oddsportal.com/basketball/usa/nba-2018-2019/results/#/page/"
#
# with open('2018-19.csv', 'w', newline='') as csvfile:
#     wr = csv.writer(csvfile)
#     for i in range(1, 29):
#         print(i)
#         tempPath = ODDSPATH + str(i) + "/"
#         driver.get(tempPath)
#         time.sleep(2.5)
#         table = driver.find_element(by=By.CLASS_NAME, value="table-main")
#         for row in table.find_elements(by=By.CSS_SELECTOR, value='tr'):
#             print([d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='td')])
#             wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
#
# #2017-18
# ODDSPATH = "https://www.oddsportal.com/basketball/usa/nba-2017-2018/results/#/page/"
#
# with open('2017-18.csv', 'w', newline='') as csvfile:
#     wr = csv.writer(csvfile)
#     for i in range(1, 29):
#         print(i)
#         tempPath = ODDSPATH + str(i) + "/"
#         driver.get(tempPath)
#         time.sleep(2.5)
#         table = driver.find_element(by=By.CLASS_NAME, value="table-main")
#         for row in table.find_elements(by=By.CSS_SELECTOR, value='tr'):
#             print([d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='td')])
#             wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
#
# #2016-17
# ODDSPATH = "https://www.oddsportal.com/basketball/usa/nba-2016-2017/results/#/page/"
#
# with open('2016-17.csv', 'w', newline='') as csvfile:
#     wr = csv.writer(csvfile)
#     for i in range(1, 30):
#         print(i)
#         tempPath = ODDSPATH + str(i) + "/"
#         driver.get(tempPath)
#         time.sleep(2.5)
#         table = driver.find_element(by=By.CLASS_NAME, value="table-main")
#         for row in table.find_elements(by=By.CSS_SELECTOR, value='tr'):
#             print([d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='td')])
#             wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
#
# #2015-16
# ODDSPATH = "https://www.oddsportal.com/basketball/usa/nba-2015-2016/results/#/page/"
#
# with open('2015-16.csv', 'w', newline='') as csvfile:
#     wr = csv.writer(csvfile)
#     for i in range(1, 30):
#         print(i)
#         tempPath = ODDSPATH + str(i) + "/"
#         driver.get(tempPath)
#         time.sleep(2.5)
#         table = driver.find_element(by=By.CLASS_NAME, value="table-main")
#         for row in table.find_elements(by=By.CSS_SELECTOR, value='tr'):
#             print([d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='td')])
#             wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
#
# #2014-15
# ODDSPATH = "https://www.oddsportal.com/basketball/usa/nba-2014-2015/results/#/page/"
#
# with open('2014-15.csv', 'w', newline='') as csvfile:
#     wr = csv.writer(csvfile)
#     for i in range(1, 30):
#         print(i)
#         tempPath = ODDSPATH + str(i) + "/"
#         driver.get(tempPath)
#         time.sleep(2.5)
#         table = driver.find_element(by=By.CLASS_NAME, value="table-main")
#         for row in table.find_elements(by=By.CSS_SELECTOR, value='tr'):
#             print([d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='td')])
#             wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
#
# #2013-14
# ODDSPATH = "https://www.oddsportal.com/basketball/usa/nba-2016-2017/results/#/page/"
#
# with open('2013-14.csv', 'w', newline='') as csvfile:
#     wr = csv.writer(csvfile)
#     for i in range(1, 30):
#         print(i)
#         tempPath = ODDSPATH + str(i) + "/"
#         driver.get(tempPath)
#         time.sleep(2.5)
#         table = driver.find_element(by=By.CLASS_NAME, value="table-main")
#         for row in table.find_elements(by=By.CSS_SELECTOR, value='tr'):
#             print([d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='td')])
#             wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
#
# #2012-13
# ODDSPATH = "https://www.oddsportal.com/basketball/usa/nba-2012-2013/results/#/page/"
#
# with open('2012-13.csv', 'w', newline='') as csvfile:
#     wr = csv.writer(csvfile)
#     for i in range(1, 30):
#         print(i)
#         tempPath = ODDSPATH + str(i) + "/"
#         driver.get(tempPath)
#         time.sleep(2.5)
#         table = driver.find_element(by=By.CLASS_NAME, value="table-main")
#         for row in table.find_elements(by=By.CSS_SELECTOR, value='tr'):
#             print([d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='td')])
#             wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
#
# #2011-12
# ODDSPATH = "https://www.oddsportal.com/basketball/usa/nba-2011-2012/results/#/page/"
#
# with open('2011-12.csv', 'w', newline='') as csvfile:
#     wr = csv.writer(csvfile)
#     for i in range(1, 24):
#         print(i)
#         tempPath = ODDSPATH + str(i) + "/"
#         driver.get(tempPath)
#         time.sleep(2.5)
#         table = driver.find_element(by=By.CLASS_NAME, value="table-main")
#         for row in table.find_elements(by=By.CSS_SELECTOR, value='tr'):
#             print([d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='td')])
#             wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
#
# #2010-11
# ODDSPATH = "https://www.oddsportal.com/basketball/usa/nba-2010-2011/results/#/page/"
#
# with open('2010-11.csv', 'w', newline='') as csvfile:
#     wr = csv.writer(csvfile)
#     for i in range(1, 30):
#         print(i)
#         tempPath = ODDSPATH + str(i) + "/"
#         driver.get(tempPath)
#         time.sleep(2.5)
#         table = driver.find_element(by=By.CLASS_NAME, value="table-main")
#         for row in table.find_elements(by=By.CSS_SELECTOR, value='tr'):
#             print([d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='td')])
#             wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
#
# #2009-10
# ODDSPATH = "https://www.oddsportal.com/basketball/usa/nba-2009-2010/results/#/page/"
#
# with open('2009-10.csv', 'w', newline='') as csvfile:
#     wr = csv.writer(csvfile)
#     for i in range(1, 30):
#         print(i)
#         tempPath = ODDSPATH + str(i) + "/"
#         driver.get(tempPath)
#         time.sleep(2.5)
#         table = driver.find_element(by=By.CLASS_NAME, value="table-main")
#         for row in table.find_elements(by=By.CSS_SELECTOR, value='tr'):
#             print([d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='td')])
#             wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
#
# #2008-09
# ODDSPATH = "https://www.oddsportal.com/basketball/usa/nba-2008-2009/results/#/page/"
#
# with open('2008-09.csv', 'w', newline='') as csvfile:
#     wr = csv.writer(csvfile)
#     for i in range(1, 29):
#         print(i)
#         tempPath = ODDSPATH + str(i) + "/"
#         driver.get(tempPath)
#         time.sleep(2.5)
#         table = driver.find_element(by=By.CLASS_NAME, value="table-main")
#         for row in table.find_elements(by=By.CSS_SELECTOR, value='tr'):
#             print([d.text for d in row.find_elements(by=By.CSS_SELECTOR, value='td')])
#             wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])
