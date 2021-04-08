"""
Test library functions to find and identify protein-coding genes in DNA.
"""
import pytest

from data_analysis import (
    get_complement,
)


# Define sets of test cases.
get_complement_cases = [
    # Check that the complement of A is T.
    ("A", "T"),
    # Check that the complement of C is G.
    ("C", "G"),
    # Check that the complement of T is A.
    ("T", "A"),
    # Check that the complement of G is C.
    ("G", "C"),
]

# Define additional testing lists and functions that check other properties of
# functions in gene_finder.py.
@pytest.mark.parametrize("nucleotide", ["A", "T", "C", "G"])
def test_double_complement(nucleotide):
    """
    Check that taking the complement of a complement of a nucleotide produces
    the original nucleotide.

    Args:
        nucleotide: A single-character string representing one of the four DNA
            nucleotides.
    """
    assert get_complement(get_complement(nucleotide)) == nucleotide