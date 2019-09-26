# cmput497_a1_yonael_zichun3

## Prerequisites

-   Python 3.7+
-   [virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

## Setup

```sh
# Setup python virtual environment
$ virtualenv venv --python=python3
$ source venv/bin/activate

# Install python dependencies
$ pip install -r requirements.txt
```

## Run

Simply run `python main.py`, output `TSV` files are saved into `output/` folder.

```
usage: main.py [-h] [--input INPUT]

Extract relations from wiki files.

optional arguments:
  -h, --help     show this help message and exit
  --input INPUT  Provide path to directory of input wiki files
```

## Author

-   Yonael Bekele - yonael
-   Michael Lin - zichun3
