"""
Contains helper functions for analyzing and plotting the election data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_subplots_bar(mean_label: str, values_outside_std_dev: list, mean: pd.Series, min_val: pd.Series, max_val: pd.Series, bar_colors: list) -> None:
    """
    Plots the regions or states that are more than 1.96 standard deviations from
    the mean.

    Args:
        mean_label (str): a string representing the label for the mean
        values_outside_std_dev (list): a list of integers or floats containing
        the values of the regions or states that are more than 1.96 standard
        deviations away from the mean.
        mean (pd.Series): a pandas Series containing all of the means for a
        country for each digit.
        min_val (pd.Series): a pandas Series representing the values 1.96
        standard deviations below the mean for each digit.
        max_val (pd.Series): a pandas Series representing the values 1.96
        standard deviations above the mean for each digit.
        bar_colors (list): A list of strings with two colors, such as 'green'
        and 'blue'. The first color is used for the country mean, and the
        second color is used for the regions or states that are outside of
        the given range.
    """    
    x = np.linspace(-1, 10, 100)
    fig, axs = plt.subplots(3, 3, figsize=(20, 20))
    for i, ax in enumerate(fig.axes):
        ax.set_xlim([-.5, 5])
        ax.set_title(f"Leading Digit: {i + 1}")
        ax.bar(mean_label, mean[i + 1], color=bar_colors[0])
        ax.plot(x, [max_val[i + 1]] * len(x))
        ax.plot(x, [min_val[i + 1]] * len(x))
        for area, digit, value in values_outside_std_dev:
            if digit == (i + 1):
                ax.bar(area, value, color=bar_colors[1])
        ax.margins(0, 0)
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
        plt.subplots_adjust(left=0.1,
                bottom=0.1, 
                right=0.9, 
                top=0.9, 
                wspace=0.4, 
                hspace=0.4)

def plot_labels(x_label: str = None, y_label: str = None, title: str = None):
    '''
    Adds title and labels to a plot. 

    Args: 
        x_label: a string representing the x-axis title
        y_label: a string representing the y-axis title
        title: a string representing the title of the chosen plot
    '''
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.tight_layout()


def plot_ideal_benfords_law_curve(num_values: int, color: str = "black", thickness: float = 1) -> None:
    '''
    Generates the theoretical values for the Benford's Law Curve for the first
    leading digit and plots these values as a line graph.

    Args:
        num_values: an integer representing the number of time steps. Will
        default to nine if a number greater than 9 is given.
    '''
    ideal_values = get_theoretical_benford_law_values(num_values)
    plt.plot(ideal_values.index, ideal_values, color=color,
             linewidth=thickness, label="Benford's Law Curve")

def find_all_leading_digits(data: pd.DataFrame, column_name: str = None, leading_digit: int = 1, threshold: int = 0) -> pd.DataFrame:
    """
    Takes data from a given csv file and finds all of the specified leading
    digits in the "votes" column and returns the leadings digits of each
    category in a Series.
    Note
    that any leading digits that are 0 will be removed as Benford's law does not
    apply to 0s, thus only values 1-9 will be returned.

    Args: 
        data: (DataFrame) A dataframe with the data. Must have one column with
        the name "votes" and if trying to find leading digit for categories in
        certain column, must also have column_name.
        column_name: (str) a single column from a dataframe containing the name
        of the column to find the leading digit of each unique category within
        or None if trying to find leading digit from entire dataframe.
        leading_digit: an integer representing which leading digit to grab, such
        as the 1st leading digit.
        threshold: integer representing the minimum number of discrete numbers
        in the votes column for a category to be included in the return
        dataframe

    Returns: 
        A pandas dataframe of integers containing all leading digits in the given column of
        the csv file. 
    """
    if column_name:
        dfs = get_vote_by_category(data, column_name, threshold)
    else:
        return pd.DataFrame(
            [
                int(str(vote)[leading_digit - 1])
                for vote in data["votes"]
                if str(vote)[leading_digit - 1] in ("123456789")
            ]
        )
    by_category = {}
    for category, value in dfs.items():
        by_category[category] = pd.Series(
            [
                int(str(vote)[leading_digit - 1])
                for vote in value
                if str(vote)[leading_digit - 1] in ("123456789")
            ]
        )

    return pd.DataFrame(by_category)


def get_vote_by_category(data: pd.DataFrame, column_name: str, threshold: int = 0) -> dict:
    """
    Finds the vote count by category, which is the unique values in a column of
    the data.

    For example, getting votes based on the candidate column will return a
    dictionary with the keys being the candidates, and each candidate
    mapped to a tuple of all votes received.

    Args:
        date (pd.DataFrame): a pandas DataFrame containing the data with the
        votes.
        column_name (str): a string representing the name of the column that
        will be used to sort through the votes. 
        threshold: integer representing the minimum number of discrete numbers
        in the votes column for a category to be included in the return
        dataframe

    Returns: 
        dict: A dictionary will categories as keys and dataframes and the rows
        belonging to them in data as a Series with the votes.
    """    
    return {key: val["votes"] for key, val in dict(tuple(data.groupby(by=column_name))).items() if val["votes"].size >= threshold}

def data_to_percentage(data_list: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a dataframe with one or more columns filled with digits and returns a
    dataframe with the percentages corresponding to the number of times the
    numbers 1-9 appear in each column.

    Args: 
        data_list: a dataframe of integers representing all of the leading
        digits from a dataset (in this case, the number of vote counts).
        Each columns is a category and is a Series with digits.
        threshold: (int) minimum number of integers in column for percentage
        to be found in it and for it to be returned.

    Returns: 
        returns a dataframe of Series with the percentages of each column that 
        are the numbers 1-9.
    """
    def per_column_percentage(column: pd.Series) -> pd.Series:
        number_of_occurrences = column.value_counts()
        number_of_occurrences = number_of_occurrences[
            (number_of_occurrences.index > 0) & (
                number_of_occurrences.index < 10)
        ]
        return number_of_occurrences.multiply(100 / sum(number_of_occurrences)).sort_index()

    return data_list.apply(per_column_percentage).dropna(axis=1)


def get_theoretical_benford_law_values(num_values: int = 9) -> pd.Series:
    """
    Generates a Series with the index being the x values of the Benford's law
    curve and the values being the y values of the curve.

    Args:
        num_values (int, optional): an integer representing the number of time
        steps. Will default to nine if a number greater than 9 is given.

    Returns:
        A pandas DataFrame containing the theoretical Benford's law distribution
        values.
    """    
    if num_values < 9:
        num_values = 9
    theoretical_x_values = np.linspace(1, 9, num_values)
    theoretical_y_values = np.log10(1 + 1 / theoretical_x_values) * 100
    return pd.Series(theoretical_y_values, index=theoretical_x_values)


def find_values_outside_range(data: pd.DataFrame, min_range: pd.Series, max_range: pd.Series) -> list:
    """
    Finds values in each column of data that fall below or above their respective
    value in min_range and max_range respectively.

    Args:
        data (pd.DataFrame): a pandas DataFrame containing the votes data.
        min_range (pd.Series): a pandas Series with the same length as data
        height.
        max_range (pd.Series): a pandas Series with same length as data height

    Returns:
        A list of tuples with the format (column name, value outside range) for
        each value outside range.
    """
    if min_range.size != len(data.index) or max_range.size != len(data.index):
        raise ValueError(
            "Length of data is not equal to length of min_range or max_range.")
    data_boolean = data.apply(lambda x: list(
        zip(x.lt(max_range), x.gt(min_range))))
    return_list = []
    for column in data_boolean:
        for index, element in data_boolean[column].iteritems():
            if False in element:
                return_list.append((column, index, data[column][index]))

    return return_list

def find_std_dev_range(data: pd.DataFrame) -> (pd.Series,pd.Series, pd.Series, pd.Series): 
    """
    Finds the mean and standard deviation for each row, and the values that are
    1.96 standard deviations below and above the mean.

    Args:
        data (pd.DataFrame): a pandas DataFrame containing the column with the
        votes data.  
    
    Returns:
        Four pandas Series containing the mean, standard deviation, maximum
        values, and minimum values.The maximum and minimum values represent the
        votes that are above or below 1.96 standard deviations from the mean.
    """    
    means = data.mean(axis=1)
    std_devs = data.std(axis=1, ddof=0)
    max_vals = pd.Series([mean + 1.96 * std_dev for mean, std_dev in zip(means, std_devs)], index=(1,2,3,4,5,6,7,8,9))
    min_vals = pd.Series([mean - 1.96 * std_dev for mean, std_dev in zip(means, std_devs)], index=(1,2,3,4,5,6,7,8,9))
    return means, std_devs, max_vals, min_vals
