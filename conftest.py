import pytest
import logging
import os
from appium import webdriver
from appium.options.common import AppiumOptions
import datetime
import subprocess

path = os.path.dirname(os.path.abspath(__file__))

def get_device_info():
    """
    Get the connected device information.
    """
    logger = logging.getLogger("device_info")
    raw_output = subprocess.check_output("adb devices", shell=True).decode().strip()
    device_info = {}
    devices = [line.split()[0] for line in raw_output.splitlines() if "device" in line and "List" not in line]
    if not devices:
        logger.error("No devices connected")
    else:
        for device in devices:
            command = f"adb -s {device} shell getprop ro.build.version.release"
            version = subprocess.check_output(command, shell=True).decode().strip() # Get the Android version by calling the adb shell command
            if "emulator" in device:
                device_info["emulated"] = (device, version)
            else:
                device_info["physical"] = (device, version)
    return device_info

info = get_device_info()

@pytest.fixture(scope="function")
def driver():
    """
    Initialize the Appium driver.
    Select the physical device if available, otherwise use the emulated device.
    """

    if "physical" in info:    # Use physical device if available
        desired_caps = {
            "platformName": "Android",
            "platformVersion": info["physical"][1],
            "deviceName": info["physical"][0],
            "appium:appPackage": "com.swaglabsmobileapp",
            "appium:appActivity": "com.swaglabsmobileapp.MainActivity",
            "automationName": "UiAutomator2",
            "noReset": False
        }
    else:   # Use emulated device if no physical device is available
        desired_caps = {
            "platformName": "Android",
            "platformVersion": info["emulated"][1],
            "deviceName": info["emulated"][0],
            "appium:appPackage": "com.swaglabsmobileapp",
            "appium:appActivity": "com.swaglabsmobileapp.MainActivity",
            "app": fr"{path}\apks\Android.SauceLabs.Mobile.Sample.app.2.7.1.apk",
            "automationName": "UiAutomator2",
            "noReset": False
        }

    # Start the Appium driver
    driver = webdriver.Remote('http://localhost:4723', options=AppiumOptions().load_capabilities(desired_caps))

    yield driver

    # End the session
    driver.quit()


# Hook to capture screenshots on failure
@pytest.hookimpl()
def reporting(item):
    """
    Hook to capture screenshots on failure.
    """
    outcome = yield
    report = outcome.get_result()
    logger = logging.getLogger("logger")
    logger.info(f"Test {item.name} finished with the following outcome: {report.outcome}")

    if report.outcome == "failed":
        logger.error(f"Test failed at {item.name} with error: {report.longrepr}")
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")  # Access driver from test function args
        if driver: #if driver is correctly returned
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            screenshot_path = f"debug/screenshots/{item.name}_{timestamp}.png" 

            driver.save_screenshot(screenshot_path)
            pytest.fail(f"Test failed. Screenshot saved to {screenshot_path}", pytrace=False)
