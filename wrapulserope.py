# на правах рекламы. Тест авторизации на собственном сайте (делал в мае)
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

URL = 'https://www.wrapulserope.online/'
drive_path = 'D:\\downloads\\chromedriver_win32\\chromedriver.exe'  # путь к драйверу (придется установить)
login_button_path = 'html/body/header/div/div/div/a'
USER_INFO = {
    'Логин': 'Username',
    'Пароль': 'pasqwert'
}


def get_login_button(driver, login_button_path):
    return driver.find_element_by_xpath(login_button_path)


def click_login_button(button):
    button.send_keys(Keys.ENTER)


def get_login_fields(driver):
    login_input = driver.find_element_by_name('username')
    password_input = driver.find_element_by_name('password')
    submit = driver.find_element_by_css_selector('form button')
    return {
        'Логин': login_input,
        'Пароль': password_input,
        'Войти': submit
    }


def user_login(login_fields, user=USER_INFO):
    login_fields['Логин'].send_keys(user['Логин'])
    login_fields['Пароль'].send_keys(user['Пароль'])
    login_fields['Войти'].send_keys(Keys.ENTER)


if __name__ == "__main__":
    driver = webdriver.Chrome(executable_path=drive_path)  # хватит только хрома
    driver.get(URL)
    button = get_login_button(driver, login_button_path)
    click_login_button(button)
    login_fields = get_login_fields(driver)
    user_login(login_fields, USER_INFO)
    driver.quit()
