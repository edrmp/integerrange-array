from django.db import models
from django.contrib.postgres.fields import ArrayField, IntegerRangeField


class PostgreSQLModel(models.Model):
    class Meta:
        abstract = True


class IntegerRangeArrayModel(PostgreSQLModel):
    field = ArrayField(IntegerRangeField())