# Using Benford's Law on Election Data
Authors: Dasha Chadiuk and Abitamim Bharmal

## Project Summary:
This project aims to answer the following question: Using Benford’s Law to analyze election data, can we identify possible fraud in the 2018 Russian and 2020 United States elections?
In this project, we gather vote data from the 2020 US and 2018 Russia elections and compare the distribution of first leading digits to the predicted Benford's Law Distribution. Doing so allows us to find inconsistencies that might point to fraudulent data. We cannot use this method to prove there was any fraud in either election, but instead be pointed in the right direction for futher analysis.

## Installation: 
To run the web-scraping scripts, you would need to install the Selenium and Beautiful Soup python libraries. 
To install Selenium and Beautiful Soup, run the following commands in your terminal: 

```
pip install Selenium
pip install beautifulsoup4
```

Note that you will have to have pip installed to run the two commands.
If you are having trouble with the installation process, please go to the [Selenium documentation page](https://selenium-python.readthedocs.io/installation.html) or the [Beautiful Soup documentation page](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup) for further instructions or troubleshooting. 

## Running the Web-Scraping Scripts: 
The code used to obtain the data is specific to the election data websites we used (for more information, see the computational essay). If you wish to use this script on other sources, you would have to modify the script to fit the architecture of the website you are using. However, in most cases our code might only be useful as a guideline rather than a template. 
### Russia: 
This program is located in the file scrape_russia_election_data.py. To run the web-scraping script for Russia, simply hit run or control enter to run the program. Note that you will have to wait for the browser to open and manually input the numerical code shown on the screen. The program will give you 10 seconds to manually input the code before it tries to proceed with the rest of the code. If you feel that 10 seconds is not enough time to input the code, you can change this value on line 96. 
### United States: 
To run the US web-scraping script, simply navigate to scrape_us_election_data.py and run the whole script. No user input is required to run this script. 

## Generating the Figures: 

We have included several functions in the data_analysis.py file that are used to process the data. In this file you will find a function that creates the confidence interval plot for all nine digits (for more information, please see the computational essay). To generate all of the figures we show in the computational essay, we use the matplotlib python library. If you wish to learn more about the types of plots you could create with this library, please visit the [matplotlib documentation page](https://matplotlib.org/). 

## List of Python Libraries Used: 
The following libraries were used to create the web-scraping code, process the data, and generate the figures. If you wish to recreate or attempt a similar project, these links might be useful. 

* **Selenium**: [Link to documentation](https://selenium-python.readthedocs.io/installation.html)
* **Beautiful Soup**:  [Link to documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
* **matplotlib**:  [Link to documentation](https://matplotlib.org/)
* **numpy**:  [Link to documentation](https://numpy.org/doc/)
* **pandas**:  [Link to documentation](https://pandas.pydata.org/docs/)
* **os**:  [Link to documentation](https://docs.python.org/3/library/os.html)
* **re**:  [Link to documentation](https://docs.python.org/3/library/re.html)
* **time**:  [Link to documentation](https://docs.python.org/3/library/time.html)
