# -*- coding: utf-8 -*-
"""Birst Tools"""

import os
import configparser as cp


spaces = {
    'space_one': '1b3f1f17-cd12-41b5-b490-33b530986b32',
    'space_two': '128aa613-6b29-6746-a6e8-a66d77c88478',
}

def get_client(config_file=os.environ.get('bitoolbox_ini')):
    from zeep import Client
    from requests import Session
    from zeep.transports import Transport
    
    config = cp.ConfigParser()
    config.read(config_file)

    api_url = config.get('API_Birst', 'host')

    session = Session()
    session.verify = False

    transport = Transport(session=session)

    client = Client(
        api_url,
        transport=transport
    )

    return client


def get_token(client=None, config_file=os.environ.get('bitoolbox_ini')):

    config = cp.ConfigParser()
    config.read(config_file)

    username = config.get('API_Birst', 'username')
    password = config.get('API_Birst', 'password')

    if(client is None):
        client = get_client(config_file)

    token = client.service.Login(username, password)

    return token


def birst_query_to_df(resp):
    import pandas as pd

    df = pd.DataFrame()

    for line in range(len(resp.rows.ArrayOfString)):
        df = df.append(
            pd.DataFrame.from_records([
                resp.rows.ArrayOfString[line].string
            ])
        )
    df.columns = resp.columnNames.string
    return df.reset_index(drop=True)


def query_birst_raw(query, space_id, token=None, client=None):
    if(client is None):
        client = get_client()

    if(token is None):
        token = get_token(client)

    response = client.service[
        'executeQueryInSpace'
        ](token,query.lstrip('\n').lstrip(' '), space_id)
    
    return response


def query_birst(query, space_id, token=None, client=None):
    response = query_birst_raw(query, space_id, token, client)
    if(response.errorCode is None):
        return birst_query_to_df(response)
    else:
        raise RuntimeError(response.errorCode, response.errorMessage)

def get_space_id(name):
    return spaces[name]


def get_load_status(space_id, token=None, client=None):
    if(client is None):
        client = get_client()

    if(token is None):
        token = get_token(client)

    response = client.service[
        'getLoadStatus'
        ](token, space_id)
    
    return response


def is_space_avaliable(space_id, token=None, client=None):
    status = get_load_status(space_id, token, client)
    if(status == 'Available'):
        return True
    else:
        return False