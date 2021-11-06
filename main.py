from argparse import ArgumentParser

import pandas as pd
from Levenshtein import distance


def main(laces_file: str, geds_file: str, threshold: float):
    laces = pd.read_csv(laces_file, parse_dates=['Birthdate'])
    geds = pd.read_csv(geds_file, parse_dates=['Date of Birth'])

    laces['DOB'] = laces['Birthdate'].dt.strftime('%Y-%m-%d').fillna('')
    geds['DOB'] = geds['Date of Birth'].dt.strftime('%Y-%m-%d').fillna('')

    laces_keys = laces[['Last Name', 'First Name', 'DOB']].agg(tuple, axis=1).tolist()
    geds_keys = geds[['Last Name', 'First Name', 'DOB']].agg(tuple, axis=1).tolist()

    def _lev(x):
        rates = [sum([distance(n, m) for n, m in zip(x, gm)]) for gm in geds_keys]
        rate_min = min(rates)
        return rate_min, geds_keys[rates.index(rate_min)]

    ds = pd.DataFrame([tuple(x) + _lev(x) for x in laces_keys],
                      columns=['Last', 'First', 'DoB', 'Distance', 'Closest Match'])
    return ds.loc[ds.Distance < threshold].sort_values('Distance')[['Last',
                                                                    'First',
                                                                    'Distance',
                                                                    'DoB',
                                                                    'Closest Match']].reset_index()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('laces_file', help='Full path to the Laces file, quote-surrounded if there are spaces')
    parser.add_argument('ged_file', help='Full path to the GED file, quote-surrounded if there are spaces')
    parser.add_argument('--threshold', type=float, required=False, default=5.0,
                        help='Maximum distance between names for which to print out results')
    args = parser.parse_args()
    results = main(args.laces_file, args.ged_file, args.threshold)
    results.to_csv('results.csv', header=True, index=False)
    print(results)
