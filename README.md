# column_property_repro
Repro of a bug with stacked column properties in SQLAlchemy

When I make a `column_property` that is derived from another `column_property`,
and then try to make a join query on that column, it fails due to column ambiguity.
See `models.py` and `bad_query.py` for the exact setup.

## Error log
```
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.AmbiguousColumn) column reference "foo" is ambiguous
LINE 4: WHERE least(foo, bar, real_thing_children.baz) < 3) AS anon_...
                    ^

[SQL: SELECT count(*) AS count_1 
FROM (SELECT real_thing_children.foo AS real_thing_children_foo, real_thing_children.bar AS real_thing_children_bar, real_thing_children.baz AS real_thing_children_baz, real_thing_children.id AS real_thing_children_id, real_thing_children.parent_id AS real_thing_children_parent_id 
FROM real_thing_children JOIN real_things ON real_thing_children.parent_id = real_things.id 
WHERE least(foo, bar, real_thing_children.baz) < %(param_1)s) AS anon_1]
[parameters: {'param_1': 3}]
```

The `< 3` is just an arbitrary condition on `RealThingChild.foobarbaz`. The behavior I would expect is for `foo` and `bar` to be associated with the `real_thing_children` table, instead of being ambiguous.

## Reproduced with
- Python 3.8 (also happens with 3.9)
- PostgresQL 11.16
- SQLAlchemy 1.3.17 (also happens with 1.4.x; did not test 2.x)

## Setup

1. Clone this repo
2. Initialize a Python env in the same folder: `virtualenv .`
3. Activate the virtualenv: `source bin/activate`
4. Install SQLAlchemy and the `psycopg2` driver:

```
pip install --force-reinstall sqlalchemy==1.3.17

pip install --force-reinstall psycopg2==2.9.3
```

5. Setup your Postgres DB. Connect to it with `sudo -u postgres psql template1`, then:

```
CREATE USER column_property_repro WITH PASSWORD 'password' CREATEDB;
CREATE DATABASE column_property_repro WITH OWNER column_property_repro TEMPLATE template0 ENCODING 'UTF8' LC_COLLATE 'C' LC_CTYPE 'C';
```

6. Run the `model.py` file to generate your tables: `python -m models`
7. Run the `bad_query.py` file to reproduce the error: `python -m bad_query`
