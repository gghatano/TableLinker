from django.test import TestCase
from factory import django

from datasets.factory import DatasetFactory


class DatasetTestCase(TestCase):
    fixtures = [
        "datasets/fixtures/attr_type.yaml",
    ]

    def setUp(self):
        self.dataset = DatasetFactory.create()

    def test_analyze(self):
        """データ分析のテスト"""
        self.dataset.analyze()
        self.assertEqual(self.dataset.is_analyzed, True)
        self.assertEqual(self.dataset.num_columns, 57)
        self.assertEqual(self.dataset.num_records, 1317)
        self.assertEqual(self.dataset.attr_set.count(), 57)


class DatasetWithAttrTypeTestCase(TestCase):
    fixtures = [
        "datasets/fixtures/attr_type.yaml",
    ]

    def setUp(self):
        original_file = django.FileField(from_path="datasets/fixtures/tests/datasets/attr_type_data.csv", filename="data.csv")
        self.dataset = DatasetFactory.create(original_file=original_file)

    def test_analyze(self):
        """データ分析のテスト"""
        self.dataset.analyze()
        self.assertEqual(self.dataset.is_analyzed, True)
        self.assertEqual(self.dataset.num_columns, 16)
        self.assertEqual(self.dataset.num_records, 2)
        self.assertEqual(self.dataset.attr_set.count(), 16)
        for attr in self.dataset.attr_set.all():
            if attr.name == "組織":
                self.assertEqual(attr.attr_type.key, "organizaion")
            if attr.name == "面積":
                self.assertEqual(attr.attr_type.key, "area")
            if attr.name == "価格":
                self.assertEqual(attr.attr_type.key, "price")
            if attr.name == "日付":
                self.assertEqual(attr.attr_type.key, "date")
            if attr.name == "日時":
                self.assertEqual(attr.attr_type.key, "datetime")
            # print("{}:{}".format(attr.name, attr.attr_type))
