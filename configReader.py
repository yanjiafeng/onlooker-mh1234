import json


class ConfigReader:

    __configFilePath= "config.json"
    __currIdx = 0
    __config = {}

    def __init__(self):
        with open(self.__configFilePath, 'r') as load_f:
            self.__config = json.load(load_f)


    def readConfig(self):

        for c in self.__config:
            print(c)

        print('input 2')
        inputId = input('请输入序号后回车')

        for index in range(len(self.__config)):
            if str(self.__config[index]['id']) == str(inputId):
                self.__currIdx = index
                break

    def saveConfig(self):
        with open(self.__configFilePath, "w") as f:
            json.dump(self.__config, f)
        print("加载入文件完成...")

    def getConfig(self):
        return self.__config[self.__currIdx]

    def getUrl(self):
        return self.getConfig()['url']

    def getEpisode(self):
        return self.getConfig()['episode']

    def getPage(self):
        return self.getConfig()['page']

    def setEpisode(self,idx):
        self.__config[self.__currIdx]['episode'] = idx

    def setPage(self,idx):
        self.__config[self.__currIdx]['page'] = idx



