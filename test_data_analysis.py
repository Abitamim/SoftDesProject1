"""
Test library functions to find and identify protein-coding genes in DNA.
"""

import pytest
import pandas as pd
import numpy as np

from data_analysis import (
    get_theoretical_benford_law_values,
    find_all_leading_digits,
    get_vote_by_category,
    data_to_percentage
)


# Define sets of test cases.
get_ideal_benfords= [
    # Check that default parameter value works.
    ([], pd.Series(np.array([30.1, 17.609, 12.494, 9.691, 7.918, 6.694, 5.799, 5.115, 4.575]), index=np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]))),
    # Check that explicit parameter value works
    ([15], pd.Series(np.array([30.103, 21.388, 16.633, 13.622, 11.539, 10.012, 8.842, 7.918, 7.169, 6.55, 6.03, 5.586, 5.203, 4.869, 4.576]), index=np.array([1, 1.571, 2.143, 2.714, 3.286, 3.857, 4.429, 5, 5.571, 6.143, 6.714, 7.286, 7.857, 8.429, 9]))),
    # Check that a value under 9 gives an error
    ([8], pd.Series(np.array([30.1, 17.609, 12.494, 9.691, 7.918, 6.694, 5.799, 5.115, 4.575]), index=np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]))),
]
#data: pd.DataFrame, column_name: str = None, leading_digit: int = 1, threshhold: int = 0

find_all_leading_digits_cases = [
    #Check that a random dataset returns the correct dataframe with leading
    #digits 
    ([pd.dataFrame(data={'random title': ['red', 'red', 'red', 'blue', 'blue'],'votes':[10,15,22,111,20]}), 'random title', 1],pd.dataFrame(data={'index':[0,1,2,3,4],'red':[1, 1, 2] ,'blue': [1, 2]})),
    #Check that if the threshhold value is 3, only leading digits for red
    #are returned
    ([pd.dataFrame(data={'random title': ['red', 'red', 'red', 'blue', 'blue'],'votes':[10,15,22,111,20]}), 'random title', 1, 3],pd.dataFrame(data={'index':[0,1,2,3,4],'red':[1, 1, 2]})),
    
]

#get_vote_by_category(data: pd.DataFrame, column_name: str, threshhold: int = 0)
get_vote_by_category_cases = [
    #Check that a dataFrame with 2 categories returns two columns with the
    #'votes' for each category
    ([pd.dataFrame(data = {'categories': ['red','red','red','red','blue','blue','blue'],'votes':[1, 1, 1, 1, 2, 2, 2]}), 'categories'], pd.dataFrame(data={'index':[0,1,2,3,4],'red':[1,1,1,1],'blue':[2,2,2]})),
]

#data_to_percentage(data_list: pd.DataFrame) -> pd.DataFrame:
data_to_percentage_cases = [
    #Check that 
    (),
]



# Define additional testing lists and functions that check other properties of
# functions in data_analysis.py
@pytest.mark.parametrize("input,output", get_ideal_benfords)
def test_get_ideal_benfords(input, output):
    assert get_theoretical_benford_law_values(*input).index.tolist() == pytest.approx(output.index.tolist(), .01) and get_theoretical_benford_law_values(*input).to_list() == pytest.approx(output.to_list(), .01) 

@pytest.mark.parametrize("input,output", find_all_leading_digits_cases)
def test_find_all_leading_digits(input, output): 
    assert find_all_leading_digits(input) == output

@pytest.mark.parametrize("input,output", get_vote_by_category_cases)
def test_get_vote_by_category(input, output): 
    assert get_vote_by_category(input) == output

@pytest.mark.parametrize("input,output", data_to_percentage_cases)
def test_data_to_percentage(input, output): 
    assert data_to_percentage(input) == output