import threading
import multiprocessing
from filedb import Filedb
import logging
import win32event


class Syncdb:
    def __init__(self, database: Filedb, thread_or_process):
        """
        initializer
        :param database: dictionary
        :param thread_or_process: true/false for thread/process
        """
        if not isinstance(database, Filedb):
            raise ValueError("not filedb instance")
        self.database = database
        self.semaphore = win32event.CreateSemaphore(None, 10, 10, "semaphore")
        self.lock = win32event.CreateMutex(None, True, "lock")

    def get_value(self, key):
        """
        allows up to 10 readers to read at the same time
        :param key: key of the dictionary
        :return: the key's value
        """
        win32event.WaitForSingleObject(self.semaphore, win32event.INFINITE)
        logging.debug("reader in")
        value = self.database.get_value(key)
        win32event.ReleaseSemaphore(self.semaphore, 1)
        logging.debug("reader out")
        return value

    def set_value(self, key, val):
        """
        allows one writer to set a new value in the dictionary while nobody else allowed in.
        :param key: key of the dictionary
        :param val: the new value for the dictionary
        :return: True if value has been added, if not False
        """
        win32event.WaitForSingleObject(self.lock, win32event.INFINITE)
        for i in range(10):
            win32event.WaitForSingleObject(self.semaphore, win32event.INFINITE)
        logging.debug("writer in")
        flag = self.database.set_value(key, val)
        win32event.ReleaseSemaphore(self.semaphore, 10)
        logging.debug("writer out")
        win32event.ReleaseMutex(self.lock)
        return flag

    def delete_value(self, key):
        """
        allows one user to delete a value from the dictionary while nobody else allowed in.
        :param key: key of the dictionary
        :return: the deleted value
        """
        self.lock.acquire()
        for i in range(10):
            self.semaphore.acquire()
        flag = self.database.delete_value(key)
        for i in range(10):
            self.semaphore.release()
        self.lock.release()
        return flag
