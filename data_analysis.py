"""
Contains helper functions for analyzing the election data.
"""

import pandas as pd


def csv_to_dataframe(csv_filepath: str):
    """
    Takes a csv file and turns it into a dataframe.

    Args: 
        csv_filepath: a string representing the path to the csv file containing
        all of the election data.
    Returns:
        a dataframe containing all of the data from a given csv file. 
    """
    return pd.read_csv(f"{csv_filepath}")


def find_all_leading_digits(column, leading_digit: int):
    """
    Takes data from a given csv file and finds all of the specified leading
    digits in the given column and returns the leadings digits in a list. Note
    that any leading digits that are 0 will be removed as Benford's law does not
    apply to 0s, thus only values 1-9 will be returned.

    Args: 
        column: a single column from a dataframe containing the election votes
        leading_digit: an integer representing which leading digit to grab, such
        as the 1st leading digit.
        
    Returns: 
        A list of integers containing all leading digits in the given column of
        the csv file. 
    """
    return pd.Series(
        [
            int(str(vote)[leading_digit - 1])
            for vote in column
            if int(str(vote)[leading_digit - 1]) != 0
        ]
    )


def data_to_percentage(data_list: pd.Series):
    """
    Takes a list of integer data and returns a list of percentages corresponding
    to the number of times the numbers 1-9 appear in the list.

    Args: 
        data_list: a list of integers representing all of the leading digits
        from a dataset (in this case, the number of vote counts). 

    Returns: 
        returns a list of floats representing the percentages of that data that 
        are the numbers 1-9.
    """
    number_of_occurrences = data_list.value_counts()
    number_of_occurrences = number_of_occurrences[
        (number_of_occurrences.index > 0) & (number_of_occurrences.index < 10)
    ]
    return number_of_occurrences.multiply(100 / sum(number_of_occurrences))

def per_candidate_votes(data: pd.DataFrame) -> pd.DataFrame:
    """[summary]

    Args:
        data (pd.DataFrame): [description]

    Returns:
        pd.DataFrame: [description]
    """    
    candidate_votes = {}
    for row in data.itertuples(index=False):
        candidate = row[0]
        votes = row[1]
        if candidate not in candidate_votes:
            candidate_votes[candidate] = [votes]
        else:
            candidate_votes[candidate].append(votes)
    return pd.DataFrame({index: pd.Series(value) for index, value in candidate_votes.items()})

# us_data = csv_to_dataframe('data/2020-elections-data.csv')
# x = per_candidate_votes(us_data)
# print(x)

def get_votes_by_region(data: pd.DataFrame)-> pd.DataFrame:
    '''
    Get all of the votes for each region or county and place it into
    a dataframe sorted by each county or region. 

    This code works assuming that the votes are in the 2nd column (index=1)
    and the region name is in column 3 (index = 2).

    Args: 
        data: a pandas DataFrame containing all of the election data for a
        country.

    Returns: 
        A pandas DataFrame containing all of the votes sorted by each region
        or country.
    '''
    #dictionary to store all the votes for each region or county
    region_votes = {}
    #a temporary list to store the votes for one region as the DataFrame
    #is iterated through
    one_region_votes = ''
    #get the name of the first region in the dataframe
    current_region = data.iloc[0,3]

    for row in data.itertuples(index = False):
        if row[3] != current_region:
            region_votes[current_region] = one_region_votes.split(',')
            current_region = row[3]
            one_region_votes = ''
        one_region_votes+=str(row[1])+','
    
    return pd.DataFrame(region_votes)
