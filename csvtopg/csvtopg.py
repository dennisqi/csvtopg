import os
import pandas as pd
import csvhelper
import secrets
from pghelper import PGHelper
from validators import validators, cols


class CSVToPG(PGHelper):
    """Used to read, clean, and write a CSV file into Postgres DB.

    :param username: PostgreSQL DB user name.
    :param password: PostgreSQL DB password.
    :param dbname: PostgreSQL DB database name.
    :param csv_file: The CSV file to read from.
    :prarm csv_cleaned_file: The CSV file name to write cleaned CSV file into.
    :param table_usecols: A list of tuples contain table name and wanted columns
        to split CSV file into different tables.
    """

    def __init__(
            self, user, password, database, csv_file, table_name_usecols=[], csv_cleaned_file=None):
        super().__init__(user, password, database)
        self.csv_file = csv_file
        self.csv_cleaned_file = csv_cleaned_file
        self.table_name_usecols = table_name_usecols

        # If no cleaned output file specified,
        #   use the same name as csv_file and add '_clean' at the end.
        if not self.csv_cleaned_file:
            path = self.csv_file[:-4]
            self.csv_cleaned_file = path + '_cleaned.csv'

    def load_csv_to_pg(self):
        """Load a CSV file, clean it and store into PostgreSQL DB."""
        dfs = []
        if not self.table_name_usecols:
            dfs = [('all', pd.read_csv(self.csv_file))]
        else:
            dfs = [csvhelper.split_csv(self.csv_file, table_name, usecols) for table_name, usecols in self.table_name_usecols]

        for table_name, df in dfs:
            wrote_header = False
            for line_dict in csvhelper.read_df_lines(df):
                v = validators[table_name]
                if v.validate(line_dict):
                    mode = 'a' if wrote_header else 'w'
                    header = False if wrote_header else True
                    output_file_name = self.change_csv_file_name(self.csv_cleaned_file, table_name)
                    csvhelper.write_csv(
                        [line_dict], output_file_name, mode=mode, header=header)
                    wrote_header = True
                else:
                    print(line_dict['emp_title'])
                    print(type(line_dict['emp_title']))
                    print(pd.isnull(line_dict['emp_title']))
                    print(v.errors)

    def change_csv_file_name(self, ori_name, table_name):
        """Add table name at the end of ori nameself.

        'loan.csv', 'usertb' => 'loan_usertb.csv'
        """
        return ori_name[:-4] + '_%s.csv' % table_name


if __name__ == '__main__':
    user = secrets.CP_PG_USER
    password = secrets.CP_PG_PASSWORD
    database = secrets.CP_PG_DATABASE

    csvtopg = CSVToPG(
        user, password, database, '../data/loan_head.csv')
    csvtopg.load_csv_to_pg()
