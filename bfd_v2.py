import string

import requests
from bs4 import BeautifulSoup
import time
import os
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def removeDisallowedFilenameChars(filename=None):
    validFileChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ()-/_ .,0123456789"
    filename = "".join(x for x in filename if x in validFileChars)
    return filename


directory_count = 0


def increment_directory_count():
    global directory_count
    directory_count += 1


"""
Esta funcao recebe o path para a diretoria onde vao ser descarregados os ficheiros e criadas
as novas pastas.
Tambem recebe um objeto Tag com o html necessario contido
"""


def file_parser(path, html=None, session=None, driver=None):
    diretoria_prefix = "/webapps/"
    ficheiro_prefix = "/bbcswebdav"
    dominio = "https://elearning.uminho.pt"
    validpath = removeDisallowedFilenameChars(path)
    if validpath[-1] != "/":
        validpath = validpath + "/"
    print(validpath)
    try:
        os.mkdir(validpath)
    except FileExistsError:
        print(str(validpath) + " ja foi criado")
    if html == None:
        return;
    for link in html.find_all("a"):
        if diretoria_prefix in link.get('href'):
            # este elemento ser diretoria
            # print(link.string)
            # diretorias_url_links.append(link['href'])
            increment_directory_count()
            if directory_count < 10:
                url = dominio + link.get('href')
                divisao_html = get_conteudo_html(driver, url)
                file_parser(os.path.join(validpath, link.string),divisao_html,session, driver)
        elif ficheiro_prefix in link.get('href'):
            # este elemento ser ficheiro para dar download
            # print(list(link.stripped_strings)[0])
            # ficheiros_url_links.append(link['href'])
            print(dominio + link.get('href'))
            ficheiro = session.get(dominio + link.get('href'))
            print("status code - " + str(ficheiro.status_code))
            nome = list(link.stripped_strings)[0]
            file_path = validpath + removeDisallowedFilenameChars(nome)
            print(file_path)
            file = open(file_path, "wb");
            file.write(ficheiro.content);
            file.close();
            print("e ficheiro")


def get_conteudo_html(driver=None, url=None):
    driver.get(url)
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    divisao = soup.find(id="containerdiv")
    return divisao


s = requests.Session()

url = "https://elearning.uminho.pt/webapps/blackboard/content/listContent.jsp?course_id=_51246_1&content_id=_1193419_1&mode=reset"
# user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0"
pasta = "ficheiros/"

diretoria_prefix = "/webapps/blackboard"
ficheiro_prefix = "/bbcswebdav"

user = input("Introduz o nome de utilizador: ")
password = input("Introduz a password: ")

driver = webdriver.Firefox()
driver.get(url)
driver.find_element(By.ID, 'user_id').send_keys(user);

search = driver.find_element(By.ID, 'password')
search.send_keys(password)
search.send_keys(Keys.RETURN)

# login feito

timeout = 5

time.sleep(5);
# try:
#    os.mkdir(pasta);
# except FileExistsError:
#    print("ja existe ficheiro")

# try:
#    os.mkdir(os.path.join(pasta, "teste3"));
# except FileExistsError:
#    print("ja existe ficheiro")

blackboard = s.get("https://elearning.uminho.pt/")
print(blackboard.content)
content = BeautifulSoup(blackboard.content, "html.parser")
token = content.find("input", {"name": "blackboard.platform.security.NonceUtil.nonce.ajax"})["value"]
login_data = {
    "user_id": "A95826",
    "password": "paumaximo123",
    "login": "Iniciar+sess�o",
    "action": "login",
    "new_loc": "",
    "blackboard.platform.security.NonceUtil.nonce.ajax": token
}
s.post("https://elearning.uminho.pt/", login_data)
# teste = s.get("https://elearning.uminho.pt/bbcswebdav/pid-1210373-dt-content-rid-5829951_1/xid-5829951_1")
# print("status code1 - " + str(teste.status_code))
# file1 = open("teste1", "wb");
# file1.write(teste.content);
# file1.close();

print("ja deu s.post")

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

divisao = soup.find(id="containerdiv")
file_parser(pasta, divisao, s, driver)

# for link in divisao.find_all("a"):
#    if diretoria_prefix in link.get('href'):
#        print(link.string)
#        diretorias_url_links.append(link['href'])
#    elif ficheiro_prefix in link.get('href'):
#        print(list(link.stripped_strings)[0])
#        ficheiros_url_links.append(link['href'])

# try:
#    element_present = EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, cadeira_nome))
#    WebDriverWait(driver, timeout).until(element_present)
#    driver.find_element(By.PARTIAL_LINK_TEXT, cadeira_nome).click();
# except TimeoutException:
#    print("Timed out waiting for page to load " + cadeira_nome)

# try:
#    element_present = EC.presence_of_element_located((By.ID, "courseMenuPalette_contents"))
#    WebDriverWait(driver, timeout).until(element_present)
#    driver.find_element(By.ID, "courseMenuPalette_contents").find_element(By.PARTIAL_LINK_TEXT, "Cont")\
#        .click();
# except TimeoutException:
#    print("Timed out waiting for page to load2")

# soup = BeautifulSoup(html, "html.parser")
# for link in soup.find_all('a', href=True):
#    print(link['href'])

"""
blackboard = s.get(url)
print(blackboard.content)
content = BeautifulSoup(blackboard.content, "html.parser")
token = content.find("input", {"name":"blackboard.platform.security.NonceUtil.nonce.ajax"})["value"]
login_data = {
    "user_id": "A95826",
    "password": "paumaximo123",
    "login": "Iniciar+sess�o",
    "action": "login",
    "new_loc": "",
    "blackboard.platform.security.NonceUtil.nonce.ajax": token
}
s.post("https://elearning.uminho.pt/", login_data)
home_page = s.get("https://elearning.uminho.pt/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_2_1")
# print(home_page.content)
time.sleep(2)
home_page_content = BeautifulSoup(home_page.content, "html.parser")

for link in home_page_content.find_all('a', href=True):
    print(link['href'])

"""
