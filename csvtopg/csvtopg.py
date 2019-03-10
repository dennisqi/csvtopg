import os
import pandas as pd
import csvhelper
import secrets
from pghelper import PGHelper
from validators import validators, cols

FORMAT = '%b-%y'


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
            self, user, password, database, csv_file, dt_cols=[], table_name_usecols=[], csv_cleaned_file=None):
        super().__init__(user, password, database)
        self.csv_file = csv_file
        self.csv_cleaned_file = csv_cleaned_file
        self.table_name_usecols = table_name_usecols
        self.dt_cols = dt_cols

        # If no cleaned output file specified,
        #   use the same name as csv_file and add '_clean' at the end.
        if not self.csv_cleaned_file:
            path = self.csv_file[:-4]
            self.csv_cleaned_file = path + '_cleaned.csv'

    def load_csv_to_pg(self):
        """Load a CSV file, clean it and store into PostgreSQL DB."""

        # Generating a list of tuples, (table_name, DataFrame)
        dfs = []
        if not self.table_name_usecols:
            dfs = [('all', pd.read_csv(self.csv_file))]
        else:
            dfs = [csvhelper.split_csv(self.csv_file, table_name, usecols) for table_name, usecols in self.table_name_usecols]

        # For each table_name and DataFrame(CSV file),
        #   validate it and write into cleaned CSV file
        for table_name, df in dfs:

            # Indicates if we wrote header or not
            wrote_header = False

            # columns order
            columns = []

            # For each row of DataFrame (each record of the CSV file)
            for line_dict in csvhelper.read_df_lines(df):

                # Provide the validate for that table
                v = validators[table_name]

                if v.validate(line_dict):

                    # # If there are string type datatime column
                    # #   add another column with datatime type
                    for col in self.dt_cols:
                        line_dict[col] = csvhelper.convert_to_dt(line_dict[col], FORMAT)

                    # Setup columns and will not change the order
                    if not columns:
                        columns = line_dict.keys()

                    # Decide if append or write into file
                    mode = 'a' if wrote_header else 'w'

                    header = False if wrote_header else True

                    # Added table name in the file,
                    #   loan_clean.csv => load_clean_table_name.csv
                    output_file_name = csvhelper.change_csv_file_name(self.csv_cleaned_file, table_name)
                    csvhelper.write_csv(
                        [line_dict], output_file_name, mode=mode, header=header, columns=columns)

                    # Changed wrote_header to False after write the first line
                    wrote_header = True
                else:
                    print(line_dict['emp_title'])
                    print(type(line_dict['emp_title']))
                    print(pd.isnull(line_dict['emp_title']))
                    print(v.errors)


if __name__ == '__main__':
    user = secrets.CP_PG_USER
    password = secrets.CP_PG_PASSWORD
    database = secrets.CP_PG_DATABASE

    dt_cols = [
        'issue_d', 'earliest_cr_line', 'last_pymnt_d',
        'next_pymnt_d', 'last_credit_pull_d'
    ]

    csvtopg = CSVToPG(
        user, password, database, '../data/loan.csv', dt_cols=dt_cols)
    csvtopg.load_csv_to_pg()
