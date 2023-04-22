# hp_4.py
#
from datetime import datetime, timedelta
import pandas as pd
from csv import DictReader, DictWriter
from collections import defaultdict

def reformat_dates(old_dates):
    """ Reform The Dates"""
    outl = []
    for i in old_dates:
        k = dt.datetime.strptime(i, '%Y-%m-%d')
        outl.append(k.strftime('%d %b %Y'))
    return outl


def date_range(start, n):
    """Gets the Date Range """
    if  not isinstance(start, str):
        raise TypeError
    elif not isinstance(n, int):
        raise TypeError
    else:
        a1 = dt.datetime.strptime(start, '%Y-%m-%d')
        k = [a1]
        for i in range(n - 1):
            a1 += dt.timedelta(days=1)
            k.append(a1)
        return k


def add_date_range(values, start_date):
    """ Add Dat e Range """
    date_val = date_range(start_date, len(values))
    k = []
    for i in range(len(values)):
        k.append((date_val[i], values[i]))
    return k


def fees_report(infile, outfile):
    """ Final Infile /Outfile Output"""
    df = pd.read_csv(infile)
    df = df.drop(['book_uid', 'isbn_13', 'date_checkout'], axis=1)
    df['date_due'] = pd.to_datetime(df['date_due'], format="%m/%d/%Y")
    df['date_returned'] = pd.to_datetime(df['date_returned'],
                                         format="%m/%d/%Y")
    df['extra_days'] = df['date_returned'] - df['date_due']
    df['extra_days'] = df['extra_days'].map(
                       lambda k: int(str(k).split(' ')[0]))
    df['extra_days'] = df['extra_days'].map(lambda k: k if k > 0 else 0)
    df['late_fees'] = df['extra_days'].map(lambda k: round(k*0.25, 2))
    df.drop(['date_due', 'date_returned', 'extra_days'], axis=1, inplace=True)
    df = df.groupby(['patron_id']).sum()
    # return df
    df.to_csv(outfile)






# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
