from django.test import TestCase
from django.db import connection
from psycopg2.extras import NumericRange

from core.models import IntegerRangeArrayModel


class TestIntegerRangeArray(TestCase):

    def test_create_with_tuples(self):
        integer_range_list = [
            (10, 20),
            (30, 40),
        ]

        ir = IntegerRangeArrayModel.objects.create(
            field=integer_range_list
        )
        loaded = IntegerRangeArrayModel.objects.get()
        assert ir.pk
        self.assertEqual(loaded.field, integer_range_list)

    def test_create_with_numericrange(self):
        integer_range_list = [
            NumericRange(10, 20),
            NumericRange(30, 40),
        ]

        ir = IntegerRangeArrayModel.objects.create(
            field=[NumericRange(10, 20), NumericRange(30, 40), ]
        )
        loaded = IntegerRangeArrayModel.objects.get()
        assert ir.pk
        self.assertEqual(loaded.field, integer_range_list)


