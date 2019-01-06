import multiprocessing as mp
import threading


# https://stonesoupprogramming.com/2017/09/11/python-multiprocessing-producer-consumer-pattern/comment-page-1/
class DictionaryStorage:

    def __init__(self, writers):
        self.__writers = writers

        manager = mp.Manager()
        self.__queue = manager.Queue()

        self.__writer_thread = threading.Thread(name='__writer', target=self.__writer, args=())
        self.__writer_thread.start()

    # url - key : value = dict{ something }
    def add_dictionary(self, dictionary):
        self.__queue.put(dictionary)

    def __writer(self):

        # change while True on wait notify
        while True:
            dictionary = self.__queue.get()

            if isinstance(dictionary, bool):
                break

            jobs = []
            for writer in self.__writers:
                # writer.write(dictionary)
                job = threading.Thread(target=writer.write, args=(dictionary,))
                job.start()
                jobs.append(job)

            # TODO delete wait all jobs
            # wait all jobs
            for job in jobs:
                job.join()

    def is_finish(self):
        # TODO wait all writers
        self.__queue.put(False)
        self.__writer_thread.join()
        return True
