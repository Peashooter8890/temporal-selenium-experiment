import pytest
import warnings
from selenium.webdriver.remote.webdriver import WebDriver
from ..driver import Driver

# filter out tarfile deprecation warning
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message="Python 3.14 will, by default, filter extracted tar archives and reject files or modify their metadata.*",
    module="tarfile"
)

class TestDriver:
    @pytest.fixture(params=["chrome", "firefox", "edge"])
    def driver_instance(self, request):
        """Fixture to create a Driver instance for each browser type."""
        return Driver(browser=request.param)

    def test_get_driver(self, driver_instance):
        """Test if get_driver returns a WebDriver instance."""
        driver = driver_instance.get_driver()
        assert isinstance(driver, WebDriver)
        driver.quit()

    def test_invalid_browser(self):
        """Test passing an invalid browser name."""
        with pytest.raises(ValueError):
            Driver(browser='invalid_browser').get_driver()
            
    def test_install_drivers(self):
        """Test if installing drivers raises no exceptions."""
        assert Driver().install_drivers()

    def test_driver_functionality(self, driver_instance):
        """Test if each created driver instance can open the Selenium website and gets its title."""
        driver = driver_instance.get_driver()
        test_url = 'https://www.selenium.dev'
        driver.get(test_url)
        assert driver.title