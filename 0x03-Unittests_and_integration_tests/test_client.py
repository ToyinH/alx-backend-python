#!/usr/bin/env python3

"""
This module contains unit tests for client.GithubOrgClient class.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient

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
