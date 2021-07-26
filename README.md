# latex-pdf-automation

A python script to automate generation of pdfs in latex template. You might need to configure the `make_pdf` function depending on your latex template. Currently the script connects to firebase as backend to fetch data, interpolate that into template and generate pdfs.

### Prerequisites

- The script uses a CLI utility `pdflatex` to generate pdfs, so make sure to have a tex distribution installed on your system locally before running this script

- `templates` directory contains the main template in discrete chunks for easier usability and their names are pretty self-explanatory

### CLI

There are three possible CLI arguments. This script uses `fire` package for CLI arguments.

- `createOne` - For generating pdf for a single user (eg: `python script.py createOne userID`)

- `createBatch` - For generating pdfs for specific batch of users (eg: `python script.py createBatch batchID`)

- `createAll` - For generating pdfs for all users in the database (eg: `python script.py createAll`)

### Edge cases covered in python due to some reserved keywords in LaTex

- Usage of comments, newline charachter and pound sign in template file

- Transcoding non-UTF-8 characters to UTF-8
