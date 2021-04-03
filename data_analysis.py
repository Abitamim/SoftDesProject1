'''
Contains helper functions for analyzing the election data.
'''

import pandas as pd
from collections import Counter


def csv_to_dataframe(csv_filepath: str):
    '''
    Takes a csv file and turns it into a dataframe.

    Args: 
        csv_filepath: a string representing the path to the csv file containing
        all of the election data.
    Returns:
        a dataframe containing all of the data from a given csv file. 
    '''
    return pd.read_csv(f'{csv_filepath}')


def find_all_leading_digits(dataframe, leading_digit: int, column_name: str):
    '''
    Takes data from a given csv file and finds all of the specified leading
    digits in the given column and returns the leadings digits in a list. Note
    that any leading digits that are 0 will be removed as Benford's law does not
    apply to 0s, thus only values 1-9 will be returned.

    Args: 
        dataframe: a dataframe containing the election data
        leading_digit: an integer representing which leading digit to grab, such
        as the 1st leading digit.
        column_name: a string representing the column in the csv file that
        contains the integers to find the leading digit of. 
    Returns: 
        A list of integers containing all leading digits in the given column of
        the csv file. 
    '''
    return [int(str(vote)[leading_digit-1]) for vote in dataframe[f'{column_name}'] if int(str(vote)[leading_digit-1]) != 0]

def data_to_percentage(data_list):
    '''
    Takes a list of integer data and returns a list of percentages corresponding
    to the number of times the numbers 1-9 appear in the list.

    Args: 
        data_list: a list of integers representing all of the leading digits
        from a dataset (in this case, the number of vote counts). 

    Returns: 
        returns a list of floats representing the percentages of that data that are
        the numbers 1-9.
    '''
    number_of_occurrences = Counter(data_list)
    return [(number_of_occurrences[number]/len(data_list))*100 for number in range(1, 9)]

