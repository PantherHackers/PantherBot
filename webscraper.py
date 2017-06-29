from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

browser = webdriver.PhantomJS()
url = "http://www.nextbus.com/displays/lcd/georgia-state/"
browser.get(url)
delay = 3

try:
	myElem = WebDriverWait(browser,delay).until(EC.text_to_be_present_in_element((By.ID, "[data-r] > div > p", "Loading predictions ...")))
# thing = browser.find_elements_by_class_name("piedmont")
	print "ready"
except TimeoutException:
	print "Took a while"
thing = browser.find_elements_by_css_selector("[data-r] > div > p")

# thing = browser.find_elements_by_css_selector("[data-r]")

# for t in thing:
# 	p = t.find_elements_by_tag_name('p')
# 	for time in p:
# 		print time.text
# # print thing.text
# browser.quit()