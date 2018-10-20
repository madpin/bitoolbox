# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
import re

class Appointment(object):
    def __init__(self, appointment_date):

        self._url = 'https://dbei.gov.ie/en/What-We-Do/Workplace-and-Skills/Employment-Permits/Current-Application-Processing-Dates/'
        self._appointment_date = appointment_date
        self._soup_data = None
        self._cur_app_date_str = None
        self._cur_date_str = None
        self._cur_app_date = None
        self._cur_date = None
        self._date_diff = None
        self._predict_date = None


    @property
    def _soup(self):
        if(self._soup_data is not None):
            return self._soup_data
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}

        resp = requests.get(self._url, headers=headers, )

        if(not resp.ok):
            return None
        self._soup_data = BeautifulSoup(resp.content, 'html.parser')
        return self._soup_data


    @property
    def cur_app_date_str(self):
        if(self._cur_app_date_str is not None):
            return self._cur_app_date_str
        print('cur_app_date_str')

        tds = self._soup.find(
            'article', {'class': 'content-body__sections__main'}
        ).find('tbody').find_all('td')

        for key in range(len(tds)):
            if(tds[key].text == 'Trusted Partner'):
                date_key = key+1
                break
        self._cur_app_date_str = str(tds[date_key].text)
        return self._cur_app_date_str

    @property
    def cur_date_str(self):
        if(self._cur_date_str is not None):
            return self._cur_date_str
        print('cur_date_str')
        ps = self._soup.find_all('p')
        
        for key in range(len(ps)):
            _ret = re.search('As of(.*), ', ps[key].text)
            if(_ret):
                self._cur_date_str = _ret.group(1).strip()
                return self._cur_date_str
        return None
        

    @property
    def cur_app_date(self):
        if(self._cur_app_date is not None):
            return self._cur_app_date
        print('cur_app_date')
        self._cur_app_date = datetime.strptime(self.cur_app_date_str, '%d %B %Y')
        return self._cur_app_date

    @property
    def cur_date(self):
        if(self._cur_date is not None):
            return self._cur_date
        print('cur_date')
        self._cur_date = datetime.strptime(self.cur_date_str, '%d %B %Y')
        return self._cur_date


    @property
    def date_diff(self):
        if(self._date_diff is not None):
            return self._date_diff
        print('date_diff')
        self._date_diff = (self.cur_date - self.cur_app_date).days
        return self._date_diff

    @property
    def predict_date(self):
        if(self._predict_date is not None):
            return self._predict_date
        print('predict_date')
        self._predict_date = self._appointment_date + timedelta(days=self.date_diff)
        return self._predict_date