"""CSCA08 Assignment 3: arxiv.org

This code is provided solely for the personal and private use of
students taking the CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021-2023 Anya Tafliovich.

"""

from copy import deepcopy
import unittest
from arxiv_functions import get_most_published_authors as get_mpas


class TestGetMostPublishedAuthors(unittest.TestCase):
    """Test the function get_most_published_authors."""

    def setUp(self):
        self.example = {
            '008': {
                'identifier': '008',
                'title': 'Intro to CS is the best course ever',
                'created': '2021-09-01',
                'modified': None,
                'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
                'abstract': ('We present clear evidence that Introduction to\n'
                             'Computer Science is the best course.')},
            '031': {
                'identifier': '031',
                'title': 'Calculus is the best course ever',
                'created': None,
                'modified': '2021-09-02',
                'authors': [('Breuss', 'Nataliya')],
                'abstract': '''We discuss the reasons why Calculus I
                is the best course.'''},
            '067': {'identifier': '067',
                    'title': 'Discrete Mathematics is the best course ever',
                    'created': '2021-09-02',
                    'modified': '2021-10-01',
                    'authors': [('Bretscher', 'Anna'), ('Pancer', 'Richard')],
                    'abstract': (
                        'We explain why Discrete Mathematics is the best'
                        ' course of all times.')},
            '827': {
                'identifier': '827',
                'title': 'University of Toronto is the best university',
                'created': '2021-08-20',
                'modified': '2021-10-02',
                'authors': [('Bretscher', 'Anna'),
                            ('Ponce', 'Marcelo'),
                            ('Tafliovich', 'Anya Y.')],
                'abstract': ('We show a formal proof that the University of\n'
                             'Toronto is the best university.')},
            '042': {
                'identifier': '042',
                'title': None,
                'created': '2021-05-04',
                'modified': '2021-05-05',
                'authors': [],
                'abstract': ('This is a very strange article with no title\n'
                             'and no authors.')}
        }

    def test_handout_example(self):
        """Test get_most_published_authors with the handout example."""

        arxiv_copy = deepcopy(self.example)
        expected = [('Bretscher', 'Anna'),
                    ('Ponce', 'Marcelo'),
                    ('Tafliovich', 'Anya Y.')]
        actual = get_mpas(self.example)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_empty_list(self):
        """Test get_most_published_authors with empty list as argument."""

        arg_lst = []
        expected = []
        actual = get_mpas(arg_lst)
        msg = message(arg_lst,
                      str(expected), str(actual))
        self.assertEqual(actual, expected, msg)
        
    def test_single_author(self):
        """Test get_most_published_authors with single author as argument."""

        arg_lst = {'031': {'identifier': '031',
                             'title': 'Calculus is the best course ever',
                             'created': None,
                             'modified': '2021-09-02',
                             'authors': [('Breuss', 'Nataliya')],
                             'abstract': '''We discuss the reasons why 
                             Calculus I
                             is the best course.'''}}
        expected = [('Breuss', 'Nataliya')]
        actual = get_mpas(arg_lst)
        msg = message(arg_lst,
                      str(expected), str(actual))
        self.assertEqual(actual, expected, msg)   
        
    def test_equal_publications(self):
        """Test get_most_published_authors with equal publications"""

        arg_lst = ({'008': {'identifier': '008','title': 
                           'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
        'abstract': '''We present clear evidence that Introduction 
        to Computer Science is the best course.'''
    },
    '067': {
        'identifier': '067',
        'title': 'Discrete Mathematics is the best course ever',
        'created': '2021-09-02',
        'modified': '2021-10-01',
        'authors': [('Bretscher', 'Anna'), ('Pancer', 'Richard')],
        'abstract': '''We explain why Discrete 
        Mathematics is the best course of all times.'''
    }})
        expected = [('Bretscher', 'Anna'), ('Pancer', 'Richard'), 
                    ('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]
        actual = get_mpas(arg_lst)
        msg = message(arg_lst,
                      str(expected), str(actual))
        self.assertEqual(actual, expected, msg)         
        
    def test_non_equal_publications(self):
        """Test get_most_published_authors with an author with more
        publications than others"""

        arg_lst = {'067': {'identifier': '067',
            'title': 'Discrete Mathematics is the best course ever',
            'created': '2021-09-02',
            'modified': '2021-10-01',
            'authors': [('Bretscher', 'Anna'), ('Pancer', 'Richard')],
            'abstract': ('We explain why Discrete Mathematics is the best ' +
                         'course of all times.')},
    '827': {'identifier': '827',
        'title': 'University of Toronto is the best university',
        'created': '2021-08-20',
        'modified': '2021-10-02',
        'authors': [('Bretscher', 'Anna'),
                    ('Ponce', 'Marcelo'),
                    ('Tafliovich', 'Anya Y.')]}}
        expected = [('Bretscher', 'Anna')]
        actual = get_mpas(arg_lst)
        msg = message(arg_lst,
                      str(expected), str(actual))
        self.assertEqual(actual, expected, msg)         
    
    def test_publication_with_no_author(self):
        """Test get_most_published_authors with one article without author"""
        arg_lst = ({'042': {
                'identifier': '042',
                'title': None,
                'created': '2021-05-04',
                'modified': '2021-05-05',
                'authors': [],
                'abstract': '''This is a very strange article with no title
        and no authors.'''}
        })        
        expected = []
        actual = get_mpas(arg_lst)
        msg = message(arg_lst, str(expected), str(actual))
        self.assertEqual(actual, expected, msg)        
        

def message(test_case: dict, expected: list, actual: object) -> str:
    """Return an error message saying the function call
    get_most_published_authors(test_case) resulted in the value
    actual, when the correct value is expected.

    """

    return ('When we called get_most_published_authors(' + str(test_case)
            + ') we expected ' + str(expected)
            + ', but got ' + str(actual))


if __name__ == '__main__':
    unittest.main(exit=False)
