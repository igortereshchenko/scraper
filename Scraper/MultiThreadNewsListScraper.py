import functools
from Scraper.WebScraper import WebScraper, WebScraperException
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
from multiprocessing import cpu_count
from datetime import datetime


# http://edmundmartin.com/multi-threaded-crawler-in-python/
# http://blog.adnansiddiqi.me/how-to-speed-up-your-python-web-scraper-by-using-multiprocessing/
# https://medium.com/python-pandemonium/6-things-to-develop-an-efficient-web-scraper-in-python-1dffa688793c

class MultiThreadNewsListScraper:

    def __init__(self, base_url, year=None, month=None, day=None, max_workers=None, parser=None, tries=3, timeout=30,
                 sleep=10):

        self.base_url = base_url

        self.__year = year
        self.__month = month
        self.__day = day

        self.__is_no_articles = False
        self.__parser = parser
        self.__tries = tries
        self.__timeout = timeout
        self.__sleep = sleep

        self.root_url = '{}://{}'.format(urlparse(self.base_url).scheme, urlparse(self.base_url).netloc)

        if max_workers is None:
            max_workers = cpu_count()
        self.__pool = ThreadPoolExecutor(max_workers=max_workers)

        self.scraped_pages = dict()
        self.error_pages = dict()
        self.to_crawl = []

        self.parse_links(self.scrape_page(base_url))

    def parse_links(self, html):

        articles_list = self.__parser.parse_articles_list(html=html)

        for article in articles_list:

            url = article.find_all('a')
            if not url:
                continue

            if 'http' not in url[0].get('href'):
                article_url = urljoin(self.root_url, url[0].get('href'))
            else:
                article_url = url[0].get('href')

            title = url[0].text
            subtitle = self.__parser.parse_article_subtitle(soup=article)
            hours, minutes, seconds = self.__parser.parse_article_time(soup=article)

            date = datetime(year=self.__year, month=self.__month, day=self.__day)
            if hours:
                date = date.replace(hour=hours)
            if minutes:
                date = date.replace(minute=minutes)
            if seconds:
                date = date.replace(second=seconds)

            self.to_crawl.append(article_url)
            self.scraped_pages[article_url] = {
                "url": article_url,
                "date": date,
                "title": title,
                "subtitle": subtitle,
                "html": None,
                "text": None
            }
        # Empty articles_list
        if article is None:
            self.error_pages[article_url] = "no article(s) found"
            self.__is_no_articles = True

    # callback
    def post_scrape_callback(self, response, target_url=None):
        html = response.result()

        if html is None:
            self.error_pages[target_url] = "nothing to scrape"
            return

        html, text = self.__parser.parse_article_text(html=html)

        if text:
            self.scraped_pages[target_url]["text"] = text
            self.scraped_pages[target_url]["html"] = html
        else:
            self.error_pages[target_url] = "no article text scrapped"

    def scrape_page(self, url):

        scraper = WebScraper(url, tries=self.__tries, timeout=self.__timeout, sleep=self.__sleep)
        try:
            result = scraper.scrape_page()

            print("Scrapped {0}".format(url))
            return result
        except WebScraperException as e:
            self.error_pages[e.url] = str(e)
            return None

    def run_scraper(self):

        if not self.__is_no_articles:
            with self.__pool as executor:
                for target_url in self.to_crawl:
                    job = executor.submit(self.scrape_page, target_url)
                    job.add_done_callback(functools.partial(self.post_scrape_callback, target_url=target_url))

        return self.scraped_pages, self.error_pages


# from Scraper.SiteHandlers.PravdaUAHandler import PravdaUAHandler
# if __name__ == '__main__':
#
#     parser = PravdaUAHandler()
#
#     s = MultiThreadNewsListScraper("https://www.pravda.com.ua/news/date_02012019/", year=2019, month=1, day=2, parser=parser )
#     result, errors = s.run_scraper()
#     print(result)