from selenium import webdriver
from os import stat


def get_vote_counts(driver, html: str) -> str:
    """
    Turns a page of with the vote counts from a county election into a csv.

    Args:
        html (str): Page with vote counts

    Returns:
        str: csv formatted in this format: candidate, votes, "county, state" 
    """
    candidates = [x.text for x in driver.find_elements_by_class_name("name")[
        ::3]]
    votes = [int(x.text.replace(',', ''))
             for x in driver.find_elements_by_class_name("num")[::2]]
    location = ",".join(driver.find_element_by_class_name(
        "header").text.split(" - ")[-1].split(", "))
    return "\n".join([f"{candidate},{vote_count},{location}" for candidate, vote_count in zip(candidates, votes)]) + "\n"


def save_csv(vote_data: str, file_path: str):
    """
    Adds csv data at end of provided file.

    Args:
        vote_data (str): formatted csv data to save
        file (str): file to store data in
    """
    f = open(file_path, 'a')
    if stat(file_path).st_size == 0:
        f.write("candidate,votes,county,state\n")
    f.write(vote_data)
    f.close()


def get_data_for_states():
    """
    Currently, it goes to Alabama, finds the 2020 election data for each
    candidate for each county, and stores it in data/2020-elections-data.txt.
    """
    #Next two lines are optional, along with the options argument to
    #webdriver.Chrome, in order to eliminate irrelevant logging information.
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    with webdriver.Chrome(options=options) as driver:
        for fip_number in [x for x in range(1, 57) if x not in (3, 7, 11, 14, 43, 52)]:
            driver.get(
                f"https://uselectionatlas.org/RESULTS/state.php?year=2020&off=0&elect=0&fips={fip_number}&f=0")
            drop_down = driver.find_element_by_name("fips")
            counties = drop_down.find_elements_by_tag_name("option")
            for i in range(len(counties)):
                drop_down = driver.find_element_by_name("fips")
                counties = drop_down.find_elements_by_tag_name("option")
                county = counties[i]
                county.click()
                input = driver.find_element_by_name("submit")
                input.click()
                county_data = get_vote_counts(driver, driver.page_source)
                save_csv(county_data, "data/2020-elections-data.txt")
                driver.back()

if __name__ == "__main__":
    get_data_for_states()