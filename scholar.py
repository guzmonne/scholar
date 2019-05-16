from urllib.parse import urlparse, parse_qs
import requests
from bs4 import BeautifulSoup

GOOGLE_SCHOLAR_URL = 'https://scholar.google.com'
URL = "https://scholar.google.com/scholar?q=kubernetes&hl=es&as_sdt=1%2C5&as_ylo=2019&as_yhi=2009"

def get_query_parameters(url):
    """
    Devuelve los `query_parameters` como un objeto
    @param {str} url URL a parsear
    @return {QueryParameters}
    >>> get_query_parameters('https://www.google.com')
    {}
    >>> get_query_parameters('https://scholar.google.com/scholar?q=kubernetes')
    {"q": "kubernetes"}
    """
    parsed = parse_qs(urlparse(url).query)
    return {key: value[0] for key, value in parsed.items()}

def parse_int(string):
    """
    Obtiene un entero del string.
    @param {str} string String a parsear
    @return {int} número parseado
    >>> parse_int("Citado por 375")
    375
    """
    int_as_str = ''.join(x for x in string if x.isdigit())
    return int(int_as_str)

def get_results(soup):
    """
    Gets the results div from the HTML soup
    @param {BeautifulSoup} soup Google Scholar BeautifulSoup instance
    @return {BeautifulSoup[]} List of Google Scholar results as
    BeautifulSoup instances
    """
    return soup.find_all('div', class_='gs_r gs_or gs_scl')

def get_data_from_results(soups):
    """
    Takes a list of BeautifulSoup instances representing a Goggle Scholar
    result `div` and returns a list of results dictionaries.
    @param {BeautifulSoup[]} soups Google Scholar BeautifulSoup instance list
    @return {Result[]} List of Google Scholar dictionary results
    """
    return [get_data_from_result(soup) for soup in soups]

def get_data_from_result(soup):
    """
    Takes a BeautifulSoup instance of a Google Scholar result and 
    transforms it into a dictionary with its details keys
    """
    title = soup.select('h3 > a', href = True)[0]
    year = soup.select('.gs_a', href = True)[0]
    citations = soup.select('.gs_fl > a', href = True)[2]
    citations_url = GOOGLE_SCHOLAR_URL + citations['href']

    return {
        "id": get_query_parameters(citations_url).get('cites'),
        "title": title.getText(),
        "link": title['href'],
        "year": parse_int(year.getText()),
        "citations": parse_int(citations.getText()),
        "citations_url": citations_url
    } 

if __name__ == '__main__':
    response = requests.get(URL, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")
    
    results = soup.find_all('div', class_='gs_r gs_or gs_scl')
    
    for result in results:
        title = result.select('h3 > a')
        if len(title) > 0:
            print(title[0].getText()) 
