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
    

    @patch('client.GithubOrgClient.get_json')
    @patch.object(GithubOrgClient, '_public_repos_url', new_callable=unittest.mock.PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Test method to test the public_repos method of GithubOrgClient.
        """
        # Define a payload for get_json
        get_json_payload = [{"name": "repo1"}, {"name": "repo2"}, {"name": "repo3"}]

        # Define a value for _public_repos_url
        public_repos_url_value = "https://api.github.com/orgs/testorg/repos"

        # Mock the return value of get_json
        mock_get_json.return_value = get_json_payload

        # Mock the return value of _public_repos_url
        mock_public_repos_url.return_value = public_repos_url_value

        # Create an instance of GithubOrgClient
        github_org_client = GithubOrgClient("testorg")

        # Call the public_repos method
        result = github_org_client.public_repos()

        # Assert that the result is equal to the expected payload
        self.assertEqual(result, [repo['name'] for repo in get_json_payload])

        # Assert that _public_repos_url property was called once
        mock_public_repos_url.assert_called_once()

        # Assert that get_json was called once with the correct argument
        mock_get_json.assert_called_once_with(public_repos_url_value)

    def test_public_repos_with_license(self):
        """
        Test method to test the public_repos_with_license method of GithubOrgClient.
        """
        # Define fixture data for _public_repos_url
        public_repos_fixture = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None}
        ]

        # Patch the _public_repos_url property to return the fixture data
        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=unittest.mock.PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = public_repos_fixture

            # Create an instance of GithubOrgClient
            github_org_client = GithubOrgClient("testorg")

            # Call the public_repos_with_license method with license="apache-2.0"
            result = github_org_client.public_repos_with_license("apache-2.0")

            # Assert that the result is equal to the expected fixture data filtered by license
            self.assertEqual(result, ["repo2"])


if __name__ == "__main__":
    unittest.main()

