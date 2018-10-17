# -*- coding: utf-8 -*-
"""Funcionalidades relacionadas com Omniture."""
import os
import configparser as cp

def get_token(config_file=os.environ.get('bitoolbox_ini')):
    import requests
    import json
    requests.packages.urllib3.disable_warnings()

    config = cp.ConfigParser()
    config.read(config_file)
    
    user = config.get('API_Omniture', 'user')
    password = config.get('API_Omniture', 'pass')
    auth_url = config.get('API_Omniture', 'auth_url')

    acess_app_adobe = {
        'grant_type': 'client_credentials',
        'Authorization': 'Bearer',
        'client_id': user,
        'client_secret': password,
    }

    # Chamada para Capturar o Token de validação
    fim = requests.post(auth_url, verify=False,
                        stream=True, data=acess_app_adobe)

    body = json.loads(fim.text)
    token = False
    try:
        token = body['access_token']
    except:
        pass
    return token


def get_header(acess_token=None):
    if(acess_token is None):
        acess_token = get_token()
    bearer = 'Bearer {acess_token}'
    header = {'Authorization': bearer.format(acess_token=acess_token)}

    return header


def get_default_report_params():
    params = {'method': 'Report.Queue'}
    return params


def get_report_request(report_request_data, omniture_header=None, acess_token=None,
                       config_file=os.environ.get('bitoolbox_ini')):
    import json
    import requests
    requests.packages.urllib3.disable_warnings()

    config = cp.ConfigParser()
    config.read(config_file)
    
    data_url = config.get('API_Omniture', 'data_url')

    if(omniture_header is None):
        omniture_header = get_header(acess_token)

    request = requests.post(
        data_url,
        headers=omniture_header,
        verify=False,
        data=json.dumps(report_request_data),
        params=get_default_report_params(),
    )

    return request


def get_report_id(report_request_data, omniture_header=None, acess_token=None):
    import json
    req = get_report_request(report_request_data, omniture_header, acess_token)
    ret = False
    try:
        ret = req.json()['reportID']
    except Exception:
        try:
            ret = req.json()["error"]
        except Exception:
            raise
    return ret


def get_report(report_id, page=1, omniture_header=None, acess_token=None,
               config_file=os.environ.get('bitoolbox_ini')):
    import json
    import requests
    requests.packages.urllib3.disable_warnings()

    config = cp.ConfigParser()
    config.read(config_file)
    
    data_url = config.get('API_Omniture', 'data_url')

    if(omniture_header is None):
        omniture_header = get_header(acess_token)

    params = {'method': 'Report.Get'}
    data = {
        'reportID': str(
            report_id
        ),
        'page': page,
        'format': "csv"
    }

    result = requests.post(
        data_url,
        headers=omniture_header,
        verify=False,
        data=json.dumps(data),
        params=params
    )

    return result
