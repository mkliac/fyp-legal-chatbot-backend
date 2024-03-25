# coding: utf-8

import requests

class Downloader:
    def __init__(self):
        # self.headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        pass

    def download(self, url):
        ''' Download the content from the given url.
        Return the corresponding content
        '''
        if url is None:
            return None

        try:
            response = requests.get(url)
        except:
            return None
            
        if response.status_code != 200:
            return None

        return response