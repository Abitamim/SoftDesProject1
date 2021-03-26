from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from os import stat
from bs4 import BeautifulSoup
import re
import threading

def get_vote_counts(page_html:str) -> str:
    '''
    docstring here

    Args: 
    Returns: 
    '''

    soup = BeautifulSoup(page_html)
    tables = soup.find_all('table')
    rows = tables[-2].find_all('tr')[13:]

    candidates_and_votes = [r.text.split('\n')[1][2:] for r in rows]
    separate_candidate_votes_regex = re.compile("([^0-9]+)([0-9]+)")
    candidates_and_votes = [separate_candidate_votes_regex.match(cav).groups() for cav in candidates_and_votes]

    location = tables[1].find_all('tr')[0].find('td').text.split(' > ')
    region_oblast = ",".join([location[1], location[2][:-2]])

    oblast_csv = '\n'.join([','.join([cav[0],cav[1],region_oblast]) for cav in candidates_and_votes])+'\n'

    return oblast_csv


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
        file.write('candidate, votes, region, oblast\n')
    file.write(votes_data)
    file.close()

def get_data(driver, url, k):
    oblast_data = ""
    driver.get(url)
    time.sleep(30)

    table_format = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Результаты выборов'))
    )
    table_format.click()

    dropdown_regions = driver.find_element_by_name('gs')
    election_regions = dropdown_regions.find_elements_by_tag_name('option')
    # navigate to the page with data for the region
    election_regions[k].click()
    select_button = driver.find_element_by_name('go')
    select_button.click()

    dropdown_oblast = driver.find_element_by_name('gs')
    election_oblast = dropdown_oblast.find_elements_by_tag_name('option')

    for i in range(1,len(election_oblast)):
            dropdown_oblast = driver.find_element_by_name('gs')
            election_oblast = dropdown_oblast.find_elements_by_tag_name('option')
            # navigate to the page for an oblast in that city
            election_oblast[i].click()
            select_button = driver.find_element_by_name('go')
            select_button.click()
            time.sleep(.5)
            oblast_data += get_vote_counts(driver.page_source)
            driver.back()
    driver.close()
    return oblast_data


def get_election_data():
    '''
    doctring here
    '''

    url = 'http://www.vybory.izbirkom.ru/region/izbirkom?action=show&root_a=null&vrn=100100084849062&region=0&global=true&type=0&prver=0&pronetvd=null'

    # Using Chrome version 89 and chromedriver version 89 (important that they match)
    driver = webdriver.Chrome()

    driver.get(url)
    # 20 seconds to manually enter code to proceed
    time.sleep(10)

    # wait until page loads, then select the page with the table of data
    # only need to do this once as the configurations save
    table_format = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Результаты выборов'))
    )

    table_format.click()

    drivers = []
    data = ""
    dropdown_regions = driver.find_element_by_name('gs')
    election_regions = dropdown_regions.find_elements_by_tag_name('option')
    for k in range(1,len(election_regions)):
        drivers.append(webdriver.Chrome())
        data_thread = threading.Thread(get_data(drivers[k],driver[k].current_url, k))
        data_thread.start()
    
    save_csv(oblast_data, 'data/2018-Russia-election-data.txt')
    driver.quit()


if __name__ == '__main__':
    get_election_data()
