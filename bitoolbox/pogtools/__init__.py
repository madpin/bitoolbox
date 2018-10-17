# -*- coding: utf-8 -*-
"""This module do what others does not dare to do."""


def mysql_column_escape(str):
    """Retorna uma str sem caracteres especiais"""
    from unidecode import unidecode
    return unidecode(
        str
        .replace(' / ', '_')
        .replace('. ', '_')
        .replace(' ', '_')
        .replace('-', '_')
        .replace('/', '_')
        .replace('\\', '_')
        .replace('.', '_')
        .replace(')', '')
        .replace('(', '')
        .lower()
    )


def str_to_md5(tbhstring):
    """Converte uma str para md5"""
    import hashlib
    hashid = hashlib.md5(tbhstring.encode('utf-8')).hexdigest()
    return hashid


def get_query(filename, folder=None):
    import os
    full_filename = filename + '.sql'
    if(folder is None):
        full_path = os.path.join('.', 'queries', full_filename)
    else:
        full_path = os.path.join('.', 'queries', folder, full_filename)

    with open(full_path, encoding='utf-8') as query_file:
        query = query_file.read()
    return query


def delete_insert_simple(conn,
                         stg_table_name,
                         raw_table_name,
                         unique_field,
                         fields_dict,
                         time_process_start=None,
                         schema_name='temporario',
                         trans=None,
                         logger=None):
    from timeit import default_timer

    had_transaction = True
    if(trans == None):
        had_transaction = False

    if time_process_start is None:
        time_process_start = default_timer()

    if(had_transaction is False):
        trans = conn.begin()

    deleted_records = None
    inserted_records = None
    try:
        # first query.  a Connection is acquired
        # from the Engine, and a Transaction
        # started.

        q1 = conn.execute("""
          DELETE `{schema_name}`.`{raw_table_name}` 
          FROM `{schema_name}`.`{raw_table_name}` 
            INNER JOIN `{schema_name}`.`{stg_table_name}` 
              ON `{schema_name}`.`{raw_table_name}`.`{unique_field}` = `{schema_name}`.`{stg_table_name}`.`{unique_field}`
          """.format(
            fields='`' + '`,\n`'.join(fields_dict) + '`',
            stg_table_name=stg_table_name,
            raw_table_name=raw_table_name,
            schema_name=schema_name,
            unique_field=unique_field
        )
        )

        if(logger is not None):
            logger.info(
                str(q1.rowcount) + ' records deleted from RAW completed. '
                'in {timedelta} seconds.'
                .format(timedelta=str(round(default_timer() - time_process_start, 2)))
            )
        deleted_records = q1.rowcount

        q2 = conn.execute("""
          INSERT INTO
              `{schema_name}`.`{raw_table_name}`
              (
                  {fields}
              )
          select
              {fields}
          from
              `{schema_name}`.`{stg_table_name}`
          """.format(
            fields='`' + '`,\n`'.join(fields_dict) + '`',
            stg_table_name=stg_table_name,
            raw_table_name=raw_table_name,
            schema_name=schema_name
        ))

        if(logger is not None):
            logger.info(
                str(q2.rowcount) +
                ' records inserted into RAW from Staging completed. '
                'in {timedelta} seconds.'
                .format(timedelta=str(round(default_timer() - time_process_start, 2)))
            )
        inserted_records = q2.rowcount

        if(had_transaction is False):
            trans.commit()

        if(logger is not None):
            logger.info(
                'Transaction commit completed. '
                'in {timedelta} seconds.'
                .format(timedelta=str(round(default_timer() - time_process_start, 2)))
            )
    except:
        if(had_transaction is False):
            trans.rollback()

        if(logger is not None):
            logger.error(
                'Error on transaction. '
                'Time elapsed: {timedelta} seconds.'
                .format(timedelta=str(round(default_timer() - time_process_start, 2)))
            )
        raise
    return deleted_records, inserted_records


def sqlite_create_table(
        status_key_column='status_key',
        status_value_column='status_value',
        status_table='status_table'):
    create_sql = """
    CREATE TABLE IF NOT EXISTS 
    {status_table} (
    '{status_key_column}' TEXT,
    '{status_value_column}' TEXT)"""

    create_index_sql = """
    CREATE INDEX IF NOT EXISTS {status_table}_idx  
    ON {status_table} ({status_key_column})"""

    import sqlite3
    connection = sqlite3.connect('sqlite.db')
    cursor = connection.cursor()

    with connection:

        cursor.execute(create_sql.format(
            status_table=status_table,
            status_key_column=status_key_column,
            status_value_column=status_value_column,
        ))

        cursor.execute(create_index_sql.format(
            status_table=status_table,
            status_key_column=status_key_column,
        ))

    connection.close()


def sqlite_set_kv(status_key, status_value,
                  status_key_column='status_key',
                  status_value_column='status_value',
                  status_table='status_table',
                  delete=False):

    insert_sql = """
    INSERT INTO 
        {status_table} 
    ({status_key_column}, {status_value_column}) 
    VALUES 
    ('{status_key}', '{status_value}')"""

    delete_sql = """
    DELETE FROM 
        {status_table} 
    WHERE
        {status_key_column} = '{status_key}'"""

    import sqlite3
    connection = sqlite3.connect('sqlite.db')
    cursor = connection.cursor()

    with connection:
        for _ in range(2):
            try:
                if(delete):
                    cursor.execute(delete_sql.format(
                        status_table=status_table,
                        status_key_column=status_key_column,
                        status_key=status_key,
                    ))

                cursor.execute(insert_sql.format(
                    status_table=status_table,
                    status_key_column=status_key_column,
                    status_value_column=status_value_column,
                    status_key=status_key,
                    status_value=status_value,
                ))
                break
            except sqlite3.OperationalError as operr:
                if(operr.args[0][0:14] == 'no such table:'):
                    sqlite_create_table(status_key_column,
                                        status_value_column,
                                        status_table)
    connection.close()
    return 1


def sqlite_get_kvs(status_keys,
                   status_key_column='status_key',
                   status_value_column='status_value',
                   status_table='status_table'):

    if(type([]) != type(status_keys)):
        status_keys = [status_keys]
    status_keys_str = "'" + "','".join(status_keys) + "'"
    
    select_sql = """
    SELECT 
        {status_key_column},
        {status_value_column}
    FROM
        {status_table}
    WHERE
        {status_key_column} in ({status_keys})
    ORDER BY {status_value_column} DESC"""

    import sqlite3
    
    connection = sqlite3.connect('sqlite.db')
    cursor = connection.cursor()
    response = []
    with connection:
        try:
            cursor.execute(select_sql.format(
                status_table=status_table,
                status_key_column=status_key_column,
                status_value_column=status_value_column,
                status_keys=status_keys_str,
            ))
            response = cursor.fetchall()
        except sqlite3.OperationalError as operr:
            if(operr.args[0][0:14] == 'no such table:'):
                sqlite_create_table(status_key_column,
                                    status_value_column,
                                    status_table)
    connection.close()
    return response


def sqlite_get_kv(status_keys,
                  status_key_column='status_key',
                  status_value_column='status_value',
                  status_table='status_table'):

    resp = sqlite_get_kvs(status_keys,
                  status_key_column,
                  status_value_column,
                  status_table)
    list_return = []
    for row in resp:
        list_return.append(row[1])
    return list_return


def sqlite_get_kvs_dict(status_keys,
                   status_key_column='status_key',
                   status_value_column='status_value',
                   status_table='status_table'):
    resp = sqlite_get_kvs(status_keys,
                   status_key_column,
                   status_value_column,
                   status_table)
    dict_return = {}
    for row in resp:
        dict_return.setdefault(row[0],[]).append(row[1])
    return dict_return


