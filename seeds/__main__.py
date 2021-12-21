from argparse import ArgumentParser

from seeds import seeds_geds


def _args():
    parser = ArgumentParser()
    parser.add_argument('laces_file', help='Full path to the Laces file, quote-surrounded if there are spaces')
    parser.add_argument('ged_file', help='Full path to the GED file, quote-surrounded if there are spaces')
    parser.add_argument('--threshold', type=float, required=False, default=5.0,
                        help='Maximum distance between names for which to print out results')
    return parser.parse_args()


if __name__ == '__main__':
    args = _args()
    results = seeds_geds(args.laces_file, args.ged_file, args.threshold)
    results.to_csv('results.csv', header=True, index=False)
    print(results)
