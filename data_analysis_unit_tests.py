"""
Test library functions to find and identify protein-coding genes in DNA.
"""
import pytest
import pandas as pd
import numpy as np

from data_analysis import (
    get_theoretical_benford_law_values,
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

# Define additional testing lists and functions that check other properties of
# functions in gene_finder.py.
@pytest.mark.parametrize("input,output", get_ideal_benfords)
def test_get_ideal_benfords(input, output):
    assert get_theoretical_benford_law_values(*input).index.tolist() == pytest.approx(output.index.tolist(), .01) and get_theoretical_benford_law_values(*input).to_list() == pytest.approx(output.to_list(), .01) 