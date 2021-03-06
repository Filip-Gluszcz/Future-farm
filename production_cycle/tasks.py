import time
from celery.schedules import crontab
import openpyxl
import os
from FutureFarm.celery import app
from selenium import webdriver
from glob import glob
from .models import MinRolPrices


@app.task(name='get_ministerial_price')
def get_ministerial_price():
    print('cena minrol')

    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    prefs = {'download.default_directory' : os.path.abspath('files')}
    options.add_experimental_option('prefs', prefs)
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-sh-usage")
    driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=options)
    
    driver.get('https://www.gov.pl/web/rolnictwo/rynek-drobiu')
    yearElement = driver.find_element_by_xpath('//*[@id="body"]/main/div[2]/article/div/ul/li[1]/a')
    yearLink = yearElement.get_attribute('href')    
    
    driver.get(yearLink)
    weekElement = driver.find_element_by_xpath('//*[@id="body"]/main/div[2]/article/div/ul/li[1]/a')
    weekLink = weekElement.get_attribute('href')
    
    driver.get(weekLink)
    file =  driver.find_element_by_css_selector('.file-download')
    location = file.location["y"] - 100
    driver.execute_script("window.scrollTo(0, %d);" %location)
    file.click()
    print('Downloading file')

    time.sleep(10)
    driver.close()

    filePath = glob(os.path.abspath('files/drob*.xlsx'))
    path = filePath[0]

    book = openpyxl.load_workbook(path)
    sheet = book['ceny skupu']
    price = sheet['B5'].value

    minRolPrice = MinRolPrices(price=price)
    minRolPrice.save()

    os.remove(path)

app.conf.beat_schedule = {
    'get_ministerial_price': {
        'task': 'get_ministerial_price',
        'schedule': crontab(hour=11, minute=55, day_of_week=4),
    },
}

#  celery -A FutureFarm worker --loglevel=info

#  celery -A FutureFarm beat --loglevel=info
