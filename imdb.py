"""Script to gather IMDB keywords from 2013's top grossing movies"""
import sys
import csv
import requests
from bs4 import BeautifulSoup

URL = "http://www.imdb.com/search/title?at=0&sort=boxoffice_gross_us,desc&start=1&year=2013,2013"

def main():
    """Main enrey point for the script"""
    movies = get_top_grossing_movie_links(URL)
    print movies[0]
    sys.exit()
    with open('output.csv', 'w') as output:
        csvwriter = csv.writer(output)
        for title, url in movies:
            keywords = get_keywords_for_movie('http://www.imdb.com{}keywords'.format(url))
            csvwriter.writerow([title, keywords])

def get_top_grossing_movie_links(url):
    """Return a list of tuples containing the top grossing movies of 2013 and link to their IMDB page."""
    response = requests.get(url)
    movie_list = []
    for each_url in BeautifulSoup(response.text).select('.title a[href*="title"]'):
        movie_title = each_url.text
        if movie_title != 'X':
            movie_list.append((movie_title, each_url['href']))
    return movie_list

def get_keywords_for_movie(url):
    """Return a list of keywords associated with *movie*."""
    keywords = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    tables = soup.find_all('table', class_='dataTable')
    table = tables[0]
    return [td.text for tr in table.find_all('tr') for td in tr.find_all('td')]


if __name__ == "__main__":
    sys.exit(main())