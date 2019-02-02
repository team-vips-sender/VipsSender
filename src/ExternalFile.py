import configparser
from Defines import STANDARD_RETURN


class ExternalFile:
    def __init__(self, file_path):
        self.__kind = 'data'
        self.__file_path = file_path

        self.config = configparser.ConfigParser()
        self.config.read(file_path)

        if not self.__kind in self.config:
            self.config[self.__kind] = {}
            with open(file_path, 'w') as configfile:
                self.config.write(configfile)

    def save(self, key, data):
        self.config[self.__kind][key] = data
        with open(self.__file_path, 'w') as configfile:
            self.config.write(configfile)

    def get(self, key):
        ret = STANDARD_RETURN.NOT_OK
        data = ''
        
        if key in self.config[self.__kind]:
            data = self.config[self.__kind][key]
            ret = STANDARD_RETURN.OK

        return ret, data
