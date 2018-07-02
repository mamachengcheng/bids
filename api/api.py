# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import xlwt


class Bids(object):

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    def __init__(self, keyword=''):
        """
        :param keyword: 关键字
        """
        self.keyword = self._get_keyword(keyword)
        self.page_num = 1
        self.table = []

    def request(self, url):
        """
        请求数据 , 放入table
        :return 放回是否为最后一页
        """
        html = requests.get(url=url, headers=self.headers).content
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        items = soup.find_all('tr')
        for i, item in enumerate(items):
            if i == 0:
                continue

            values = item.find_all('td')
            state = values[0].text
            title = values[1].text.replace('\n', '')
            place = values[2].text
            date = values[3].text

            self.table.append((state, title, place, date))

        page_num = soup.find('div', class_='megas512').contents[-4].text

        if page_num == repr(self.page_num):
            # 已到最后一页
            return False
        else:
            # 未到最后一页
            return True

    def save(self):
        """
        保存数据至table
        """
        wb = xlwt.Workbook()
        sheet = wb.add_sheet('数据')

        url = self._get_url(self.keyword, self.page_num)
        print('第{}页'.format(self.page_num))
        while self.request(url):
            # 翻到下一页
            self.page_num += 1
            print('第{}页'.format(self.page_num))
            url = self._get_url(self.keyword, self.page_num)

        for i, col in enumerate(self.table):
            for j, row in enumerate(col):
                sheet.write(i, j, row)

        wb.save('data.xls')

    @ staticmethod
    def _get_keyword(keyword):
        """
        处理关键字为url编码方式
        :param keyword: 关键字
        :return: 处理后关键字
        """
        keyword = keyword.encode('gbk')
        keyword = quote(keyword, 'gbk')
        return keyword

    @ staticmethod
    def _get_url(keyword, page_num):
        """
        处理url
        :return: 返回处理后的url
        """
        return 'http://www.qianlima.com/new/keywordzhuolu_new4.jsp?q={}&p={}'.format(keyword, page_num)


if __name__ == '__main__':
    bids = Bids(keyword='工厂')
    bids.save()
