# Python client for Bulk Importer API

Client for handling app and model requests to the bulk importer API ([Documentation](https://pivotbio.github.io/bulk-api-python-client/bulk_api_client/))

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Installing

To install the project or upgrade it when bugfixes/features are added, there are two methods:

If you have set up an ssh key in github:
```
pip install -U git+ssh://git@github.com/pivotbio/bulk-api-python-client.git
```

If you haven't set up an ssh key in github, you can use the fallback of installing over https:
```
pip install -U git+https://github.com/pivotbio/bulk-api-python-client.git
```


## Usage
From bash or in your systems RC file.

```
export BULK_API_TOKEN='<token>'
```

From Python

```
from bulk_api_client.env_client import env_client as client
ModelName = client.app('app_label').model('model_name')
```

## ModelAPI

### List

List all objects on a model. Only 100 objects can be returned at a time. Use the page option to query for different pages

```
ModelName.list(page=1)
```

Returns a list of ModelObj objects

List can also take a filter and an order similar to the query function. This is useful because rather than only getting that functionality on a query that returns a dataframe, you can now filter and order for ModelObjs

```
ModelName.list(page=1, filter={'or': [{'field_name1': 'value1'}, {'field_name2': 'value2'}]}, order='field', fields=['field1','field2','field3'])
```

### Get

Get a model object using it's primary key

```
ModelName.get(pk=1)
```

Returns a ModelObj object

### Create

Create an object on a model using a dictionary of data on the object

```
ModelName.create(obj_data={})
```

Returns a ModelObj object

#### File Field

ModelAPI supports create/update of an instance with a file as a field. This file field accepts an open file/file buffer. This file is stored in the database and retrievable.

```
with open(file_path, "rb") as file:
     obj_data = {
         "text": "model_text",
         "data_file": file,
     }
     obj = ModelName.create(obj_data)
```

With a ModelObj, a file field on the instance downloads the file from the database to be readable by the user. This will be an open python file object ('rb' mode).

This file object cannot be overwritten or changed with a simple set action (i.e. `model_obj.file = new_file`), as it is read-only. Instead, any changes to the file must use the update method, which will change the file saved to the database completely. Reference the [ModelObj update section](#update) on how to us that method.

### Query

```
ModelName.query(filter=...,order=...,distinct=...,page_size=,fields=[...],skip_cache=bool)
```

Returns a Pandas dataframe object

| Query      | Description                                                         | Example                                    |
| ---------- | ------------------------------------------------------------------- | ------------------------------------------ |
| fields     | Returns a data set of columns containing the specified field(s)     | query(fields=['field1','field2','field3']) |
| filter     | Returns a data set containing objects that match the given field(s) | query(filter={'field_name1': 'value1'})    |
| order      | Returns a data set ordered by the given field(s)                    | query(order='field')                       |
| distinct   | Remove duplicate rows from the result (defaults to False)           | query(distinct=True)
| page size  | Limits the data set to specified number of data points              | query(page_size=10)                        |
| skip_cache | Skip any caching for this request                                   | query(skip_cache=True)                     |

#### Example Queries

```
query(filter={'or': [{'field_name1': 'value1'}, {'field_name2': 'value2'}]}, order='field', fields=['field1','field2','field3'])
```

joins (on foreign key fields use double underscore)

```
query(filter={'field__field_on_related_model': 'value'})
```

field starts with

```
query(filter={'id__startswith': 110})
```

### Complex filter query

```
query(filter={'or': [{'question__startswith': 'Who'}, {'and': [{'question__startswith': 'What'}, {'integer__gte': 1'}]}])
```

# Filter query using Q object

Q objects can be used to simplify making complex queries by allowing users to use pythons built in boolean operators

This produces the same query as the one above.
```
from bulk_api_client import Q

filter_obj = Q(question_startswith='Who') or (Q(question__startswith='What') and Q(integer__gte= 1))
ModelName.query(filter=filter_obj)
```

### Fields

Queries now support using dict for for fields as well as renaming field column output

Example Fields

```
['field1_name', 'field2_name', 'fk__fieldname']
```

Example Fields Dict/OrderedDict with Renamed Fields

```
{field1: new_field1_name}
```

or

```
OrderedDict({field1: new_field1_name})
```

### Filter

Queries now support using YAML for for filters

Example Field Yaml

```
---
     and:
       field1__in:
         - 1
         - 2
         - 3
       field2: "text"
       or:
         fields3__gte: 1
         fields4: "4field"
```

## ModelObj

Object returned by the create/get/list functions of the ModelAPI

### Update

Update an existing object with a dictionary of data

```
.update({...})
```

### Delete

Removes the model instance

```
.delete()
```

Useful Link

- [Django QuerySet Field Lookups](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#field-lookups)

## Running the tests

For testing, we use pytest and coverage. In your terminal/DOS, navigate to the folder this project is stored and run the command

```
pytest -{flag} tests/
```

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

```
git clone git@github.com:pivotbio/bulk-api-python-client.git
```

Install the requirements

```
pip install -e .[dev]
```

Using git, create a branch of the repo. Develop using an IDE of your choice

```
git branch -b {your_branch}
```

Once you're read to add your changes, add them to your branch and commit

```
git add -p
git commit
```

Push your changes and make a pull request on GitHub

```
git push
```

## Authors

- **Mikela Clemmons** - [GitHub Profile](https://github.com/glassresistor)
- **Donnell Muse** - [GitHub Profile](https://github.com/donnell794)
