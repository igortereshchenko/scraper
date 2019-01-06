


class CommonHandler:

    @staticmethod
    def parse_articles_list(html=None, soup=None):
        return []

    @staticmethod
    # return hour, minute, seconds
    def parse_article_time(html=None, soup=None):
        return None, None, None

    @staticmethod
    def parse_article_subtitle(html=None, soup=None):
        return None

    @staticmethod
    # return html, cleaned html
    def parse_article_text(html=None, soup=None):
        return None, None
