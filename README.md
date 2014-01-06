Dimtable is a Python library that provides editable, multidimensional HTML tables that can be easily mapped to data storage. 

Django model integration is provided out of the box. 

Priorities
----------

The top priority in this fork is currently removing all HTML generation code from the python files. Instead,
we want to rely on the Django templates to generate the HTML. This will give the user much greater power to customize
and style the tables.

Requirements
------------

1. Install Django 
2. Install git 
3. Checkout git repository from https://github.com/tmu/dimtable


Demo instructions
-----------------
    
    export PYTHONPATH=<path to the root of the project, i.e. the dir that contains README.md>
    e.g.
    export PYTHONPATH=~/dimtable

    cd djangoexample
    mysql --user=root -p < create_db.sql
    python manage.py syncdb
    python manage.py create_ex1_data
    python manage.py collectstatic
    python manage.py runserver


