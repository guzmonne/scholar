import os
import unittest
import random
import string
from bs4 import BeautifulSoup

from scholar import (
    get_query_parameters,
    get_results, 
    get_data_from_result, 
    parse_int,
    get_data_from_results
)

FILENAME = "google_scholar_example_page.html"
DIR = os.path.dirname(os.path.realpath(__file__))
FILEPATH = os.path.join(DIR, FILENAME)

def random_string(string_length=10):
        """ Genera un string aleatorio de largo `string_length` """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(string_length))
     
class MainTest(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        """ Abre el HTML de prueba """
        with open(FILEPATH) as fp:
            cls.soup = BeautifulSoup(fp, 'html.parser')    
       
    def test_empty_query_parameters(self):
        """ 
        Debería devolver un objeto vacío sí la URL no contiene query
        parameters 
        """
        expected = {}
        actual = get_query_parameters('https://www.google.com')
        self.assertEqual(actual, expected)

    def test_query_parameters(self):
        """ Debería devolver un objeto con los query parameters de la URL """
        key1 = random_string()
        value1 = random_string()
        key2 = random_string()
        value2 = random_string()
        url = 'http://www.example.com/?' + key1 + '=' + value1 + '&' +  key2 + '=' + value2
        expected = {key1: value1, key2: value2}
        actual = get_query_parameters(url)
        self.assertEqual(actual, expected)

    def test_parse_int(self):
        """ Parsea un string con `int` y devuelve solo el `int` """
        expected = 375
        actual = parse_int('Citado por 375')
        self.assertEqual(actual, expected)

    def test_get_results(self):
        """ Obtiene los resultados de la página """
        expected = 20
        actual = len(get_results(self.soup))
        self.assertEqual(actual, expected)

    def test_get_data_from_results(self):
        """ 
        Convierte una lista de resultados en una lista de diccionarios
        validos 
        """
        expected = [{
            "title": "Containers and cloud: From lxc to docker to kubernetes",
            "citations": 375,
            "year": 2014,
            "link": 'https://ieeexplore.ieee.org/abstract/document/7036275/',
            "citations_url":
            'https://scholar.google.com/scholar?cites=2110749876942837248&as_sdt=2005&sciodt=1,5&hl=es',
            "id": '2110749876942837248'
        }, {
            "title": "Borg, omega, and kubernetes",
            "citations": 210,
            "year": 2016,
            "link": 'https://ai.google/research/pubs/pub44843.pdf',
            "citations_url":
            'https://scholar.google.com/scholar?cites=3003686304824470147&as_sdt=2005&sciodt=1,5&hl=es',
            "id": '3003686304824470147'
        }]
        results = get_results(self.soup)[0:2]
        actual = get_data_from_results(results)
        self.assertEqual(actual, expected)

    def test_get_data_from_result(self):
        """ Convierte un resultado en un diccionario valido """
        expected = {
            "title": "Containers and cloud: From lxc to docker to kubernetes",
            "citations": 375,
            "year": 2014,
            "link": 'https://ieeexplore.ieee.org/abstract/document/7036275/',
            "citations_url":
            'https://scholar.google.com/scholar?cites=2110749876942837248&as_sdt=2005&sciodt=1,5&hl=es',
            "id": '2110749876942837248'
        }
        result = get_results(self.soup)[0]
        actual = get_data_from_result(result)
        self.assertEqual(actual, expected)


