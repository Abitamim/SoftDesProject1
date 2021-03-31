"""
Finds and stores the voting data for each candidate in every district
in the Russia 2018 Presidential election.
"""

import re
from os import stat
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_vote_counts(page_html: str) -> str:
    """
    Takes the html source of the page with vote counts and collects all of the
    votes for each candidate from that page into a string to be put into a csv
    file.

    Args:
        page_html: a string representing the html page source containing the
        vote counts.
    Returns:
        A string of data representing the vote counts for each candidate in each
        region and district to be put into a csv file. The data is formatted as
        follows: candidate, votes, region, oblast
    """

    soup = BeautifulSoup(page_html)
    tables = soup.find_all("table")
    rows = tables[-2].find_all("tr")[13:]

    candidates_and_votes = [r.text.split("\n")[1][2:] for r in rows]
    separate_candidate_votes_regex = re.compile("([^0-9]+)([0-9]+)")
    candidates_and_votes = [
        separate_candidate_votes_regex.match(cav).groups()
        for cav in candidates_and_votes
    ]

    location = tables[1].find_all("tr")[0].find("td").text.split(" > ")
    print(f"location: {location}")
    if len(location) > 2:
        region_oblast = ",".join([location[1], location[2][:-1]])
    elif len(location) > 1:
        region_oblast = ",".join([location[1][:-1], location[1][:-1]])
    else:
        region_oblast = "N/A"
    oblast_csv = (
        "\n".join(
            [re.sub('(,[^,]*),', r'\1 ', ",".join([cav[0], cav[1], region_oblast])) for cav in candidates_and_votes]
        )
        + "\n"
    )

    return oblast_csv


def save_csv(votes_data:str, path:str):
    """
    Adds a string of data to the end of a csv file.

    Args:
        votes_data: a string representing the votes data collected in the format
        'candidate, votes, city, oblast'.
        path: a string representing the name of the path to the file to store
        the data
    """
    file = open(path, "a", encoding="utf-8")
    if stat(path).st_size == 0:
        file.write("candidate,votes,region,oblast\n")
    file.write(votes_data)
    file.close()


def get_election_data():
    """
    Iterates through a website containing the election data for the Russia 2018
    Presidential Election, grabs the votes for each candidate in each region,
    and stored that data in a csv file.
    """

    url = "http://www.vybory.izbirkom.ru/region/izbirkom?action=show& \
            root_a=null&vrn=100100084849062&region=0&global=true& \
            type=0&prver=0&pronetvd=null"

    # Using Chrome version 89 and chromedriver version 89 (important that they match)
    driver = webdriver.Chrome()

    driver.get(url)
    # 20 seconds to manually enter code to proceed
    time.sleep(10)

    # wait until page loads, then select the page with the table of data
    # only need to do this once as the configurations save
    table_format = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Результаты выборов"))
    )

    table_format.click()

    dropdown_regions = driver.find_element_by_name("gs")
    election_regions = dropdown_regions.find_elements_by_tag_name("option")

    for k in range(1, len(election_regions)):
        dropdown_regions = driver.find_element_by_name("gs")
        election_regions = dropdown_regions.find_elements_by_tag_name("option")
        # navigate to the page with data for the region
        election_regions[k].click()
        select_button = driver.find_element_by_name("go")
        select_button.click()

        try:
            dropdown_oblast = driver.find_element_by_name("gs")
            election_oblast = dropdown_oblast.find_elements_by_tag_name("option")

            for i in range(1, len(election_oblast)):
                dropdown_oblast = driver.find_element_by_name("gs")
                election_oblast = dropdown_oblast.find_elements_by_tag_name("option")
                # navigate to the page for an oblast in that city
                election_oblast[i].click()
                select_button = driver.find_element_by_name("go")
                select_button.click()
                oblast_data = get_vote_counts(driver.page_source)
                save_csv(oblast_data, "data/2018-Russia-election-data.csv")
                driver.back()
        except NoSuchElementException:
            oblast_data = get_vote_counts(driver.page_source)
            save_csv(oblast_data, "data/2018-Russia-election-data.csv")
        driver.back()

    driver.quit()


if __name__ == "__main__":
    get_election_data()
