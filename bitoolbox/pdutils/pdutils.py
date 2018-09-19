# -*- coding: utf-8 -*-
"""This module do some helper functions to pandas."""

import pandas as pd


def fill_grouped(df_input, group_fields,
                 fill_columns=None, sort_fields=None,
                 fill_method='ffill', check_not_in_list_value=False):
    """ ATENTION: This Dataframe need to be sorted, 
    or use the sort_fields correctly 
    """

    df = df_input.copy()
    if(sort_fields is not None):
        df = df.sort_values(group_fields + sort_fields)

    if(type([]) != type(group_fields)):
        group_fields = [group_fields]

    if(fill_columns is None):
        fill_columns = list(set(df.columns) - set(group_fields))

    indexer_last = df.groupby(group_fields, as_index=False).nth(-1).index
    indexer_first = df.groupby(group_fields, as_index=False).nth(0).index
    # print('indexer_last: ', indexer_last)
    # print('indexer_first: ', indexer_first)
    for col in fill_columns:
        # print('col: ', col)
        if(not df[col].isnull().any()):
            continue
        indexer_last_null = indexer_last[df.loc[indexer_last, col].isnull()]
        indexer_first_null = indexer_first[df.loc[indexer_first, col].isnull()]
        # print('indexer_last_null: ', indexer_last_null)
        # print('indexer_first_null: ', indexer_first_null)

        first_not_null_val = -999
        last_not_null_val = -998

        if(check_not_in_list_value):
            while((df[col] == first_not_null_val).any()):
                first_not_null_val = first_not_null_val + 1
            while((df[col] == last_not_null_val).any()):
                last_not_null_val = last_not_null_val - 1

        df.loc[indexer_last_null, col] = first_not_null_val
        df.loc[indexer_first_null, col] = last_not_null_val

        if(fill_method in ['ffill', 'forwardfill', 'pad']):
            replace_all = first_not_null_val
            replace_first = last_not_null_val
        else:
            fill_method = 'bfill'
            replace_all = last_not_null_val
            replace_first = first_not_null_val

        df[col] = df[col].fillna(
            method=fill_method
        ).replace(
            replace_all, pd.np.nan
        ).fillna(
            method=fill_method, limit=1
        ).replace(
            replace_first, pd.np.nan
        )
    return df


def shift_compare_unless_fields(df, not_equal_fields=[], compare_with_next=False):
    """ ATENTION: This Dataframe need to be sorted!!!
    """
    import pandas as pd

    if(type([]) != type(not_equal_fields)):
        not_equal_fields = [not_equal_fields]

    s = True
    s_created = False

    if compare_with_next:
        shift_value = -1
    else:
        shift_value = 1

    for col in df.columns:
        
        if col not in not_equal_fields:
            compare = df[col].fillna(0) == df[col].fillna(0).shift(shift_value)
            if(s_created):
                s = (compare) & (s)
            else:
                s = pd.Series(compare)
                s_created = True
    return s


def shift_compare_date(df, date_field, smaller_eq_than_days=1, compare_with_next=False):
    """ ATENTION: This Dataframe need to be sorted!!!
    """
    from datetime import timedelta

    if compare_with_next:
        s = (
            (df[date_field].shift(-1) - df[date_field]
             ) <= timedelta(days=smaller_eq_than_days)
        ) & (
            (df[date_field].shift(-1) - df[date_field]) > timedelta(days=0)
        )
    else:
        s = (
            (df[date_field] - df[date_field].shift(1)
             ) <= timedelta(days=smaller_eq_than_days)
        ) & (
            (df[date_field] - df[date_field].shift(1)) >= timedelta(days=0)
        )

    return s


def drop_repeated_with_dt_limit(df,
                                key_fields,
                                date_field,
                                smaller_eq_than_days=1,
                                keep_last=False,
                                drop_index=True):

    if(type([]) != type(key_fields)):
        key_fields = [key_fields]

    if(type([]) != type(date_field)):
        date_field = [date_field]

    dfi = df.sort_values(
        key_fields + date_field
    ).reset_index(drop=drop_index).copy()

    # Verificar se os dados são iguais ao próximo
    s_compare = shift_compare_unless_fields(
        dfi,
        date_field
    )

    # Verificar se a data do próximo é apenas smaller_eq_than_days menor
    s_date = shift_compare_date(dfi, date_field[0], smaller_eq_than_days)

    s_comb1 = s_compare & s_date
    if(keep_last):
        s_comb1 = s_comb1 & s_comb1.shift(-1)

    return dfi.drop(dfi[s_comb1].index)
