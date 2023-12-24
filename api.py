"""
File that contains a class to make calls to the WikiMedia API, found here: https://www.mediawiki.org/wiki/MediaWiki
"""
from __future__ import annotations
import requests


class WikiMediaAPI:
    """
    Obtain the properties of a Wikipedia article
    """
    _URL = 'http://en.wikipedia.org/w/api.php'
    _PARAMS = {
        "action": "query",
        "format": "json",
        "titles": "",
        "prop": "",
        "cllimit": "max",
        "rvprop": "size",
        "rvlimit": "1",
        "pllimit": "max"
    }
    _S = requests.Session()

    @classmethod
    def get_article_properties(cls, article: str) -> dict | None:
        """
        Get the properties of a given article
        """
        r = cls._S.get(url=cls._URL, params=cls.property_query_params(article))
        if not r:
            print(r.status_code)
            print('Please ensure the article title is correct')
            return None
        data = r.json()

        properties = {
            'name': article,
            'hyperlinks': set(),
            'categories': set(),
            'size': 0
        }

        for k, v in data['query']['pages'].items():
            if 'links' in v:
                for i in v['links']:
                    properties['hyperlinks'].add(i['title'])
            if 'categories' in v:
                for i in v['categories']:
                    properties['categories'].add(i['title'])
            if 'length' in v:
                properties['size'] = int(v['length'])
            if 'revisions' in v:
                properties['size'] = v['revisions'][0]['size']

        return properties

    @classmethod
    def property_query_params(cls, title: str) -> dict:
        """
        Generate params to make a request
        """
        formatted = title.strip().replace(' ', '_')
        temp_params = cls._PARAMS.copy()
        temp_params["titles"] = formatted
        temp_params["prop"] = 'links|categories|revisions'
        return temp_params
