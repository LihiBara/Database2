import os.path
from database import Database
import pickle
import win32file


class Filedb(Database):
    def __init__(self):
        """
        initializer
        """
        super().__init__()
        file_handle = win32file.CreateFileW("dbfile.txt", win32file.GENERIC_WRITE,
                                            win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE, None,
                                            win32file.OPEN_ALWAYS, 0)
        win32file.CloseHandle(file_handle)

    def dump(self):
        """
        writes the dictionary in the file
        """
        file_handle = win32file.CreateFileW("dbfile.txt", win32file.GENERIC_WRITE,
                                            win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE, None,
                                            win32file.OPEN_ALWAYS, 0)
        data = pickle.dumps(self.dict)
        return_value = win32file.WriteFile(file_handle, data)
        assert return_value[0] == 0
        win32file.CloseHandle(file_handle)

    def set_value(self, key, val):
        """
        set a new value in the dictionary file
        :param key: key of the dictionary
        :param val: the new value for the dictionary
        :return: True if value has been added, if not False
        """
        self.load()
        flag = super().set_value(key, val)
        self.dump()
        return flag

    def get_value(self, key):
        """
        gets the value from the dictionary file
        :param key: key of the dictionary
        :return: The value of the key from the dictionary file
        """
        self.load()
        return super().get_value(key)

    def load(self):
        """
        put the written in the file back into the dictionary
        """
        file_handle = win32file.CreateFileW("dbfile.txt", win32file.GENERIC_READ,
                                            win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE, None,
                                            win32file.OPEN_ALWAYS, 0)
        error, data = win32file.ReadFile(file_handle, os.path.getsize("dbfile.txt"))
        assert error == 0
        try:
            self.dict = pickle.loads(data)
        except EOFError:
            self.dict = {}
        win32file.CloseHandle(file_handle)

    def delete_value(self, key):
        """
        deletes the value of the key from the dictionary file
        :param key: key of the dictionary
        :return: the value that was deleted
        """
        self.load()
        val = super().delete_value(key)
        self.dump()
        return val
