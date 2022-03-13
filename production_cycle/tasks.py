from ast import operator
import time
from celery.schedules import crontab
import openpyxl
import os
from celery import shared_task
from FutureFarm.celery import app
from django_celery_beat.models import CrontabSchedule, PeriodicTask
import pytz
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from glob import glob
from .models import MinRolPrices


@app.task(name='get_ministerial_price')
def get_ministerial_price():
    print('cena minrol')

    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : os.path.abspath('files')}
    options.add_experimental_option('prefs', prefs)
    operator.add_argument("--headless")
    operator.add_argument("--no-sandbox")
    operator.add_argument("--disable-dev-sh-usage")
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
    
    driver.get('https://www.gov.pl/web/rolnictwo/rynek-drobiu')
    yearElement = driver.find_element_by_xpath('//*[@id="body"]/main/div[2]/article/div/ul/li[1]/a')
    yearLink = yearElement.get_attribute('href')    
    
    driver.get(yearLink)
    weekElement = driver.find_element_by_xpath('//*[@id="body"]/main/div[2]/article/div/ul/li[1]/a')
    weekLink = weekElement.get_attribute('href')
    
    driver.get(weekLink)
    driver.execute_script("window.scrollTo(0, 400)") 
    file = driver.find_element_by_xpath('//*[@id="main-content"]/a')
    file.click()
    print('Downloading file')

    time.sleep(10)
    driver.close()

    filePath = glob('/Users/FilipGluszcz/Desktop/Django/Projects/static/drob*.xlsx')
    path = filePath[0]

    book = openpyxl.load_workbook(path)
    sheet = book['ceny skupu']
    price = sheet['B6'].value

    minRolPrice = MinRolPrices(price=price)
    minRolPrice.save()

    os.remove(path)

app.conf.beat_schedule = {
    'get_ministerial_price': {
        'task': 'get_ministerial_price',
        'schedule': crontab(hour=18, minute=56),
    },
}


# crontab(hour=20, minute=56, day_of_week=4),


#  celery -A FutureFarm worker --loglevel=info

#  celery -A FutureFarm beat --loglevel=info


#  day_of_week=5