import requests as req
import os, base64
import requests as req
from PIL import Image
from io import BytesIO
import psutil as psutil

import configReader


class Episode:
    __chapterImages = []
    __chapterPath = ''
    __list = []
    __currPageIdx = 0
    __currEpIdx = 0
    __url = ''

    __cr = configReader.ConfigReader()

    def __init__(self):

        self.__cr.readConfig()

        self.__getEpisodeList(self.__cr.getUrl())
        self.__url = self.__getEpisode(self.__cr.getEpisode())
        self.__currPageIdx = self.__cr.getPage()
        self.__currEpIdx = self.__cr.getEpisode()

        self.getCurrPage()

    def __getEpisode(self, idx):
        return 'https://www.mh1234.com' + self.__list.__getitem__(idx)

    def __getEpisodeList(self, url):
        r1 = req.get(url)
        html = r1.content
        data = html.decode('utf-8')  # This will return entire content.
        # print(data)

        idxStart = data.find('chapter-list-1')
        # print(idxStart)
        idxEnd = data[idxStart:].find('</ul>')
        # print(idxEnd)
        chapterHtml = data[idxStart:idxStart + idxEnd] \
            .replace('chapter-list-1" data-sort="asc">', '') \
            .replace('<li class="">', '') \
            .replace('<li class="new">', '') \
            .replace('<i></i>', '') \
            .replace('</li>', '') \
            .replace('                            ', '') \
            .replace('    ', '') \
            .replace('    ', '').replace('<a  href=', '').replace('"', '') \
            .replace('\r', '') \
            .replace('\n', '')

        chapterList = chapterHtml.split('</a>')

        i = 0;
        for cp in chapterList:
            print(str(i) + ' --- ' + cp)
            i = i + 1

            cpTmp = cp[:cp.find('>')]
            self.__list.append(cpTmp)

    def getCurrPage(self):
        r1 = req.get(self.__url)
        html = r1.content
        data = html.decode('utf-8')  # This will return entire content.
        self.__chapterImages = self.__getChapterImages(data)
        print(self.__chapterImages)
        self.__chapterPath = self.__getChapterPath(data)
        url = 'https://img.wszwhg.net/' + self.__chapterPath + self.__chapterImages[self.__currPageIdx]
        self.__showImage(url)

    def __getChapterPath(self, data):
        idxStart = data.find('chapterPath = ')
        idxEnd = data[idxStart:].find(';')
        chapterPath = data[idxStart:idxStart + idxEnd].replace('chapterPath = ', '').replace('"', '')
        return chapterPath

    def __getChapterImages(self, data):
        idxStart = data.find('chapterImages = ')
        idxEnd = data[idxStart:].find(';')
        chapterImages = data[idxStart:idxStart + idxEnd].replace('chapterImages = ', '')
        images = chapterImages.replace('"', '').replace('[', '').replace(']', '').replace('\\/','/').split(',')
        return images

    def __showImage(self, url):
        response = req.get(url)

        # # 内存中打开图片
        # image = Image.open(BytesIO(response.content))

        # 图片的base64编码
        ls_f = base64.b64encode(BytesIO(response.content).read())

        # base64编码解码
        imgdata = base64.b64decode(ls_f)

        # 图片文件保存
        file = open('test.jpg', 'wb')
        file.write(imgdata)
        file.close()

        scale = 1
        img = Image.open('test.jpg')
        width = int(img.size[0] * scale)
        height = int(img.size[1] * scale)
        img = img.resize((width, height), Image.ANTIALIAS)
        img.show()  # 显示图片

    def closePage(self):
        for proc in psutil.process_iter():  # 遍历当前process
            if proc.name() == "display":  # 如果process的name是display
                proc.kill()

    def getNextPage(self):
        self.__currPageIdx = self.__currPageIdx + 1

        if self.__currPageIdx >= len(self.__chapterImages):
            self.__currEpIdx = self.__currEpIdx + 1
            self.__currPageIdx = 0
            self.__url = self.__getEpisode(self.__currEpIdx)
            self.getCurrPage()

            self.__cr.setEpisode(self.__currEpIdx)
            self.__cr.setPage(self.__currPageIdx)
        else:
            url = 'https://img.wszwhg.net/' + self.__chapterPath + self.__chapterImages[self.__currPageIdx]
            self.__showImage(url)

            self.__cr.setPage(self.__currPageIdx)

        self.__cr.saveConfig()

