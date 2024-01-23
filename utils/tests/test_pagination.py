import pytest
from unittest import TestCase
from utils.pagination import custom_pagination_range


@pytest.mark.fast
class PaginationTest(TestCase):
    def setUp(self):
        self.page_range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_custom_pagination_range_first_two_pages_does_not_change(self):
        # FIRST PAGE
        pagination = custom_pagination_range(
            page_range=self.page_range,
            current_page=1,
            pages_to_display=4,
        )
        self.assertEqual(pagination['pagination'], self.page_range[:4])
        # SECOND PAGE
        pagination = custom_pagination_range(
            page_range=self.page_range,
            current_page=2,
            pages_to_display=4,
        )
        self.assertEqual(pagination['pagination'], self.page_range[:4])

    def test_custom_pagination_range_last_two_pages_does_not_change(self):
        # LAST BUT ONE PAGE
        pagination = custom_pagination_range(
            page_range=self.page_range,
            current_page=9,
            pages_to_display=4,
        )
        self.assertEqual(pagination['pagination'], self.page_range[6:10])
        # LAST PAGE
        pagination = custom_pagination_range(
            page_range=self.page_range,
            current_page=10,
            pages_to_display=4,
        )
        self.assertEqual(pagination['pagination'], self.page_range[6:10])

    def test_custom_pagination_range_changes_when_bigger_than_middle_page(self):
        pagination = custom_pagination_range(
            page_range=self.page_range,
            current_page=3,
            pages_to_display=4,
        )
        self.assertEqual(pagination['pagination'], self.page_range[1:5])
