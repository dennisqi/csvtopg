# csvtopg

csvtopg is a program to load loan related CSV file(s) into PostgreSQL databases.

## How to install and run
[Optional] Changing PostgreSQL DB username, password and database name in `csvtopg/secrets.txt`.

[Optional] Changing validation rules in `csvtopg/validators.py`.

[Optional] Changing schema and insertion in `csvtopg/queries.py`

[Optional] Activating virtual environment.
```bash
$ conda create -n landingclub pip
$ conda activate landingclub
```

**[Required]** Installing packaged and running program
```bash
$ pip install -r requirements.txt
$ ./upload.sh data/loan.csv
```

## How does csvtopg work
It first generate a `CSVToPG` instance which extends from `PGHelper`.

The `CSVToPG` will then call its `load_csv_to_pg()` method, which will do the follwing steps.

First, it iterate through all tables that can be filled using this CSV file.

For each table:
* Creates a table in database
* Generate a CSV filename for output **valid** record.
* Generate a CSV filename for output **invalid** record.
* Generate a CSV filename for output **reason** for invalid record.
* Then for each record:
    * Validate this record.
    * Insert into table.
    * Write into valid/invalid file.


There are a few options when initialize the CSVToPG.
* **table_creations**: A dictionray of table creation queries.
```python
{
    'user_tb': '''
        CREATE TABLE IF NOT EXISTS user_tb (
            id NUMERIC NOT NULL PRIMARY KEY,
            name TEXT
        );'''
}
```
* **update**: Indicates whether or not update the record in database if find the same pk.
* **dt_cols**: Datatime column names, will be convert to datetime str format.
```python
dt_cols = ['date_borrowed']
# Record: 'Dec-09' => 2009-12-01
# Record: 'Dec-2009' => 2009-12-01
```
* **table_name_usecols**: A list of tables the CSV file can be splited into (e.g. loan.csv can be split into 'user' table and 'loan_record' table if needed).
* **alter_tables**: A dictionary of tuples containing table_name and alter query.
```python
{
    'all_tb': '''
    ALTER TABLE all_tb ADD COLUMN test_add_column TEXT;
    '''
}
```
