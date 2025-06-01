#!/usr/bin/env python3
"""Module for testing the GithubOrgClient.
"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests the GithubOrgClient class.
    """
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """Tests that org returns the correct organization payload.
        """
        # Configure the mock to return a specific payload
        mock_get_json.return_value = {"login": org_name}

        client = GithubOrgClient(org_name)
        result = client.org

        # Assert that get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(
            client.ORG_URL.format(org=org_name)
        )
        # Assert that the result matches the mocked payload
        self.assertEqual(result, {"login": org_name})

    def test_public_repos_url(self) -> None:
        """Tests that _public_repos_url returns the correct URL.
        """
        expected_url = "https://api.github.com/orgs/testorg/repos"
        # Mock the 'org' property using PropertyMock
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": expected_url}
            client = GithubOrgClient("testorg")
            self.assertEqual(client._public_repos_url, expected_url)

    @patch('client.get_json')
    def test_repos_payload(self, mock_get_json: Mock) -> None:
        """Tests that repos_payload returns the expected JSON.
        """
        # Mock get_json to return a list of repo payloads
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]

        # Mock _public_repos_url property
        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "http://mock.url/repos"

            client = GithubOrgClient("testorg")
            result = client.repos_payload

            # Assert get_json was called with the mocked URL
            mock_get_json.assert_called_once_with("http://mock.url/repos")
            # Assert the result is the mocked payload
            self.assertEqual(result, [{"name": "repo1"}, {"name": "repo2"}])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"no_license": True}, "my_license", False),
        ({}, "my_license", False),
        ({"license": {"key": "bsd-3-clause"}}, "bsd-3-clause", True),
    ])
    def test_has_license(self, repo: Dict, license_key: str, expected: bool) -> None:
        """Tests the has_license static method.
        """
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Performs integration tests for GithubOrgClient.public_repos.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Set up class for integration tests.
        Mocks requests.get to return predefined payloads from fixtures.
        """
        # Mock requests.get globally for the duration of these tests
        # We need to map URLs to specific responses
        cls.get_patcher = patch('requests.get', side_effect=cls.mapped_requests_get)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class after integration tests.
        Stops the mocked requests.get.
        """
        cls.get_patcher.stop()

    @classmethod
    def mapped_requests_get(cls, url: str) -> Mock:
        """Helper to map URLs to fixture data."""
        if url == "https://api.github.com/orgs/google":
            mock_response = Mock()
            mock_response.json.return_value = cls.org_payload
            return mock_response
        elif url == "https://api.github.com/orgs/google/repos":
            mock_response = Mock()
            mock_response.json.return_value = cls.repos_payload
            return mock_response
        else:
            # Fallback for unexpected URLs, though not expected here
            return Mock(json=Mock(return_value={}))

    def test_public_repos(self) -> None:
        """Tests public_repos without a license.
        """
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Tests public_repos with a license.
        """
        client = GithubOrgClient("google")
        # Assuming apache2_repos is a list of names with apache-2.0 license
        # You might need to adjust TEST_PAYLOAD to explicitly provide apache2_repos if not already there
        # For TEST_PAYLOAD as provided, "dagger" has apache-2.0 license
        apache2_repos = [
            repo["name"] for repo in self.repos_payload
            if GithubOrgClient.has_license(repo, "apache-2.0")
        ]
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, apache2_repos)


if __name__ == '__main__':
    unittest.main()