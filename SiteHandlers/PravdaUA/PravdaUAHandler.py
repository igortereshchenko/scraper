import re
from bs4 import BeautifulSoup


class PravdaUAHandler:

    @staticmethod
    def parse_articles_list(html=None, soup=None):

        if soup is None:
            soup = BeautifulSoup(html, 'html.parser')

        div_news = soup.find_all('div', {'class': ['news_all']})

        if not div_news:
            return None

        return div_news[0].find_all('div', {'class': ['article']})

    @staticmethod
    def parse_article_time(html=None, soup=None):

        if soup is None:
            soup = BeautifulSoup(html, 'html.parser')

        time = soup.find_all('div', {'class': ['article__time']})

        if time:

            hours, minutes = re.findall(r'\d+', time[0].text)
            seconds = None
            return int(hours), int(minutes), seconds

        else:
            return None, None, None

    @staticmethod
    def parse_article_subtitle(html=None, soup=None):

        if soup is None:
            soup = BeautifulSoup(html, 'html.parser')

        subtitle = soup.find_all('div', {'class': ['article__subtitle']})

        if subtitle:
            return subtitle[0].text.strip()
        else:
            return None

    @staticmethod
    def parse_article_text(html=None, soup=None):

        if soup is None:
            soup = BeautifulSoup(html, 'html.parser')

        text = soup.find_all('div', {'class': ['post_news__text', 'post__text']})  # post__text for epravda

        if text:

            html_text = text[0].prettify()
            cleaned_text = text[0]
            [x.extract() for x in cleaned_text.findAll('script')]

            return html_text, cleaned_text.text.strip()
        else:
            return None, None
