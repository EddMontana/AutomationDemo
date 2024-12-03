# automation-demo

This project is a mobile test automation suite for an Android application using Appium and pytest.
The tests cover login and filtering capabilities of the SwagLabs application.

## Project Structure

## Requirements

- Python 3.10
- Appium
- Android SDK

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/EddMontana/AutomationDemo.git 
    cd to AutomationDemo
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements
    ```

3. Ensure you have Appium installed and running:
    ```sh
    npm install -g appium
    appium
    ```

## Configuration

The pytest can be configured via the `pytest.ini` file 

## Running Tests
To run the tests, use the following commands
    to run the full test suite:
        pytest
    to run a speciffic test:
        pytest tests/tests/test_1_login.py
        pytest tests/tests/test_2_filter_accuracy.py

## Test Structure
Login Tests
Located in tests/test_1_login.py
These tests verify the login functionality with both correct and incorrect credentials.

Filter Accuracy Tests
Located in tests/test_2_filter_accuracy.py 
These tests verify that the product filtering functionality works as expected.

## Page Objects
The page objects are located in the pages directory and include:

pages/page.py: Base page class.
pages/login_page.py: Login page class.
pages/main_page.py: Main page class.
Logging and Reporting
Logs are saved in the logging/logs directory, and screenshots of failed tests are saved in the logging/screenshots directory. An HTML report is generated as report.html.

## License
MIT License
This is an open project, do with it as you please