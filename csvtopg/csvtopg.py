import sys
import json
import pandas as pd
import csv_helpers
import secrets
from pg_helper import PGHelper
from queries import LOAN_TABLE_CREATION_QUERY
from queries import insert_head, insert_body, insert_tail
from validators import validators, cols
from psycopg2 import IntegrityError


class CSVToPG(PGHelper):
    """Used to read, clean, and write a CSV file into Postgres DB.

    :param user: PostgreSQL DB user name.
    :param password: PostgreSQL DB password.
    :param database: PostgreSQL DB database name.
    :param csv_file: The CSV file to read from.
    :param table_creations: A dictionray of table creation queries.
    :param update: Whether or not update the record (using the latest CSV file)
        that is already in the table.
    :param dt_cols: Datatime column names, will be convert to datetime.
    :param table_name_usecols: A list of tables the CSV file can be splited into,
        loan.csv can be split into 'user' table and 'loan_record' table.
    :param csv_cleaned_filename: The CSV file name to write cleaned CSV file into.
    """

    def __init__(
            self, user, password, database, csv_file, table_creations, update,
            dt_cols=[], table_name_usecols=[], csv_cleaned_filename=None, pk='id'):
        super().__init__(user, password, database)
        self.csv_file = csv_file
        self.csv_cleaned_filename = csv_cleaned_filename
        self.table_name_usecols = table_name_usecols
        self.dt_cols = dt_cols
        self.table_creations = table_creations
        self.update = update
        self.pk = pk

        # If no cleaned output file specified,
        #   use the same name as csv_file and add '_clean' at the end.
        if not self.csv_cleaned_filename:
            base_filename = csv_helpers.get_base_filename(self.csv_file)
            self.csv_cleaned_filename = base_filename + '_cleaned.csv'

        self.pg_helper = PGHelper(user, password, database)

    def generate_table_name_dataframes(self):
        """Generate a list of tuples contain table names and dataframes.

        If there are more than one table the CSV file can be parsed,
        table_name_usecols is needed to be provided, it will parse table names
        and column names in coresponding table.
        """
        if not self.table_name_usecols:
            return [('all_tb', pd.read_csv(self.csv_file))]
        return [csv_helpers.split_csv(self.csv_file, table_name, usecols) for table_name, usecols in self.table_name_usecols]

    def drop_table(self, table_name):
        drop_all_tb_query = """DROP TABLE IF EXISTS %s""" % table_name
        self.pg_helper.execute(drop_all_tb_query, [])

    def create_table(self, table_name):
        creation_query = self.table_creations[table_name]
        self.pg_helper.execute(creation_query, [])

    def csv_add_tail(self, file_path, added):
        """Added table name to the end of filename.

        loan_clean.csv => load_clean_table_name.csv
        """
        base_filename = csv_helpers.get_base_filename(file_path)
        return base_filename + '_%s.csv' % added

    def csv_add_head(self, file_path, added):
        file_path_parts = file_path.split('/')
        return '/'.join(file_path_parts[:-1] + ['%s_' % added + file_path_parts[-1]])

    def write_db(self, line_dict, table_name):
        """Write record into table.

        :param line_dict: A dictionray contains a loan record.
        :param table_name: Table name.
        """
        keys, values = line_dict.keys(), line_dict.values()
        # write into db
        insert_query = \
            insert_head % table_name \
            + ','.join(map(lambda x: '"%s"' % x, keys)) \
            + insert_body \
            + ','.join('%s' for _ in range(len(keys))) \
            + insert_tail
        self.pg_helper.execute(insert_query, list(values))

    def delete_record(self, pk, table_name):
        self.pg_helper.execute('DELETE FROM %s WHERE %s = %d' % (table_name, self.pk, pk), [])

    def write_invalid_reason(self, reason_filename, line_dict, errors):
        with open(reason_filename, 'a') as f:
            f.write(
                'Reason: '
                + json.dumps(errors)
                + ';ReasonEnd; Record: '
                + json.dumps(line_dict)
                + ';RecordEnd;\n')

    def load_csv_to_pg(self):
        """Load a CSV file, clean it and store into PostgreSQL DB."""

        # Generating a list of tuples, (table_name, DataFrame)
        dfs = self.generate_table_name_dataframes()

        # For each table_name and DataFrame(CSV file),
        #   validate it and write into cleaned CSV file
        for table_name, df in dfs:

            # Indicates if we wrote header or not
            valid_wrote_header = False
            invalid_wrote_header = False

            # columns order
            columns = []

            # Create table for table_name.
            # Call self.drop_table(table_name) if necessary.
            self.create_table(table_name)

            # CSV valid record and invalid record output filenames
            valid_output_filename = self.csv_add_tail(self.csv_cleaned_filename, table_name)
            invalid_filename = self.csv_add_head(valid_output_filename, 'invalid')
            reason_filename = self.csv_add_head(valid_output_filename, 'reason')

            # For each line or record of DataFrame (each record of the CSV file)
            for line_dict in csv_helpers.read_df_lines(df):

                # Setup columns and will not change the order
                if not columns:
                    columns = line_dict.keys()

                # Provide the validate for that table
                v = validators[table_name]

                if v.validate(line_dict):

                    # Decide if append or write into file
                    valid_mode = 'a' if valid_wrote_header else 'w'

                    # Set if need to write a header
                    valid_header = False if valid_wrote_header else True

                    # # If there are string type datatime column
                    # #   add another column with datatime type
                    for col in self.dt_cols:
                        line_dict[col] = csv_helpers.convert_to_dt(line_dict[col])

                    try:
                        self.write_db(line_dict, table_name)

                        csv_helpers.write_csv(
                            [line_dict],
                            valid_output_filename,
                            mode=valid_mode,
                            header=valid_header,
                            columns=columns)
                    except IntegrityError as ie:
                        if self.update:
                            self.delete_record(line_dict[self.pk], table_name)
                            self.write_db(line_dict, table_name)
                    except Exception as e:
                        print(line_dict)
                        print(str(e))

                    # Changed wrote_header to False after write the first line
                    valid_wrote_header = True

                else:
                    # Decide if append or write into file
                    invalid_mode = 'a' if invalid_wrote_header else 'w'

                    # Set if need to write a header
                    invalid_header = False if invalid_wrote_header else True

                    csv_helpers.write_csv(
                        [line_dict],
                        invalid_filename,
                        mode=invalid_mode,
                        header=invalid_header,
                        columns=columns)

                    self.write_invalid_reason(reason_filename, line_dict, v.errors)

                    # Changed wrote_header to False after write the first line
                    invalid_wrote_header = True


if __name__ == '__main__':

    csv_filename = sys.argv[1]
    if csv_filename[-4:].lower() != '.csv':
        print(csv_filename)
        raise ValueError('Needed to be a csv file')

    user = secrets.CP_PG_USER
    password = secrets.CP_PG_PASSWORD
    database = secrets.CP_PG_DATABASE

    dt_cols = [
        'issue_d', 'earliest_cr_line', 'last_pymnt_d',
        'next_pymnt_d', 'last_credit_pull_d'
    ]

    table_creations = {
        'all_tb': LOAN_TABLE_CREATION_QUERY
    }

    csvtopg = CSVToPG(
        user, password, database, csv_filename, table_creations, update=True,
        dt_cols=dt_cols, pk='id')
    csvtopg.load_csv_to_pg()
