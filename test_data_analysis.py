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
    data_to_percentage, 
    find_std_dev_range, 
    find_values_outside_range
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
#data: pd.DataFrame, column_name: str = None, leading_digit: int = 1, threshold: int = 0

# find_all_leading_digits_cases = [
#     #Check that a random dataset returns the correct dataframe with leading
#     #digits 
#     (pd.DataFrame(data={'random title': ['red', 'red', 'red', 'blue', 'blue'],'votes':[10,15,22,111,20]}), ['random title'],[1],[],pd.DataFrame(data={'red':[1, 1, 2] ,'blue': [1, 2, np.NaN]})),
#     #Check that if the threshold value is 3, only leading digits for red
#     #are returned
#     (pd.DataFrame(data={'random title': ['red', 'red', 'red', 'blue', 'blue'],'votes':[10,15,22,111,20]}), ['random title'],[1],[3],pd.DataFrame(data={'red':[1, 1, 2]})),
    
# ]

# #get_vote_by_category(data: pd.DataFrame, column_name: str, threshold: int = 0)
# get_vote_by_category_cases = [
#     #Check that a dataFrame with 2 categories returns two columns with the
#     #'votes' for each category
#     (pd.dataFrame(data = {'categories': ['red','red','red','red','blue','blue','blue'],'votes':[1, 1, 1, 1, 2, 2, 2]}), 'categories', pd.dataFrame(data={'index':[0,1,2,3,4],'red':[1,1,1,1],'blue':[2,2,2]})),
# ]

#data_to_percentage(data_list: pd.DataFrame) -> pd.DataFrame:
data_to_percentage_cases = [
    #Check that a dataframe with only 1s and leading digits returns 100%
    (pd.DataFrame(data = {'leading digits': [1, 1, 1, 1, 1]}), pd.DataFrame(data = {'leading digits':[100.0]}, index = [1])),
    #Check that a dataframe with more than one type of digit returns
    #the right percentages for all digits
    (pd.DataFrame(data = {'leading digits': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]}), (pd.DataFrame(data = {'leading digits': [50.0,50.0]}, index = [1,2]))),
    #Check that a dataframe with 2 columns returns the percentages for
    #the column that has more unique values
    (pd.DataFrame(data = {'leading digits': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],'second column': [1, 1, 1, 1,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN]}), (pd.DataFrame(data = {'leading digits': [50.0,50.0]}, index = [1.0,2.0]))),
]

# #find_values_outside_range(data: pd.DataFrame, min_range: pd.Series, max_range: pd.Series) -> list:
# find_values_outside_range_cases = [
#     #Check that 
#     (pd.DataFrame(data = {'votes':[10,11,12,12,13,14]}), pd.Series()),
# ]

#find_std_dev_range(data: pd.DataFrame) -> (pd.Series,pd.Series, pd.Series, pd.Series):
find_std_dev_range_cases = [
    #Check that a dataframe with only ones in each row returns 1 for the mean, 0
    #for the standard deviation, 1 for the max value, 1 for the min value
    (pd.DataFrame(data = {'col1': [1,1,1,1,1,1,1,1,1],'col2': [1,1,1,1,1,1,1,1,1], 'col3': [1,1,1,1,1,1,1,1,1]},index = [1,2,3,4,5,6,7,8,9]), \
        (pd.Series(data = 9*[1.0], index = [1,2,3,4,5,6,7,8,9]),\
        pd.Series(data = 9*[0.0], index = [1,2,3,4,5,6,7,8,9]),\
        pd.Series(data = 9*[1.0], index = [1,2,3,4,5,6,7,8,9]),\
        pd.Series(data = 9*[1.0], index = [1,2,3,4,5,6,7,8,9]))), 
    #Check that a dataframe with 3 columns of random values returns the correct
    #mean, standard deviation, max value, and min value
    (pd.DataFrame(data = {'col1': [1,2,3,4,5,6,7,8,9],'col2': [9,8,7,6,5,4,3,2,1], 'col3': [1,2,3,4,5,6,7,8,9]},index = [1,2,3,4,5,6,7,8,9]),\
          (pd.Series(data = [3.666667,4.000000,4.333333,4.666667,5.000000,5.333333,5.666667,6.000000,6.333333], index = [1,2,3,4,5,6,7,8,9]),\
          pd.Series(data = [3.771236,2.828427,1.885618,0.942809,0.000000,0.942809,1.885618,2.828427,3.771236], index = [1,2,3,4,5,6,7,8,9]),\
          pd.Series(data = [11.058290, 9.543717,8.029145,6.514572,5.000000,7.181239,9.362478,11.543717,13.724956], index = [1,2,3,4,5,6,7,8,9]),\
          pd.Series(data = [-3.724956,-1.543717,0.637522,2.818761,5.000000,3.485428,1.970855,0.456283,-1.058290], index = [1,2,3,4,5,6,7,8,9]))),
]

# Define additional testing lists and functions that check other properties of
# functions in data_analysis.py
@pytest.mark.parametrize("input,output", get_ideal_benfords)
def test_get_ideal_benfords(input, output):
    assert get_theoretical_benford_law_values(*input).index.tolist() == pytest.approx(output.index.tolist(), .01) and get_theoretical_benford_law_values(*input).to_list() == pytest.approx(output.to_list(), .01) 

# @pytest.mark.parametrize("data,column_name,leading_digit,threshold,output", find_all_leading_digits_cases)
# def test_find_all_leading_digits(data, column_name, leading_digit, threshold, output): 
#     assert find_all_leading_digits(data, *column_name, *leading_digit, *threshold).eq(output)

# @pytest.mark.parametrize("data,column_name,threshold,output", get_vote_by_category_cases)
# def test_get_vote_by_category(data, column_name, threshold, output): 
#     assert get_vote_by_category(data, column_name, threshold) == output

@pytest.mark.parametrize("data,output", data_to_percentage_cases)
def test_data_to_percentage(data, output): 
    assert pd.testing.assert_frame_equal(data_to_percentage(data), output) == None

# @pytest.mark.parametrize("data, min_range, max_range,output", find_values_outside_range_cases)
# def test_find_values_outside_range(data, min_range, max_range, output): 
#     assert pd.testing.assert_frame_equal(find_values_outside_range(data, min_range, max_range), output) == None

@pytest.mark.parametrize("data,output", find_std_dev_range_cases)
def test_find_std_dev_range(data,output): 
    data_output = find_std_dev_range(data)
    for i in range(4):
        assert np.testing.assert_almost_equal(data_output[i].to_list(), output[i].to_list(), decimal = 3) == None
        