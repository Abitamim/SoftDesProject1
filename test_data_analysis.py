"""
Test the data analysis code. 
"""

import pytest
import data_analysis


# Define sets of test cases.
get_percentages = [
    #One number is 100% of the list
    (1,[1],100.0)
    (2,[2],100.0)
    (1,[1,1,1,2,2,2],50.0)

]

# Define standard testing functions to check functions' outputs given certain
# inputs defined above.
@pytest.mark.parametrize("number, data_list, percentage", get_percentages)
def test_get_complement(number, data_list, percentage):
    """
    docstring here
    """
    assert data_analysis.data_to_percentage(data_list, number) == percentage