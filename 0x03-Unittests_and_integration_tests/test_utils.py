#!/usr/bin/env python3

"""
This module contains unit tests for utils.access_nested_map function.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import get_json

class TestAccessNestedMap(unittest.TestCase):
    """
    TestAccessNestedMap class to test the access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """
        Test method to test the access_nested_map function.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",), "Key 'a' not found in nested map"),
        ({"a": 1}, ("a", "b"), "Key 'b' not found in nested map")
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_exception_message):
        """
        Test method to test that KeyError is raised for invalid access.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_exception_message)


class TestGetJson(unittest.TestCase):
    """
    TestGetJson class to test the get_json function.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test method to test that get_json returns the expected result.
        """
        # Mocking the requests.get function
        mock_get.return_value = Mock()
        mock_get.return_value.json.return_value = test_payload

        # Calling the function under test
        result = get_json(test_url)

        # Asserting that requests.get was called exactly once with the test_url argument
        mock_get.assert_called_once_with(test_url)

        # Asserting that the output of get_json is equal to test_payload
        self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()
