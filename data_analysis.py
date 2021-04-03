'''
Contains helper functions for analyzing the election data.
'''

import pandas as pd
from collections import Counter

def csv_to_dataframe(csv_filepath:str):
    '''
    Takes a csv file and turns it into a dataframe.

    Args: 
        csv_filepath: a string representing the path to the csv file containing
        all of the election data.
    Returns:
        a dataframe containing all of the data from a given csv file. 
    '''
    return pd.read_csv(f'{csv_filepath}')

def find_all_leading_digits(dataframe, leading_digit:int, column_name:str):
    '''
    Takes data from a given csv file and finds all of the specified leading
    digits in the given column and returns the leadings digits in a list. Note
    that any leading digits that are 0 will be removed as Benford's law does not
    apply to 0s.

    Args: 
        dataframe: a dataframe containing the election data
        leading_digit: an integer representing which leading digit to grab, such
        as the 1st leading digit.
        column_name: a string representing the column in the csv file that
        contains the integers to find 
        the leading digit of. 
    Returns: 
        A list of integers containing all leading digits in the given column of
        the csv file. 
    '''
    #should we add something that checks if that digit does 
    #not exist in some numbers and ask the person to retry wth a different number? 

    return [int(str(vote)[leading_digit-1]) for vote in dataframe[f'{column_name}']]
    

def data_to_percentage(data_list, number:int):
    '''
    Takes a list of integer data and an integer, and determines what percent of
    the data is that integer. For this project, the data_list is the list of
    leading digits, and the number is between 1-9.

    Args: 
        data_list: a list of integers representing all of the leading digits
        from a dataset (in this case, the number of vote counts). 
        number: an integer representing a number between 1-9.
    
    Returns: 
        returns a float representing the percentage of that data that is
        the given number.
    '''
    number_of_occurances = Counter(data_list)
    return (number_of_occurances[number]/len(data_list))*100