# Contributing Guidelines

Thank you for considering contributing to our project! Please follow these guidelines to make the contribution process easy and effective.

## Prerequisites

Before getting started, please ensure that you have the following software installed on your machine:

- Python (version 3.8 or higher)
- Git

## Getting Started

1. Fork the repository and clone it to your local machine: `git clone https://github.com/your-username/repo-name.git`.
2. Install the development dependencies: `pip install -r requirements.txt`.
3. Create a new branch for your changes: `git checkout -b my-feature-branch`.
4. Make your changes and ensure that your code is well-documented and formatted properly.
5. Run the tests locally by running `pytest`.
6. Commit your changes: `git commit -m "Add some feature"`.
7. Push to the branch: `git push origin my-feature-branch`.
8. Create a new pull request.

## Code Style

We follow the coding style guidelines for Python provided by the PEP 8 style guide. Please ensure that your code adheres to this standard before submitting a pull request. You can use a linter like Flake8 to check your code for compliance with the style guide.

## Testing

Please ensure that your changes include unit tests and integration tests as applicable. You can run the tests locally by running `pytest` from the project root directory. Additionally, you can check the code coverage by running `coverage run -m pytest` followed by `coverage report`.

Before opening a pull request, please make sure to:

- Run the linter to ensure your code adheres to the style guide: `flake8`.
- Run the tests and ensure that they all pass: `pytest`.

We appreciate your contributions to our project and look forward to reviewing your pull requests! Please add tests for any new features you introduce.
