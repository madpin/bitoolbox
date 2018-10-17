# -*- coding: utf-8 -*-
"""Funcionalidades relacionadas com TrackSale."""
import os
import configparser as cp
import requests
import json
from datetime import date
requests.packages.urllib3.disable_warnings()

def get_url(config_file=os.environ.get('bitoolbox_ini')):
    config = cp.ConfigParser()
    config.read(config_file)
    url = config.get('API_TrackSales', 'url')
    return url


def get_token(config_file=os.environ.get('bitoolbox_ini')):


    config = cp.ConfigParser()
    config.read(config_file)

    user = config.get('API_TrackSales', 'user')
    password = config.get('API_TrackSales', 'pass')
    url = config.get('API_TrackSales', 'url')

    try:
        token = config.get('API_TrackSales', 'token')
        return token
    except:
        pass
    
    headers_login = {
        "content-type": "application/json",
        "cache-control": "no-cache",
    }

    data_login = {
        "email": user,
        "password": password
    }

    response = requests.post(
        url+'login',
        data=json.dumps(data_login),
        headers=headers_login,
        verify=False)
    
    token = None
    if(response.status_code == requests.codes.ok):
        response.json()['token']
    else:
        response.raise_for_status()
    
    return token


def get_header(acess_token=None, config_file=os.environ.get('bitoolbox_ini')):
    if(acess_token is None):
        acess_token = get_token(config_file)

    header = {
        "content-type": "application/json",
        "authorization": "Bearer " + acess_token,
        "cache-control": "no-cache",
    }

    return header


def get_answers(date_from=date.today(), date_to=date.today(), limit=-1, config_file=os.environ.get('bitoolbox_ini')):

    if(isinstance(date_from, str)):
        date_from_str = date_from
    elif(isinstance(date_from, date)):
        date_from_str = date_from.strftime('%Y-%m-%d')

    if(isinstance(date_to, str)):
        date_to_str = date_to
    elif(isinstance(date_to, date)):
        date_to_str = date_to.strftime('%Y-%m-%d')

    config = cp.ConfigParser()
    config.read(config_file)

    url = config.get('API_TrackSales', 'url')

    get_data = {
        'tags': 'true',
        'limit': str(limit),
        'start': date_from_str,
        'end': date_to_str,
    }

    header = get_header()

    response = requests.get(url+'report/answer', params=get_data, headers=header, verify=False)

    return response.json()
    