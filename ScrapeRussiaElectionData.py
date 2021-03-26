from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from os import stat
from bs4 import BeautifulSoup


def get_vote_counts(driver, page_html):
    '''
    docstring here

    Args: 
    Returns: 
    '''
    
    pass

def save_csv(votes_data, path): 
    '''
    Adds a string of data to the end of a csv file.

    Args: 
        votes_data: a string representing the votes data collected in the format
        'candidate, votes, city, oblast'.
        path: a string representing the name of the path to the file to store
        the data
    '''
    file = open(path, 'a')
    if stat(path).st_size == 0: 
        file.write('candidate, votes, city, oblast\n')
    file.write(votes_data)
    file.close()

def get_election_data():
    '''
    doctring here
    '''

    url = 'http://www.vybory.izbirkom.ru/region/izbirkom?action=show&root_a=null&vrn=100100084849062&region=0&global=true&type=0&prver=0&pronetvd=null'

    #Using Chrome version 89 and chromedriver version 89 (important that they match)
    driver = webdriver.Chrome('/home/softdes/Downloads/chromedriver')

    driver.get(url)
    #20 seconds to manually enter code to proceed
    time.sleep(20)

    #wait until page loads, then select the page with the table of data
    #only need to do this once as the configurations save
    table_format = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.LINK_TEXT,'Результаты выборов'))
    )

    table_format.click()

    dropdown_cities = driver.find_element_by_name('gs')
    election_cities = dropdown_cities.find_elements_by_tag_name('options')
    for cities in election_cities:
        #navigate to the page with data for the city
        driver.find_element_by_link_text(f'{cities}').click()
        select_button = driver.find_elements_by_name('go')
        select_button.click()
        
        dropdown_oblast = driver.find_element_by_name('gs')
        election_oblast = dropdown_oblast.find_element_by_tag_name('options')
        
        for oblast in election_oblast:
            #navigate to the page for an oblast in that city
            driver.find_element_by_link_text(f'{oblast}').click()
            select_button.click()
            #oblast_data = get_vote_counts(driver, driver.page_source)
            oblast_data =''
            save_csv(oblast_data, 'data/2018-Russia-election-data.txt')
            driver.back()

    driver.quit()

if __name__ == '__main__':
    get_election_data()