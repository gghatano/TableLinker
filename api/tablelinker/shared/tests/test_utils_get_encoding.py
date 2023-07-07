import unittest

from django.conf import settings
from factory import django

from ..utils import get_encode


class TestUtilsGetEncode(unittest.TestCase):
    def setUp(self):
        pass

    def test_GetEncodeNkfBinnary(self):
        path = settings.BASE_DIR + "/shared/fixtures/test_files/binary_csv.csv"
        self.assertEqual(get_encode(path, mode="nkf"), "Shift_JIS")

    def test_GetEncodeShiftJis(self):
        path = settings.BASE_DIR + "/shared/fixtures/test_files/shiftjis.csv"
        self.assertEqual(get_encode(path, mode="nkf"), "Shift_JIS")

    def test_GetEncodeUTF8(self):
        path = settings.BASE_DIR + "/shared/fixtures/test_files/utf8.csv"
        self.assertEqual(get_encode(path, mode="nkf"), "UTF-8")
