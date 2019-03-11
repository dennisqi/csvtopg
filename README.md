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
