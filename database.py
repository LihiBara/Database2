class Database:
    def __init__(self):
        """
        initializer
        """
        self.dict = {}

    def set_value(self, key, val):
        """
        sets a new value in the dictionary
        :param key: key of the dictionary
        :param val: the new value for the dictionary
        :return: success if value has been added, if not failure
        """
        self.dict[key] = val
        if key in self.dict.keys():
            return "success"
        else:
            return "failure"

    def get_value(self, key):
        """
        returns the value in the dictionary
        :param key: key of the dictionary
        :return: The value of the key from the dictionary file
        """
        if key in self.dict.keys():
            return self.dict[key]
        else:
            return None

    def delete_value(self, key):
        """
        deletes the value of the key
        :param key: key of the dictionary
        :return: the value that was deleted
        """
        if key in self.dict.keys():
            value = self.get_value(key)
            del self.dict[key]
            return value
