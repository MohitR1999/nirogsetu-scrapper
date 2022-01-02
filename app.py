from flask import Flask
from bs4 import BeautifulSoup
from flask.json import jsonify
from selenium import webdriver
from selenium.webdriver.firefox import service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager import driver
from webdriver_manager.firefox import GeckoDriverManager

URL = 'https://www.mohfw.gov.in/index.html'
service = Service(executable_path=GeckoDriverManager().install())
firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(service=service, options=firefox_options)

app = Flask(__name__)

@app.route('/')
def getScrapedData():
    driver.get(URL)
    button = driver.find_element(By.CLASS_NAME, "open-table")
    button.click()
    table = driver.find_element(By.CSS_SELECTOR, ".statetable")
    tableMarkup = table.get_attribute("outerHTML")
    soup = BeautifulSoup(tableMarkup, 'html5lib')
    statesData = []
    rows = soup.find_all('tr')
    for i in range(3, 39):
        cells = rows[i].find_all('td')
        if (len(cells) > 1):
            data = {}
            data['id'] = cells[0].text
            data['name'] = cells[1].text
            data['total_active'] = cells[2].text
            data['total_cured'] = cells[4].text
            data['total_deaths'] = cells[6].text
            statesData.append(data)
    return jsonify(statesData)

@app.route('/vaccinated')
def getVaccinatedData():
    driver.get(URL)
    totalVaccinated = driver.find_element(By.CSS_SELECTOR, "span.coviddata")
    vaccinated = {}
    vaccinated['totalVaccinated'] = totalVaccinated.text
    return jsonify(vaccinated)

if __name__ == '__main__':
    app.run(debug= False)