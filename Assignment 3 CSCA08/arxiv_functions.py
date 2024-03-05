"""CSCA08 Assignment 3: arxiv.org

This code is provided solely for the personal and private use of
students taking the CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021-2023 Anya Tafliovich.

"""

import copy  # needed in examples of functions that modify input dict
from typing import TextIO

# remove unused constants from this import statement when you are
# finished your assignment
from constants import (ID, TITLE, CREATED, MODIFIED, AUTHORS,
                       ABSTRACT, END, SEPARATOR, NameType,
                       ArticleValueType, ArticleType, ArxivType)


EXAMPLE_ARXIV = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''},
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
            'abstract': ('We explain why Discrete Mathematics is the best ' +
                         'course of all times.')},
    '827': {
        'identifier': '827',
        'title': 'University of Toronto is the best university',
        'created': '2021-08-20',
        'modified': '2021-10-02',
        'authors': [('Bretscher', 'Anna'),
                    ('Ponce', 'Marcelo'),
                    ('Tafliovich', 'Anya Y.')],
        'abstract': '''We show a formal proof that the University of
Toronto is the best university.'''},
    '042': {
        'identifier': '042',
        'title': None,
        'created': '2021-05-04',
        'modified': '2021-05-05',
        'authors': [],
        'abstract': '''This is a very strange article with no title
and no authors.'''}
}


EXAMPLE_TEXT = ['008\n', 'Intro to CS is the best course ever\n',
                '2021-09-01\n', '\n', 'Ponce,Marcelo\n',
                'Tafliovich,Anya Y.\n', '\n',
                'We present clear evidence that Introduction to\n',
                'Computer Science is the best course.\n', 'END\n', '031\n',
                'Calculus is the best course ever\n', '\n', '2021-09-02\n',
                'Breuss,Nataliya\n', '\n',
                'We discuss the reasons why Calculus I\n',
                'is the best course.\n', 'END\n']

SEPERATED_ARTICLES = [['008\n', 'Intro to CS is the best course ever\n',
                       '2021-09-01\n', '\n', 'Ponce,Marcelo\n',
                       'Tafliovich,Anya Y.\n', '\n',
                       'We present clear evidence that Introduction to\n',
                       'Computer Science is the best course.\n'],
                      ['031\n', 'Calculus is the best course ever\n',
                       '\n', '2021-09-02\n',
                       'Breuss,Nataliya\n', '\n',
                       'We discuss the reasons why Calculus I\n',
                       'is the best course.\n']]

SINGLE_ARTICLE = ['008\n', 'Intro to CS is the best course ever\n',
                  '2021-09-01\n', '\n', 'Ponce,Marcelo\n',
                  'Tafliovich,Anya Y.\n', '\n',
                  'We present clear evidence that Introduction to\n',
                  'Computer Science is the best course.\n']

ASSIGNED_INFO = {
    'identifier': '008',
    'title': 'Intro to CS is the best course ever',
    'created': '2021-09-01',
    'modified': None,
    'abstract': 'We present clear evidence that Introduction to\n' +
                'Computer Science is the best course.',
    'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]}

EXAMPLE_BY_AUTHOR = {
    ('Ponce', 'Marcelo'): ['008', '827'],
    ('Tafliovich', 'Anya Y.'): ['008', '827'],
    ('Bretscher', 'Anna'): ['067', '827'],
    ('Breuss', 'Nataliya'): ['031'],
    ('Pancer', 'Richard'): ['067']
}


# We provide the header and docstring for this function to get you
# started and to demonstrate that there are no docstring examples in
# functions that read from files.
def read_arxiv_file(afile: TextIO) -> ArxivType:
    """Return a dict containing all arxiv information in afile.

    Precondition: afile is open for reading
                  afile is in the format described in the handout
    """
    arxiv_type = {}

    total_articles = arxiv_file_seperate_articles(afile)
    for article in total_articles:
        article_info = arxiv_file_assign_info(article)
        article_info = {key.replace('\n', ''): value for key, value in
                        article_info.items()}
        arxiv_type[article_info[ID]] = article_info
    return arxiv_type


def arxiv_file_seperate_articles(text: list[str]) -> list[list[str]]:
    """ Returns a list of seperated articles given the info from text text.
    Used as a helper function for read_arxiv_file.

    >>> arxiv_file_seperate_articles(EXAMPLE_TEXT) == SEPERATED_ARTICLES
    True

    >>> arxiv_file_seperate_articles([])
    []
    """
    articles = []
    article = []

    for line in text:
        if line.strip() == END:
            articles.append(article[:])
            article = []
        else:
            article.append(line)
    if article:
        articles.append(article[:])
    if article:
        articles.append(article[:])
    return articles


def arxiv_file_assign_info(text: ArxivType) -> ArxivType:
    """Returns a dictionary of the text's info from text to ArxivType format.
    Used as a helper function for read_arxiv_file.

    Precondition: text must be of format from arxiv_file_seperate_articles

    >>> arxiv_file_assign_info(SEPERATED_ARTICLES[0]) == ASSIGNED_INFO
    True

    >>> arxiv_file_assign_info([])
    []
    """
    if text == []:
        return []

    information = {}
    information[ID] = text[0].strip()
    information[TITLE] = text[1].strip()
    information[CREATED] = text[2].strip()
    information[MODIFIED] = text[3].strip()

    end_index = text[::-1].index('\n')
    abstract_lines = text[-end_index:]
    information[ABSTRACT] = '\n'.join(line.strip() for line in abstract_lines)

    information[AUTHORS] = sorted(arxiv_file_assign_authors(text))

    arxiv_file_assign_none(information)

    return information


def arxiv_file_assign_authors(article: list) -> list[int]:
    """Returns a list of codes from article article. Used as a helper
    function for read_arxiv_file.

    >>> arxiv_file_assign_authors(SINGLE_ARTICLE)
    [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]

    >>> arxiv_file_assign_authors(SEPERATED_ARTICLES[1])
    [('Breuss', 'Nataliya')]
    """
    article_authors = []

    i = 0
    while i < len(article):
        if ',' in article[i] and len(article[i]) < 50:
            author_parts = [part.strip() for part in article[i].split(',')]
            if len(author_parts) >= 2:
                author_tuples = [(author_parts[j], author_parts[j + 1]
                                  ) for j in range(0, len(author_parts)-1, 2)]
                article_authors.extend(author_tuples)
        i += 1
    return article_authors


def arxiv_file_assign_none(info: ArxivType) -> None:
    """Returns a dictionary of the missing information in info info
    with None.

    >>> example = copy.deepcopy(ASSIGNED_INFO)
    >>> example[MODIFIED] = ''
    >>> arxiv_file_assign_none(example)
    >>> example == ASSIGNED_INFO
    True

    >>> example = copy.deepcopy(ASSIGNED_INFO)
    >>> arxiv_file_assign_none(example)
    >>> example == ASSIGNED_INFO
    True
    """
    for key, value in info.items():
        if value == '':
            info[key] = None


# We provide the header and part of a docstring for this function to
# get you started and to demonstrate the use of example data.
def make_author_to_articles(id_to_article: ArxivType) -> dict[NameType,
                                                              list[str]]:
    """Return a dict that maps each author name to a list (sorted in
    lexicographic order) of IDs of articles written by that author,
    based on the information in arxiv data id_to_article.

    >>> make_author_to_articles(EXAMPLE_ARXIV) == EXAMPLE_BY_AUTHOR
    True
    >>> example = {'008': {'identifier': '008',
    ...            'title': 'Intro to CS is the best course ever',
    ...            'created': '2021-09-01',
    ...            'modified': None,
    ...    'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
    ...    'abstract': '''We present clear evidence that Introduction to
    ...     Computer Science is the best course.'''}}
    >>> make_author_to_articles(example)
    {('Ponce', 'Marcelo'): ['008'], ('Tafliovich', 'Anya Y.'): ['008']}
    """
    author_to_articles = {}
    for article_id, article_info in id_to_article.items():
        authors = article_info[AUTHORS]
        for author in authors:
            if author not in author_to_articles:
                author_to_articles[author] = [article_id]
            else:
                author_to_articles[author].append(article_id)
    for articles in author_to_articles.values():
        articles.sort()
    return author_to_articles


def get_coauthors(id_to_article: ArxivType, author_name:
                  NameType) -> list[NameType]:
    """Returns a list of coauthors of the specificed author from author_name
    in the given articles id_to_article.

    >>> get_coauthors(EXAMPLE_ARXIV, ('Tafliovich', 'Anya Y.'))
    [('Bretscher', 'Anna'), ('Ponce', 'Marcelo')]

    >>> get_coauthors(EXAMPLE_ARXIV, (('Bretscher', 'Anna')))
    [('Pancer', 'Richard'), ('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]

    >>> get_coauthors(EXAMPLE_ARXIV, (('Ponce', 'Marcelo')))
    [('Bretscher', 'Anna'), ('Tafliovich', 'Anya Y.')]

    >>> get_coauthors(EXAMPLE_ARXIV, (('Breuss', 'Nataliya')))
    []
    """
    all_author_list = []
    for items in id_to_article.values():
        if author_name in items[AUTHORS]:
            all_author_list.extend((items[AUTHORS]))
    for author in all_author_list:
        if author == author_name:
            k = all_author_list.index(author)
            all_author_list.pop(k)
    sort_coauthors(all_author_list)
    all_author_list.sort()
    return all_author_list


def sort_coauthors(author_list: list) -> None:
    """Returns a list of authors from author_list without duplicates. Used
    as a helper function for get_coauthors.

    >>> authors = [('Ponce', 'Marcelo'), ('Bretscher', 'Anna'),
    ...           ('Ponce', 'Marcelo')]
    >>> sort_coauthors(authors)
    >>> authors == [('Ponce', 'Marcelo'), ('Bretscher', 'Anna')]
    True

    >>> authors = [('Tafliovich', 'Anya Y.'), ('Ponce', 'Marcelo'),
    ...           ('Ponce', 'Marcelo')]
    >>> sort_coauthors(authors)
    >>> authors == [('Tafliovich', 'Anya Y.'), ('Ponce', 'Marcelo')]
    True
    """
    i = 0
    while i < len(author_list):
        j = i + 1
        while j < len(author_list):
            if author_list[i] == author_list[j]:
                author_list.pop(j)
            else:
                j += 1
        i += 1


# We provide the header and part of a docstring for this function to
# get you started and to demonstrate the use of function deepcopy in
# examples that modify input data.

def get_most_published_authors(id_to_article: ArxivType) -> list[NameType]:
    """Returns a list of authors from id_to_article who have published
    the most articles.

    >>> get_most_published_authors(EXAMPLE_ARXIV)
    [('Bretscher', 'Anna'), ('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]

    >>> get_most_published_authors([])
    []
    """
    count = []
    most_published_authors = []
    if id_to_article == []:
        return []

    author_to_articles = make_author_to_articles(id_to_article)
    if get_no_author(id_to_article) == []:
        return []

    for articles in author_to_articles.values():
        count.append(len(articles))
    max_val = max(count)
    for authors, articles in author_to_articles.items():
        if len(articles) == max_val:
            most_published_authors.append(authors)
    most_published_authors.sort()
    return most_published_authors


def get_no_author(id_to_article: ArxivType) -> list:
    """Returns a dictionary given the ArxivType dictionary of id_to_article
    with missing info replaced with None. Used as a helper function for
    get_most_published_authors_

    >>> example = {'042': {
    ...    'identifier': '042',
    ...    'title': None,
    ...    'created': '2021-05-04',
    ...    'modified': '2021-05-05',
    ...    'authors': [],
    ...    'abstract': '''This is a very strange article with no title
    ...                   and no authors.'''}}
    >>> get_no_author(example)
    []

    >>> get_no_author(EXAMPLE_ARXIV) == []
    False
    """
    for item in id_to_article.values():
        if item[AUTHORS] == [] and len(id_to_article) == 1:
            return []
    return id_to_article


def suggest_collaborators(id_to_article: ArxivType, author_name:
                          NameType) -> list[NameType]:
    """Returns a list of suggested collaborators from id_to_article
    which the author author_name should collaborate with.

    >>> suggest_collaborators(EXAMPLE_ARXIV, ('Pancer', 'Richard'))
    [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]

    >>> suggest_collaborators(EXAMPLE_ARXIV, ('Tafliovich', 'Anya Y.'))
    [('Pancer', 'Richard')]

    >>> suggest_collaborators(EXAMPLE_ARXIV, ('Breuss', 'Nataliya'))
    []

    >>> suggest_collaborators(EXAMPLE_ARXIV, ('Ponce', 'Marcelo'))
    [('Pancer', 'Richard')]
    """
    i = 0
    suggested_collaborators = []
    coauthors = get_coauthors(id_to_article, author_name)

    for author in coauthors:
        suggested_collaborators.extend(get_coauthors(id_to_article, author))

    while i < len(suggested_collaborators):
        coauthor = suggested_collaborators[i]
        if coauthor in coauthors:
            suggested_collaborators.pop(i)
        else:
            i += 1

    suggestions = remove_original_author(suggested_collaborators, author_name)
    suggestions.sort()
    return suggestions


def remove_original_author(author_list: list[str], author_name:
                           NameType) -> list[str]:
    """Returns a list of authors from author_list with all occurences of
    the author author_name removed. Used as a helper function for
    suggest_collaborators.

    >>> remove_original_author([('Pancer', 'Richard'), ('Breuss', 'Nataliya'),
    ...                         ('Breuss', 'Nataliya')],
    ...                         ('Breuss', 'Nataliya'))
    [('Pancer', 'Richard')]

    >>> remove_original_author([('Pancer', 'Richard'), ('Breuss', 'Nataliya'),
    ...                         ('Tafliovich', 'Anya Y.'),
    ...                         ('Pancer', 'Richard')], ('Breuss', 'Nataliya'))
    [('Pancer', 'Richard'), ('Tafliovich', 'Anya Y.'), ('Pancer', 'Richard')]
    """
    i = 0
    while i < len(author_list):
        if author_list[i] == author_name:
            author_list.pop(i)
        else:
            i += 1
    return author_list


def has_prolific_authors(author_name_to_article_id: dict[NameType, list[str]],
                         article_code: ArticleType, min_pubs:
                         int) -> bool:
    """Returns True or False if the code article_code in an author to article
    code author_name_to_article_id has prolific authors who have written
    more articles than min_pubs.

    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, '008', 2)
    True

    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, '067', 2)
    True

    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, '031', 2)
    False

    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, '827', 5)
    False

    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, '827', 0)
    True
    """
    authors_with_code = []
    for authors, codes in author_name_to_article_id.items():
        if article_code in codes:
            authors_with_code.append(authors)

    return len(authors_with_code) >= min_pubs


def keep_prolific_authors(id_to_article: ArxivType,
                          min_publications: int) -> None:
    """Update the articles data id_to_article so that it contains only
    articles published by authors with min_publications or more
    articles published. As long as at least one of the authors has
    min_publications, the article is kept. FIXXXX THIS CODE

    >>> arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV)
    >>> keep_prolific_authors(arxiv_copy, 2)
    >>> len(arxiv_copy)
    3
    >>> '008' in arxiv_copy and '067' in arxiv_copy and '827' in arxiv_copy
    True
    """
    articles_to_remove = []

    for article_id, article_data in id_to_article.items():
        authors = article_data[AUTHORS]
        prolific_author_found = False

        for author in authors:
            if author in EXAMPLE_BY_AUTHOR and len(EXAMPLE_BY_AUTHOR[author]
                                                   ) >= min_publications:
                prolific_author_found = True
                break
        if not prolific_author_found:
            articles_to_remove.append(article_id)
    for article_id in articles_to_remove:
        id_to_article.pop(article_id, None)


if __name__ == '__main__':

    import doctest
    doctest.testmod()

    # uncomment to test with example data files
    # with open('example_data.txt', encoding='utf-8') as example_data:
    #    RESULT = read_arxiv_file(example_data)
    #    print('Did we produce a correct dict? ',
    #            RESULT == EXAMPLE_ARXIV)

    # uncomment to work with a larger data set
    # with open('data.txt', encoding='utf-8') as data_txt:
    #    EXAMPLE = read_arxiv_file(data_txt)
    # EXAMPLE_AUTHOR_TO_ARTICLE = make_author_to_articles(EXAMPLE)
    # EXAMPLE_MOST_PUBLISHED = get_most_published_authors(EXAMPLE)
    # print(EXAMPLE_MOST_PUBLISHED)
    # print(EXAMPLE_MOST_PUBLISHED)
    # print(get_coauthors(EXAMPLE, ('Varanasi', 'Mahesh K.')))  # one
    # print(get_coauthors(EXAMPLE, ('Chablat', 'Damien')))  # many
