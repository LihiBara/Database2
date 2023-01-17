"""
author: Lihi Baranetz
checks the synchronization while mode is processing
"""
from filedb import Filedb
from sync import Syncdb
from threading import Thread
import logging
import win32event
import win32process


def reader(database):
    """
    a reader try to get an access to read the value from the dictionary
    :param database: an object that one of his feature is a dictionary
    """
    logging.debug("reader started")
    for i in range(100):
        flag = database.get_value(i) == i or database.get_value(i) is None
        assert flag
    logging.debug("reader left")


def writer(database):
    """
    writer try to get an access to write the value from the dictionary
    :param database: an object that one of his feature is a dictionary
    """
    logging.debug("writer started")
    for i in range(100):
        assert database.set_value(i, i)
    for i in range(100):
        val = database.delete_value(i)
        flag = val == i or val is None
        assert flag
    logging.debug("writer left")


def main():
    """
    main function
    """
    logging.basicConfig(filename='log_thread.txt', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(threadName)s %(message)s')
    database = Syncdb(Filedb(), True)
    for i in range(400, 500):
        database.set_value(i, i)
    logging.debug("no competition")
    writer(database)
    reader(database)
    logging.debug("in competition")
    counter = 0
    for i in range(0, 10):
        thread = win32process.beginthreadex(None, 1000, reader, (database,), 0)[0]
        if win32event.WaitForSingleObject(thread, win32event.INFINITE) == 0:
            counter += 1
    for i in range(0, 50):
        thread = win32process.beginthreadex(None, 1000, writer, (database,), 0)[0]
        if win32event.WairForSingleObject(thread, win32event.INFINITE) == 0:
            counter += 1


if __name__ == "__main__":
    main()
