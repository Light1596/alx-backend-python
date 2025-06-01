#!/usr/bin/env python3
"""Module for testing utils functions.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests the access_nested_map function.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ({"a": {"b": {"c": 3}}}, ("a", "b", "c"), 3),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: any) -> None:
        """Tests that access_nested_map returns the expected result.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map: dict, path: tuple, exception: Exception) -> None:
        """Tests that access_nested_map raises the expected exception.
        """
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests the get_json function.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"status": "ok"}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url: str, test_payload: dict, mock_requests_get: Mock) -> None:
        """Tests that get_json returns the expected JSON.
        """
        # Configure the mock to return a mock response object
        # which itself returns test_payload when .json() is called
        mock_requests_get.return_value.json.return_value = test_payload

        result = get_json(test_url)

        # Assert that requests.get was called exactly once with the test_url
        mock_requests_get.assert_called_once_with(test_url)

        # Assert that the result is the expected payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Tests the memoize decorator.
    """
    def test_memoize(self) -> None:
        """Tests that a_method is called only once when memoized.
        """
        class TestClass:
            """A class to test memoization."""
            def a_method(self) -> int:
                """A test method."""
                return 42

            @memoize
            def a_property(self) -> int:
                """A test property."""
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_a_method:
            test_instance = TestClass()

            # Access the memoized property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Assert that a_method was called only once
            mock_a_method.assert_called_once()

            # Assert that the results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)


if __name__ == '__main__':
    unittest.main()
