import os
import time
from os import getcwd
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

chrome_driver = "/home/ubuntu/chromedriver"

browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
browser.get("https://wordpress.com/log-in?redirect_to=https://wordpress.com/wp-login.php?action=jetpack-sso&site_id=144801029&sso_nonce=p8anqpwuxig9jbh24cd1")

username = browser.find_element_by_id('usernameOrEmail')
username.send_keys('varunjain2108@gmail.com')
continue_button = browser.find_element_by_class_name('button form-button is-primary')
continue_button.click()

# quit the browser
browser.quit()