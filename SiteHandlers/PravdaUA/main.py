from Scraper.MultiThreadNewsListScraper import MultiThreadNewsListScraper

from Scraper.WebScraper import WebScraper
from Scraper.DictionaryStorage import DictionaryStorage
from bs4 import BeautifulSoup
from threading import Thread

import time as Timer

from Scraper.Writters.ElasticSearchWriter import ElasticSearchWriter
from Scraper.Writters.FileWritter import FileWriter
from SiteHandlers.PravdaUA.PravdaUAHandler import PravdaUAHandler

error_urls= dict()

def month_string_to_number(string):
    month = {
        'січень': 1,
        'лютий': 2,
        'березень': 3,
        'квітень':4,
         'травень':5,
         'червень':6,
         'липень':7,
         'серпень':8,
         'вересень':9,
         'жовтень':10,
         'листопад':11,
         'грудень':12
        }

    s = string.strip().lower()

    try:
        return month[s]
    except:
        raise ValueError('Not a month')

def worker(fwd,data):
    parser = PravdaUAHandler()
    scraper = MultiThreadNewsListScraper(data['url'], year = data['year'], month=data['month'], day=data['day'], parser=parser)
    dataset, errors = scraper.run_scraper()

    error_urls.update(errors)

    print("Finish scraped year {0} month {1} day {2}".format(data['year'], data['month'], data['day']))
    fwd.add_dictionary(dataset)


def parseYear(year, outputfile):
    start = Timer.time()

    scraper = WebScraper("https://www.pravda.com.ua/archives/year_{0}/".format(year))
    page = scraper.scrape_page()

    soup = BeautifulSoup(page, 'html.parser')

    calendars = soup.find_all('div', {'class': ['ui-datepicker-group']})

    # fdw = DictionaryStorage([ FileWriter(outputfile), ElasticSearchWriter(doc_type='pravdaua')])
    fdw = DictionaryStorage([FileWriter(outputfile)])

    jobs = []
    jobs_package = []
    max_parallel_jobs = 100

    for calendar in calendars:
        month = calendar.find_all('div', {'class': ['ui-datepicker-header']})[0].text.strip()

        month = month_string_to_number(month.split()[0])

        days_urls = calendar.find_all('a', {'class': ['ui-state-default']})


        for url in days_urls:
            day = url.text.strip()
            data = {"url":'https://www.pravda.com.ua'+url.get('href') ,"year":year, "month": month, "day": int(day)}

            job = Thread(target=worker, args=(fdw, data,))
            jobs.append(job)
            jobs_package.append(job)
            job.start()
            # test one day
            # break

        # wait by max_parallel_jobs
        if len(jobs_package) > max_parallel_jobs:
            for job in jobs_package:
                job.join()

            jobs_package.clear()

    # wait all jobs
    for job in jobs:
        job.join()
    fdw.is_finish()
    print("Year {0} writing ended in {1} seconds".format(year,Timer.time()-start))


if __name__ == '__main__':
    start = Timer.time()
    for year in range(2019, 2020):
        parseYear(year, "../../data/{0}.csv".format(year))


    print("All done in {0} seconds".format(Timer.time()-start))

    if error_urls:
        file = open("../../data/error.txt", mode='w', encoding="utf-8")
        for url in error_urls:
            file.write("{0}, {1}\n".format(url,error_urls[url]))

        file.flush()
        file.close()







