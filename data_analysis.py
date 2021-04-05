"""
Contains helper functions for analyzing the election data.
"""

import pandas as pd
import numpy as np

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
            if str(vote)[leading_digit - 1] in ("123456789")
        ]
    )


def data_to_percentage(data_list: pd.Series) -> pd.Series:
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
    return number_of_occurrences.multiply(100 / sum(number_of_occurrences)).sort_index()

def get_votes_per_parameter(data: pd.DataFrame, column_index: int) -> pd.DataFrame:
    """
    Get all of the votes for each region, county, candidate, or other parameter
    and store the data in a dataframe.

    This code works assuming that the votes are in the 2nd column (index=1)

    Args: 
        data: a pandas DataFrame containing all of the election data for a
        country.
        column_index: an integer representing the index of the column containing
        the parameter to sort the votes by. For example, to get the votes sorted
        by state for the US election, the index should be 3 because the names of
        the states are located in the dataframe in that index.

    Returns: 
        A pandas DataFrame containing all of the votes sorted by the chosen
        parameter.
    """    
    item_votes = {}
    for row in data.itertuples(index=False):
        item = row[column_index]
        votes = row[1]
        if item not in item_votes:
            item_votes[item] = [votes]
        else:
            item_votes[item].append(votes)
    return pd.DataFrame({index: pd.Series(value) for index, value in item_votes.items()})

def find_std_dev_to_ideal(gathered_data: pd.Series) -> float:
    """[summary]

    Args:
        gathered_data (pd.Series): Values must be in percentage terms

    Raises:
        Exception: [description]

    Returns:
        float: [description]
    """    
    theoretical_data = get_theoretical_benford_law_values()
    rms_sum = 0
    for data_index in gathered_data.index:
        if data_index not in theoretical_data.index:
            raise Exception("Please have only 1-9 in your index.")
        else:
            rms_sum += (theoretical_data[data_index] - gathered_data[data_index]) ** 2
            
    return (rms_sum / gathered_data.size) ** .5

def get_theoretical_benford_law_values(num_values = 9) -> pd.Series:
    '''
docstring here
'''
    theoretical_x_values = np.linspace(1, 9, num_values)
    theoretical_y_values = np.log10(1 + 1 / theoretical_x_values) * 100
    return pd.Series(theoretical_y_values, index = theoretical_x_values)

def sum_votes(data: pd.DataFrame, column_index: int) -> pd.DataFrame:
    '''
    docstring here
    '''
    votes = get_votes_per_parameter(data, column_index)
    return pd.DataFrame({index: value.sum() for index, value in votes.items()}, index=[0])

def find_std_dev(votes_data: pd.DataFrame, region_index:int):
    '''
    docstring here
    votes_data: dataframe containing all votes for a country 
    region_index: int representing the index where all the region names are located

    '''

    benford_law_ideal = get_theoretical_benford_law_values()
    standard_dev = {}
    region_percentages = pd.DataFrame()

    region_votes = get_votes_per_parameter(votes_data, region_index)
    for region in votes_data.columns:
        region_leading_digits = find_all_leading_digits(region_votes.iloc[:,region],1)
        region_percentages = data_to_percentage(region_leading_digits)

    




