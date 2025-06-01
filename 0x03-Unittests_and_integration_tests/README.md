# 0x02. Python - Unit Tests

This project focuses on understanding and implementing unit and integration tests in Python using the `unittest` framework and the `unittest.mock` library. It covers key testing concepts such as mocking, parametrizations, and fixtures.

## Learning Objectives

- Understand the fundamental differences between unit tests and integration tests.
- Learn how to use `unittest` for writing tests.
- Master the art of mocking external dependencies using `unittest.mock`.
- Explore common testing patterns like parametrization and the use of fixtures.

## Project Structure

- `utils.py`: Contains generic utility functions used by the `GithubOrgClient`.
- `client.py`: Implements a GitHub organization client that interacts with the GitHub API.
- `fixtures.py`: Provides test data (payloads) for testing.
- `test_utils.py`: Unit tests for functions in `utils.py`.
- `test_client.py`: Unit and integration tests for the `GithubOrgClient` class in `client.py`.
