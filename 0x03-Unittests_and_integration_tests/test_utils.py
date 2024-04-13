#!/usr/bin/env python3

"""
This module contains unit tests for utils.access_nested_map function.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import get_json, memoize
from client import GithubOrgClient

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

class TestMemoize(unittest.TestCase):
    """
    TestMemoize class to test the memoize decorator.
    """

    class TestClass:
        """
        TestClass to test memoization.
        """

        def a_method(self):
            """
            Method to be memoized.
            """
            return 42

        @memoize
        def a_property(self):
            """
            Property memoized using memoize decorator.
            """
            return self.a_method()

    @patch.object(TestClass, 'a_method')
    def test_memoize(self, mock_method):
        """
        Test method to test memoization.
        """
        # Create an instance of TestClass
        obj = self.TestClass()

        # Call the memoized property twice
        result1 = obj.a_property()
        result2 = obj.a_property()

        # Assert that the underlying method was called only once
        mock_method.assert_called_once()

        # Assert that the results are correct
        self.assertEqual(result1, 42)
        self.assertEqual(result2, 42)

class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient class to test the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.GithubOrgClient.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test method to test that GithubOrgClient.org returns the correct value.
        """
        # Mock the return value of get_json
        mock_get_json.return_value = {"name": org_name}

        # Create an instance of GithubOrgClient
        github_org_client = GithubOrgClient(org_name)

        # Call the org method
        result = github_org_client.org

        # Assert that get_json was called once with the expected argument
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

        # Assert that the result is correct
        self.assertEqual(result, {"name": org_name})

if __name__ == "__main__":
    unittest.main()
