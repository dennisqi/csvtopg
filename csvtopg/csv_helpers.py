import pandas as pd
from datetime import datetime


def split_csv(csv_in, table_name, usecols):
    """Take only wanted columns return a table name and DataFrame"""
    return (table_name, pd.read_csv(csv_in, usecols=usecols))


def read_df_lines(df):
    """Read a CSV file yield a dictionary contains one line."""
    for line in df.T.to_dict().values():
        yield (line)


def get_header(csv):
    return pd.read_csv(csv, nrows=0).columns.tolist()


def write_csv(cleaned_csv, csv_out, index_labels=None, mode='w', header=False, columns=[]):
    """Write cleaned data into csv file.

    :param cleaned_csv: A list of dictionaries, each contains a line of a CSV file.
    :param csv_out: The CSV file that the data will be write into.
    :param index_label: The index labels.
    :param mode: Append ('a') or write ('w').
    :param header: Indicates whether or not write the header line.
    """
    df = pd.DataFrame(cleaned_csv)
    df.to_csv(csv_out, mode=mode, index=False, index_label=index_labels, header=header, columns=columns)


def is_valid(line, validator):
    """Validate a dictionary that is a line of a CSV file.

    :param line: A dictionary contains a line of a CSV file.
    :param validator: A validator that check if the line is valid.
    :return: A boolean indicates if the line is valid.
    """
    return validator(line)


def get_base_filename(ori_name):
    if type(ori_name) != str:
        raise TypeError('origin filename must be a string.')
    if len(ori_name) <= 4 or ori_name[-4:].lower() != '.csv':
        raise ValueError('Invalid origin filename.')
    return ori_name[:-4]


def convert_to_dt(val):
    if not pd.isnull(val):
        try:
            dt = datetime.strptime(val, '%y-%b')
            return dt.strftime('%Y-%m-%d')
        except ValueError as ve:
            pass
        try:
            dt = datetime.strptime(val, '%Y-%b')
            return dt.strftime('%Y-%m-%d')
        except ValueError as ve:
            pass
        try:
            dt = datetime.strptime(val, '%b-%y')
            return dt.strftime('%Y-%m-%d')
        except ValueError as ve:
            pass
        try:
            dt = datetime.strptime(val, '%b-%Y')
            return dt.strftime('%Y-%m-%d')
        except Exception as e:
            pass
        try:
            dt = datetime.strptime('0'+val, '%y-%b')
            return dt.strftime('%Y-%m-%d')
        except Exception as e:
            pass
    # return float('nan')
    return val
