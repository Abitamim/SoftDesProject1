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
    find_values_outside_range,
    find_std_dev_range,
)


# Define sets of test cases.
get_ideal_benfords = [
    # Check that default parameter value works.
    (
        [],
        pd.Series(
            np.array(
                [30.1, 17.609, 12.494, 9.691, 7.918, 6.694, 5.799, 5.115, 4.575]
            ),
            index=np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ),
    ),
    # Check that explicit parameter value works
    (
        [15],
        pd.Series(
            np.array(
                [
                    30.103,
                    21.388,
                    16.633,
                    13.622,
                    11.539,
                    10.012,
                    8.842,
                    7.918,
                    7.169,
                    6.55,
                    6.03,
                    5.586,
                    5.203,
                    4.869,
                    4.576,
                ]
            ),
            index=np.array(
                [
                    1,
                    1.571,
                    2.143,
                    2.714,
                    3.286,
                    3.857,
                    4.429,
                    5,
                    5.571,
                    6.143,
                    6.714,
                    7.286,
                    7.857,
                    8.429,
                    9,
                ]
            ),
        ),
    ),
    # Check that a value under 9 gives an error
    (
        [8],
        pd.Series(
            np.array(
                [30.1, 17.609, 12.494, 9.691, 7.918, 6.694, 5.799, 5.115, 4.575]
            ),
            index=np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ),
    ),
]
# data: pd.DataFrame, column_name: str = None, threshold: int = 0

find_all_leading_digits_cases = [
    # Check that a random dataset returns the correct dataframe with leading
    # digits. Also checks that the optional threshold parameter works.
    (
        pd.DataFrame(
            data={
                "random title": ["red", "red", "red", "blue", "blue"],
                "votes": [10, 15, 22, 111, 20],
            }
        ),
        ["random title"],
        [],
        pd.DataFrame(data={"blue": [1, 2, np.NaN], "red": [1, 1, 2]}),
    ),
    # Check that if the threshold value is 3, only leading digits for red
    # are returned
    (
        pd.DataFrame(
            data={
                "random title": ["red", "red", "red", "blue", "blue"],
                "votes": [10, 15, 22, 111, 20],
            }
        ),
        ["random title"],
        [3],
        pd.DataFrame(data={"red": [1, 1, 2]}),
    ),
    # Test case where optional parameters are not specified
    (
        pd.DataFrame(
            data={
                "random title": ["red", "red", "red", "blue", "blue"],
                "votes": [10, 15, 22, 111, 20],
            }
        ),
        [],
        [],
        pd.DataFrame(data={0: [1, 1, 2, 1, 2]}),
    ),
    # Test case where there are multiple columns with categories
    (
        pd.DataFrame(
            data={
                "random title": ["red", "red", "red", "blue", "blue"],
                "title2": ["r", "f", "r", "f", "r"],
                "votes": [10, 15, 22, 111, 20],
            }
        ),
        ["random title"],
        [],
        pd.DataFrame(data={"blue": [1, 2, np.NaN], "red": [1, 1, 2]}),
    ),
]

# get_vote_by_category(data: pd.DataFrame, column_name: str, threshold:
# int = 0)
get_vote_by_category_cases = [
    # Check that a dataFrame with 2 categories returns two columns with the
    # 'votes' for each category
    (
        pd.DataFrame(
            data={
                "random title": ["red", "red", "red", "blue", "blue"],
                "votes": [10, 15, 22, 111, 20],
            }
        ),
        "random title",
        [],
        {"blue": pd.Series([111, 20]), "red": pd.Series([10, 15, 22])},
    ),
    # Check that threshold works
    (
        pd.DataFrame(
            data={
                "random title": ["red", "red", "red", "blue", "blue"],
                "votes": [10, 15, 22, 111, 20],
            }
        ),
        "random title",
        [3],
        {"red": pd.Series([10, 15, 22])},
    ),
]

# data_to_percentage(data_list: pd.DataFrame) -> pd.DataFrame:
data_to_percentage_cases = [
    # Check that a dataframe with only 1s and leading digits returns 100%
    (
        pd.DataFrame(data={"leading digits": [1, 1, 1, 1, 1]}),
        pd.DataFrame(data={"leading digits": [100.0]}, index=[1]),
    ),
    # Check that a dataframe with more than one type of digit returns
    # the right percentages for all digits
    (
        pd.DataFrame(data={"leading digits": [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]}),
        (pd.DataFrame(data={"leading digits": [50.0, 50.0]}, index=[1, 2])),
    ),
    # Check that a dataframe with 2 columns returns the percentages for
    # the column that has more unique values
    (
        pd.DataFrame(
            data={
                "leading digits": [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
                "second column": [
                    1,
                    1,
                    1,
                    1,
                    np.NaN,
                    np.NaN,
                    np.NaN,
                    np.NaN,
                    np.NaN,
                    np.NaN,
                ],
            }
        ),
        (pd.DataFrame(data={"leading digits": [
         50.0, 50.0]}, index=[1.0, 2.0])),
    ),
]

# find_values_outside_range(data: pd.DataFrame, min_range: pd.Series,
# max_range: pd.Series) -> list:
find_values_outside_range_cases = [
    # Check that standard case with the height of data being equal to
    # the length of both max_range and min_range returns a list of tuples as
    # expected
    (
        pd.DataFrame(
            data={
                "votes": [10, 11, 12, 12, 13, 14],
                "votes2": [46, 32, 69, 420, 140, 2],
                "votes3": [1, 12, 56, 43, 24, 21],
            }
        ),
        pd.Series([10, 15, 2, 34, 96, 8]),
        pd.Series([20, 25, 34, 53, 112, 12]),
        [
            ("votes", 0, 10),
            ("votes", 1, 11),
            ("votes", 3, 12),
            ("votes", 4, 13),
            ("votes", 5, 14),
            ("votes2", 0, 46),
            ("votes2", 1, 32),
            ("votes2", 2, 69),
            ("votes2", 3, 420),
            ("votes2", 4, 140),
            ("votes2", 5, 2),
            ("votes3", 0, 1),
            ("votes3", 1, 12),
            ("votes3", 2, 56),
            ("votes3", 4, 24),
            ("votes3", 5, 21),
        ],
    ),
    (
        pd.DataFrame(
            data={
                "votes": [10, 11, 12, 12, 13, 14],
                "votes2": [46, 32, 69, 420, 140, np.NaN],
                "votes3": [1, 12, 56, 43, 24, 21],
            }
        ),
        pd.Series([10, 15, 2, 34, 96, 8]),
        pd.Series([20, 25, 34, 53, 112, 12]),
        [
            ("votes", 0, 10),
            ("votes", 1, 11),
            ("votes", 3, 12),
            ("votes", 4, 13),
            ("votes", 5, 14),
            ("votes2", 0, 46),
            ("votes2", 1, 32),
            ("votes2", 2, 69),
            ("votes2", 3, 420),
            ("votes2", 4, 140),
            ("votes3", 0, 1),
            ("votes3", 1, 12),
            ("votes3", 2, 56),
            ("votes3", 4, 24),
            ("votes3", 5, 21),
        ],
    ),
]

# find_values_outside_range(data: pd.DataFrame, min_range: pd.Series,
# max_range: pd.Series) -> list:
find_values_outside_range_cases_invalid = [
    # Check that invalid input with unequal
    (
        pd.DataFrame(
            data={
                "votes": [10, 11, 12, 12, 13, 9],
                "votes2": [46, 32, 69, 420, 140, 2],
                "votes3": [1, 12, 56, 43, 24, 21],
            }
        ),
        pd.Series([15, 2, 34, 96, 8]),
        pd.Series([20, 5, 34, 53, 46, 3]),
    ),
]

# find_std_dev_range(data: pd.DataFrame) -> (pd.Series,pd.Series,
# pd.Series, pd.Series):
find_std_dev_range_cases = [
    # Check that a dataframe with only ones in each row returns 1 for the mean, 0
    # for the standard deviation, 1 for the max value, 1 for the min value
    (
        pd.DataFrame(
            data={
                "col1": [1, 1, 1, 1, 1, 1, 1, 1, 1],
                "col2": [1, 1, 1, 1, 1, 1, 1, 1, 1],
                "col3": [1, 1, 1, 1, 1, 1, 1, 1, 1],
            },
            index=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        ),
        (
            pd.Series(data=9 * [1.0], index=[1, 2, 3, 4, 5, 6, 7, 8, 9]),
            pd.Series(data=9 * [0.0], index=[1, 2, 3, 4, 5, 6, 7, 8, 9]),
            pd.Series(data=9 * [1.0], index=[1, 2, 3, 4, 5, 6, 7, 8, 9]),
            pd.Series(data=9 * [1.0], index=[1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ),
    ),
    # Check that a dataframe with 3 columns of random values returns the correct
    # mean, standard deviation, max value, and min value
    (
        pd.DataFrame(
            data={
                "col1": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "col2": [9, 8, 7, 6, 5, 4, 3, 2, 1],
                "col3": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            },
            index=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        ),
        (
            pd.Series(
                data=[
                    3.666667,
                    4.000000,
                    4.333333,
                    4.666667,
                    5.000000,
                    5.333333,
                    5.666667,
                    6.000000,
                    6.333333,
                ],
                index=[1, 2, 3, 4, 5, 6, 7, 8, 9],
            ),
            pd.Series(
                data=[
                    3.771236,
                    2.828427,
                    1.885618,
                    0.942809,
                    0.000000,
                    0.942809,
                    1.885618,
                    2.828427,
                    3.771236,
                ],
                index=[1, 2, 3, 4, 5, 6, 7, 8, 9],
            ),
            pd.Series(
                data=[
                    11.058290,
                    9.543717,
                    8.029145,
                    6.514572,
                    5.000000,
                    7.181239,
                    9.362478,
                    11.543717,
                    13.724956,
                ],
                index=[1, 2, 3, 4, 5, 6, 7, 8, 9],
            ),
            pd.Series(
                data=[
                    -3.724956,
                    -1.543717,
                    0.637522,
                    2.818761,
                    5.000000,
                    3.485428,
                    1.970855,
                    0.456283,
                    -1.058290,
                ],
                index=[1, 2, 3, 4, 5, 6, 7, 8, 9],
            ),
        ),
    ),
]

# Define additional testing lists and functions that check other properties of
# functions in data_analysis.py
#------------------------------------------------------------------------------

@pytest.mark.parametrize("input_values,output", get_ideal_benfords)
def test_get_ideal_benfords(input_values, output):
    """
    Test that the get_theoretical_benford_law_values function works as intended.
    The function should return the values predicted by benford's law for each
    digit 1-9.

    Args:
        input_values(OPTIONAL): an integer representing the number of time steps
        (will default to 9).
        output: a pandas Series containing the predicted frequency of the digits
        1-9.
    """
    assert get_theoretical_benford_law_values(
        *input_values
    ).index.tolist() == pytest.approx(
        output.index.tolist(), 0.01
    ) and get_theoretical_benford_law_values(
        *input_values
    ).to_list() == pytest.approx(
        output.to_list(), 0.01
    )


@pytest.mark.parametrize(
    "data,column_name,threshold,output", find_all_leading_digits_cases
)
def test_find_all_leading_digits(data, column_name, threshold, output):
    """
    Test that the function find_all_leading_digits finds all of the leadings
    digits in a dataframe.

    Args:
        data: a pandas DataFrame containing the votes data (data with numerical
        values)
        column_name: a string representing the name of the column to sort the
        leading digits by
        threshold: integer representing the minimum number of digits in the
        column with data
        output: a pandas dataFrame containing all of the leading digits found in
        the given dataset that meet the threshold cutoff.
    """
    assert (
        pd.testing.assert_frame_equal(
            find_all_leading_digits(data, *column_name, *threshold),
            output,
            check_dtype=False,
        )
        is None
    )


@pytest.mark.parametrize(
    "data,column_name,threshold,output", get_vote_by_category_cases
)
def test_get_vote_by_category(data, column_name, threshold, output):
    """
    Test that the function get_vote_by_category works as intended. The function
    should return a dataframe of the votes sorted by the given category.

    Args:
        data: a dataframe containing the votes data and at least one category
        column
        column_name: a string representing the name of the category to sort by
        threshold: and integer representing the minimum number of digits in the
        column with data
        output: a pandas DataFrame containing the votes sorted by category
    """
    real_output = get_vote_by_category(data, column_name, *threshold)
    for category, values in real_output.items():
        assert (
            category in output.keys()
            and output[category].to_list() == values.to_list()
        )


@pytest.mark.parametrize("data,output", data_to_percentage_cases)
def test_data_to_percentage(data, output):
    """
    Test that the data_to_percentage function is returning a dataframe
    containing the percentage that each unique value occurs in the dataset

    Args:
        data: a pandas dataframe containing a column with some values
        output: a pandas dataframe containing the percentage of times that each
        unique value occurs in the dataset
    """
    assert (
        pd.testing.assert_frame_equal(data_to_percentage(data), output) is None
    )


@pytest.mark.parametrize(
    "data, min_range, max_range,output", find_values_outside_range_cases
)
def test_find_values_outside_range(data, min_range, max_range, output):
    """
    Test the function find_values_outside_range to check that it finds values in
    each column of data that fall below or above their respective
    value in min_range and max_range respectively.

    Args:
        data: a pandas dataframe containing the votes data
        min_range: a pandas Series containing the minimum probabilities that
        each digit 1-9 can occur
        max_range: a pandas Series containing the maximum probabilities that
        each digit 1-9 can occur
        output: a list of states that fall outside of the min and max range for
        each digit
    """
    assert find_values_outside_range(data, min_range, max_range) == output


@pytest.mark.parametrize(
    "data, min_range, max_range", find_values_outside_range_cases_invalid
)
def test_find_values_outside_range_invalid_input(data, min_range, max_range):
    """
    Test that the find_values_outside_range function returns an error if there
    is an invalid input

    Args:
        data: a pandas dataframe containing the votes data
        min_range: a pandas Series containing the minimum probabilities that
        each digit 1-9 can occur
        max_range: a pandas Series containing the maximum probabilities that
        each digit 1-9 can occur
    """
    with pytest.raises(ValueError):
        assert find_values_outside_range(data, min_range, max_range)


@pytest.mark.parametrize("data,output", find_std_dev_range_cases)
def test_find_std_dev_range(data, output):
    """
    Test that the find_std_dev_range function finds the mean and standard
    deviation for each row, and the values that are
    1.96 standard deviations below and above the mean.

    Args:
        data: a pandas dataframe containing the column with the votes data
        or some numerical data)
        output: four pandas Series containing the mean, standard deviation,
        min value, and max value for each digit.
    """
    data_output = find_std_dev_range(data)
    for i in range(4):
        assert (
            np.testing.assert_almost_equal(
                data_output[i].to_list(), output[i].to_list(), decimal=3
            )
            is None
        )
