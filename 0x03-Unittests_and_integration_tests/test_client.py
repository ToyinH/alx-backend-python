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

    def test_public_repos_url(self):
        """
        Test method to test the _public_repos_url method of GithubOrgClient.
        """
        # Define a known payload for the org property
        org_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}

        # Patch the org property to return the known payload
        with patch.object(GithubOrgClient, 'org', new_callable=unittest.mock.PropertyMock) as mock_org:
            mock_org.return_value = org_payload

            # Create an instance of GithubOrgClient
            github_org_client = GithubOrgClient("testorg")

            # Call the _public_repos_url method
            result = github_org_client._public_repos_url

            # Assert that the result is the expected repos_url from the mocked payload
            self.assertEqual(result, org_payload["repos_url"])

if __name__ == "__main__":
    unittest.main()

