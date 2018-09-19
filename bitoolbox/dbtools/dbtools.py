# -*- coding: utf-8 -*-
"""Funcionalidades relacionadas ao banco de dados."""


import os
import configparser as cp
from pandas import DataFrame


def get_engine(database, schema=False, config_file=os.environ.get('bitoolbox_ini')):
    from sqlalchemy import create_engine
    # from sqlalchemy.pool import NullPool

    config = cp.ConfigParser()
    config.read(config_file)

    host = config.get(database, 'host')
    port = config.get(database, 'port')
    username = config.get(database, 'username')
    password = config.get(database, 'password')
    charset = config.get(database, 'charset')

    try:
        schema = schema or config.get(database, 'schema')
    except Exception:
        schema = ''

    engine = create_engine('mysql+pymysql://{username}:{password}@{host}:{port}'
                           '/{schema}?charset={charset}'.format(host=host,
                                                                port=port,
                                                                username=username,
                                                                password=password,
                                                                charset=charset,
                                                                schema=schema))
    return engine


def get_vertica_engine(database, schema=False, config_file=os.environ.get('bitoolbox_ini')):
    from sqlalchemy import create_engine
    # from sqlalchemy.pool import NullPool

    config = cp.ConfigParser()
    config.read(config_file)

    host = config.get(database, 'host')
    port = config.get(database, 'port')
    username = config.get(database, 'username')
    password = config.get(database, 'password')

    try:
        schema = schema or config.get(database, 'schema')
    except Exception:
        schema = ''

    engine = create_engine('vertica+vertica_python://{username}:{password}@{host}:{port}'
                           '/{schema}'.format(host=host,
                                                                port=port,
                                                                username=username,
                                                                password=password,
                                                                schema=schema))
    return engine




def get_gaia_engine(schema='temporario', database='GAIA'):
    return get_engine(database, schema=schema)


def get_devel_engine(schema='temporario', database='DEVEL'):
    return get_engine(database, schema=schema)

# Monkey patching pandas DataFrame.
def df_to_mysql(self, table_name,
                database,
                schema,
                if_exists='replace',
                config_file=os.environ.get('bitoolbox_ini'),
                indexes=[],
                dtype=None,
                chunksize=25000):
    import pandas as pd
    engine = get_engine(database, schema, config_file)
    self.to_sql(schema=schema,
                name=table_name,
                index_label=indexes,
                if_exists=if_exists,
                con=engine,
                index=False,
                chunksize=chunksize,
                dtype=dtype)
    engine.dispose()


def df_to_gaia(self, table_name,
               database='GAIA',
               schema='temporario',
               if_exists='replace',
               config_file=os.environ.get('bitoolbox_ini'),
               indexes=[],
               dtype=None,
               chunksize=25000):
    df_to_mysql(self, table_name,
                database,
                schema,
                if_exists,
                config_file,
                indexes,
                dtype,
                chunksize)


def df_to_devel(self, table_name,
                database='GAIA',
                schema='temporario',
                if_exists='replace',
                config_file=os.environ.get('bitoolbox_ini'),
                indexes=[],
                dtype=None,
                chunksize=25000):
    df_to_mysql(self, table_name,
                database,
                schema,
                if_exists,
                config_file,
                indexes,
                dtype,
                chunksize)


DataFrame.to_bidb = df_to_mysql
DataFrame.to_gaia = df_to_gaia
DataFrame.to_devel = df_to_devel
