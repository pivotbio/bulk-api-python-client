# Python client for Bulk Importer API

Client for handling app and model requests to the bulk importer API (Docs: <https://pivotbio.github.io/bulk-api-python-client/bulk_api_client/>)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Installing

Since this is a private repo, you will have to install using SSH

To install the project

    pip install git+ssh://git@github.com/pivotbio/bulk-api-python-client.git

## Usage

    from bulk_api_client import Client

    client = Client(token)
    client.app('app_label').model('model_name').query(filter=...,order=...,page=,page_size=,fields=[...])

| Query     | Description                                                         | Example                                   |
| --------- | ------------------------------------------------------------------- | ----------------------------------------- |
| fields    | Returns a data set of columns containing the specified field(s)     | query(fields=['field1','field2','field3'] |
| filter    | Returns a data set containing objects that match the given field(s) | query(filter='field_name1=value1')        |
| order     | Returns a data set ordered by the given field(s)                    | query(order='field')                      |
| page      | Returns a data set of a specified page number                       | query(page=1)                             |
| page size | Limits the data set to specified number of data points              | query(page_size=10)                       |

##### Example Queries

    query(filter='field_name1=value1|field_name2=vaue2', order='field', fields=['field1','field2','field3'])

joins (on foreign key models use double underscore)

    query(filter='field__field_on_related_model')

field starts with

    query(filter='id__startswith=110')

Complex filter query

    query(filter='question__startswith=Who|question__startswith=What&integer__gte=1')

Useful Link

-   [Django QuerySet Field Lookups](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#field-lookups)

## Running the tests

For testing, we use pytest and coverage. In your terminal/DOS, navigate to the folder this project is stored
and run the command

    pytest -{flag} tests/

### Useful flags

| Flag                    | Description                                                                                                                                                                      | Example                                      |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| -s                      | Show output                                                                                                                                                                      | pytest -s                                    |
| -x                      | Stop after first failure                                                                                                                                                         | pytest -x                                    |
| -vv                     | Verbose output from pytest                                                                                                                                                       | pytest -vv                                   |
| -q, --quiet             | Less verbose                                                                                                                                                                     | pytest -q                                    |
| --count                 | Run tests {count} # of times                                                                                                                                                     | pytest --count=10                            |
| {test_file}::{function} | Run specified function in test                                                                                                                                                   | pytest tests/test_file::test_fn              |
| -r chars                | Show extra test summary info as specified by chars: (f)ailed, (E)error, (s)skipped, (x)failed, (X)passed, (w)pytest-warnings (p)passed, (P)passed with output, (a)all except pP. | pytest -r fe                                 |
| -k "expression"         | Only run tests that match expession (and fixtures)                                                                                                                               | pytest -k 'test_001 or test_some_other_test' |

### Coding Style Tests

Tests will automatically check for code style, which should adhere to Pep8

## Contributing

Clone the repository

    git clone git@github.com:pivotbio/bulk-api-python-client.git

Install the requirements

    pip install -e .[dev]

Using git, create a branch of the repo. Develop using an IDE of your choice

    git branch -b {your_branch}

Once you're read to add your changes, add them to your branch and commit

    git add -p
    git commit

Push your changes and make a pull request on GitHub

    git push

## Authors

-   **Mikela Clemmons** - [GitHub Profile](https://github.com/glassresistor)
-   **Donnell Muse** - [GitHub Profile](https://github.com/donnell794)
