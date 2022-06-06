from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import time

PATH = '/home/jotaalvim/Documents/projetos/chromedriver/chromedriver102.0.5005.61'

#option = webdriver.ChromeOptions()
#option.add_argument('headless')
#driver = webdriver.Chrome( PATH ,options = option)
driver = webdriver.Chrome( PATH )

driver.get('https://elearning.uminho.pt/')


search = driver.find_element_by_name('user_id')
search.send_keys('a95191')

search = driver.find_element_by_name('password')
search.send_keys('113eurosali')
search.send_keys(Keys.RETURN)
#login feito

#encontrar cadeiras
time.sleep(0.5)
sourceCode = str(driver.page_source)
print(sourceCode)

search3 = re.findall(r'\<li\>(\w+)\<\/li\>',sourceCode)
print(search3)
