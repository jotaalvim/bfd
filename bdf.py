from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

PATH = '/home/jotaalvim/Documents/projetos/chromedriver/chromedriver102.0.5005.61'

driver = webdriver.Chrome(PATH)

driver.get('https://elearning.uminho.pt/')


search = driver.find_element_by_name('user_id')
search.send_keys('a95191')

search = driver.find_element_by_name('password')
search.send_keys('garconefeio')
search.send_keys(Keys.RETURN)
#login feito

#não funciona tou so a experimentar
cadeiras = driver.find_element_by_id('div1_1')
cadeiras2 = driver.findElement(By.xpath("//div[@class='div1_1']/div[@class='div1_1']")).getText();

print(cadeiras.text)
print(cadeiras2)


