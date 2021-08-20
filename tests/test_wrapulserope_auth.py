from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
import pytest
import wrapulserope


LOGIN_URL = 'https://www.wrapulserope.online/access/login'

@pytest.mark.get_login_button
def test_correct_button_path():
    with webdriver.Chrome(executable_path=wrapulserope.drive_path) as driver:
        driver.get(wrapulserope.URL)
        button = wrapulserope.get_login_button(driver, wrapulserope.login_button_path)
        assert button


@pytest.mark.get_login_button
def test_uncorrect_button_path():
    with webdriver.Chrome(executable_path=wrapulserope.drive_path) as driver:
        driver.get(wrapulserope.URL)
        try:
            button = wrapulserope.get_login_button(driver, 'qsdgdfgd')
        except exceptions.NoSuchElementException as er:
            assert 'Message: no such element:' in str(er)


@pytest.mark.click_login_button
def test_correct_click():
    with webdriver.Chrome(executable_path=wrapulserope.drive_path) as driver:
        driver.get(wrapulserope.URL)
        button = wrapulserope.get_login_button(driver, wrapulserope.login_button_path)
        wrapulserope.click_login_button(button)
        assert driver.current_url == LOGIN_URL


@pytest.mark.get_login_fields
def test_fields_correct_url():
    with webdriver.Chrome(executable_path=wrapulserope.drive_path) as driver:
        driver.get(LOGIN_URL)
        fields = wrapulserope.get_login_fields(driver)
        assert fields['Логин'] and fields['Пароль'] and fields['Войти']


@pytest.mark.get_login_fields
def test_fields_uncorrect_url():
    with webdriver.Chrome(executable_path=wrapulserope.drive_path) as driver:
        driver.get('https://github.com/')
        try:
            fields = wrapulserope.get_login_fields(driver)
        except exceptions.NoSuchElementException as er:
            assert 'no such element' in str(er)


@pytest.mark.user_login
def test_success_user_login():
    with webdriver.Chrome(executable_path=wrapulserope.drive_path) as driver:
        driver.get(LOGIN_URL)
        fields = wrapulserope.get_login_fields(driver)
        wrapulserope.user_login(fields, wrapulserope.USER_INFO)
        assert wrapulserope.USER_INFO['Логин'] in driver.page_source and 'Войти' not in driver.page_source
        assert driver.current_url == 'https://www.wrapulserope.online/'


@pytest.mark.user_login
def test_failed_user_login():
    user = {
    'Логин': 'Usernam',
    'Пароль': 'pasqwert'
}
    with webdriver.Chrome(executable_path=wrapulserope.drive_path) as driver:
        driver.get(LOGIN_URL)
        fields = wrapulserope.get_login_fields(driver)
        wrapulserope.user_login(fields, user)
        assert 'Пожалуйста, введите правильные имя пользователя и пароль.' in driver.page_source
        assert driver.current_url == LOGIN_URL