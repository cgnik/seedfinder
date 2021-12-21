from functools import partial

import pandas as pd
from Levenshtein import distance


def _lev(geds_keys: pd.DataFrame, x):
    rates = [sum([distance(n, m) for n, m in zip(x, gm)]) for gm in geds_keys]
    rate_min = min(rates)
    return rate_min, geds_keys[rates.index(rate_min)]


def seeds_geds(laces_file: str, geds_file: str, threshold: int):
    laces = pd.read_csv(laces_file, parse_dates=['Birthdate'])
    geds = pd.read_csv(geds_file, parse_dates=['Date of Birth'])

    laces['DOB'] = laces['Birthdate'].dt.strftime('%Y-%m-%d').fillna('')
    geds['DOB'] = geds['Date of Birth'].dt.strftime('%Y-%m-%d').fillna('')

    laces_keys = laces[['Last Name', 'First Name', 'DOB']].agg(tuple, axis=1).tolist()
    geds_keys = geds[['Last Name', 'First Name', 'DOB']].agg(tuple, axis=1).tolist()

    _l = partial(_lev, geds_keys)
    ds = pd.DataFrame([tuple(x) + _l(x) for x in laces_keys],
                      columns=['Last', 'First', 'DoB', 'Distance', 'Closest Match'])
    return ds.loc[ds.Distance < threshold].sort_values('Distance')[['Last',
                                                                    'First',
                                                                    'Distance',
                                                                    'DoB',
                                                                    'Closest Match']].reset_index()
