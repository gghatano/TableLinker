# # from django.test import TestCase

# # Create your tests here.
# from datasets.factory import DatasetFactory
# from django.test import TestCase

# from .models import DatasetTemplate


# class DatasetTemplateTestCase(TestCase):
#     def setUp(self):
#         self.dataset = DatasetFactory.create()

#     def test_create_by_dataset(self):
#         """データテンプレート"""
#         tempalte = DatasetTemplate.create_by_dataset(self.dataset)
#         self.assertEqual(tempalte.name, self.dataset.name + "テンプレート")
#         self.assertEqual(tempalte.attr_set.count(), self.dataset.attr_set.count())
#         self.assertEqual(
#             tempalte.attr_set.order_by("index")[0].name, self.dataset.attr_set.order_by("index")[0].name,
#         )
#         self.assertEqual(
#             tempalte.attr_set.order_by("index")[0].index, self.dataset.attr_set.order_by("index")[0].index,
#         )
