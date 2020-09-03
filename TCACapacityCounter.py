from selenium import webdriver
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from datetime import date
import pytz
import time
import gspread


#Scraping setup
url = "https://www.theclimbingacademy.com/tca-life/capacity-tracker/?fbclid=IwAR1Oq7ur4Y3bwSV062221D-3UuP29QmQCgG8l7nDpkjY3_amGvbF1L9nfnE"
driver = webdriver.Chrome()

#Get date and time
date = str(date.today().strftime("%d/%m/%Y"))
tz = pytz.timezone('Europe/London')
curr_time = str(datetime.now(tz))[11:16]

#Get current capacity
driver.get(url)
time.sleep(5)
driver.switch_to.frame(driver.find_element_by_id("occupancyCounter"))
driver.find_element_by_xpath('//*[@id="gym-switcher"]/option[4]').click()
time.sleep(5)
curr_capacity = driver.find_element_by_xpath('//*[@id="count"]').text

#Output to Google Sheet
scope = ['http://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('TCACounter-cbf97f52177e.json')
client = gspread.authorize(creds)
sheet = client.open('TCA Newsroom Capacity').sheet1
sheet.append_rows([[date, curr_time, str(curr_capacity)]])
print("Done")
