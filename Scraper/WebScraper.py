import time as t
import requests


class WebScraperException(Exception):
    def __init__(self, message, url):
        super(Exception, self).__init__(message)
        self.url = url


class WebScraper:

    def __init__(self, url, tries=4, timeout=30, sleep=10):
        self.__url = url
        self.__tries = tries
        self.__timeout = timeout
        self.__sleep = sleep

    def scrape_page(self):
        html = None
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        for i in range(1, self.__tries + 1):
            try:
                result = requests.get(self.__url, headers=headers, timeout=self.__timeout)
                html = result.text

                # Success
                if html:
                    break

            except Exception as e:
                # print("Got error: {0}\nwhen requesting URL {1} with {2} tries".format(str(e), self.__url, i))
                if i == self.__tries:
                    # print("Failed requesting from URL {0} ==> {1}".format(self.__url, e))
                    raise WebScraperException(str(e), self.__url)
                else:
                    # wait each time longer
                    t.sleep(self.__sleep * (i - 1))

        return html
