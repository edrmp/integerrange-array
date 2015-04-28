# integerrange-array
Test project to demonstrate an issue with a  IntegerRangeField ArrayField

I'm with problems trying to create a model object that contains an ArrayField with IntegerRangeField as base.


Model:


```python
class PostgreSQLModel(models.Model):
    class Meta:
        abstract = True


class IntegerRangeArrayModel(PostgreSQLModel):
    field = ArrayField(IntegerRangeField())
```

The initial migration an the table are created fine.

```
                           Table "public.core_integerrangearraymodel"
 Column |    Type     |                                Modifiers
--------+-------------+--------------------------------------------------------------------------
 id     | integer     | not null default nextval('core_integerrangearraymodel_id_seq'::regclass)
 field  | int4range[] | not null
Indexes:
    "core_integerrangearraymodel_pkey" PRIMARY KEY, btree (id)
```


However, when I try to create an object, it fails with a SQL error.

```python

integer_range_list = [
    (10, 20),
    (30, 40),
]

IntegerRangeArrayModel.objects.create(
    field=integer_range_list
)

```

```

======================================================================
ERROR: test_create_with_tuples (core.tests.TestIntegerRangeArray)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/eder/.virtualenvs/integerrange-array/lib/python3.4/site-packages/django/db/backends/utils.py", line 64, in execute
    return self.cursor.execute(sql, params)
psycopg2.ProgrammingError: column "field" is of type int4range[] but expression is of type text[]
LINE 1: ...O "core_integerrangearraymodel" ("field") VALUES (ARRAY['[10...
                                                             ^
HINT:  You will need to rewrite or cast the expression.


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/eder/devel/integerrange-array/core/tests.py", line 17, in test_create_with_tuples
    field=integer_range_list
  File "/home/eder/.virtualenvs/integerrange-array/lib/python3.4/site-packages/django/db/models/manager.py", line 127, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/home/eder/.virtualenvs/integerrange-array/lib/python3.4/site-packages/django/db/models/query.py", line 348, in create
    obj.save(force_insert=True, using=self.db)
  File "/home/eder/.virtualenvs/integerrange-array/lib/python3.4/site-packages/django/db/models/base.py", line 710, in save
    force_update=force_update, update_fields=update_fields)
  File "/home/eder/.virtualenvs/integerrange-array/lib/python3.4/site-packages/django/db/models/base.py", line 738, in save_base
    updated = self._save_table(raw, cls, force_insert, force_update, using, update_fields)
  File "/home/eder/.virtualenvs/integerrange-array/lib/python3.4/site-packages/django/db/models/base.py", line 822, in _save_table
    result = self._do_insert(cls._base_manager, using, fields, update_pk, raw)
  File "/home/eder/.virtualenvs/integerrange-array/lib/python3.4/site-packages/django/db/models/base.py", line 861, in _do_insert
    using=using, raw=raw)
  File "/home/eder/.virtualenvs/integerrange-array/lib/python3.4/site-packages/django/db/models/manager.py", line 127, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/home/eder/.virtualenvs/integerrange-array/lib/python3.4/site-packages/django/db/models/query.py", line 920, in _insert
    return query.get_compiler(using=using).execute_sql(return_id)
  File "/home/eder/.virtualenvs/integerrange-array/lib/python3.4/site-packages/django/db/models/sql/compiler.py", line 963, in execute_sql
    cursor.execute(sql, params)
  File "/home/eder/.virtualenvs/integerrange-array/lib/python3.4/site-packages/django/db/backends/utils.py", line 64, in execute
    return self.cursor.execute(sql, params)
  File "/home/eder/.virtualenvs/integerrange-array/lib/python3.4/site-packages/django/db/utils.py", line 97, in __exit__
    six.reraise(dj_exc_type, dj_exc_value, traceback)
  File "/home/eder/.virtualenvs/integerrange-array/lib/python3.4/site-packages/django/utils/six.py", line 658, in reraise
    raise value.with_traceback(tb)
  File "/home/eder/.virtualenvs/integerrange-array/lib/python3.4/site-packages/django/db/backends/utils.py", line 64, in execute
    return self.cursor.execute(sql, params)
django.db.utils.ProgrammingError: column "field" is of type int4range[] but expression is of type text[]
LINE 1: ...O "core_integerrangearraymodel" ("field") VALUES (ARRAY['[10...
                                                             ^
HINT:  You will need to rewrite or cast the expression.


```

There are no difference if a NumericRange object is used instead.


```python

integer_range_list = [
    NumericRange(10, 20),
    NumericRange(30, 40),
]

IntegerRangeArrayModel.objects.create(
    field=integer_range_list
)

```

The generated SQL is:

```sql

INSERT INTO "core_integerrangearraymodel" ("field") VALUES (ARRAY['[10,20)', '[30,40)']) RETURNING "core_integerrangearraymodel"."id"

```

It should be something like this:

```sql

INSERT INTO "core_integerrangearraymodel" ("field") VALUES (ARRAY['[10,20)'::int4range, '[30,40)'::int4range]) RETURNING "core_integerrangearraymodel"."id"

```

or this:

```sql

INSERT INTO "core_integerrangearraymodel" ("field") VALUES ('{"[10,20)","[30,40)"}') RETURNING "core_integerrangearraymodel"."id";

```

