import sys
import time
import typing

from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.select import Select
from tqdm import tqdm
from models.UserConfig import UserConfig
from utils.utils import parse_game_config

def seamles_login(login: str, password: str, user_name: str) -> UserConfig:
    options = webdriver.ChromeOptions()
    options.add_argument("--host-resolver-rules=MAP vk.com 8.8.8.8")
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(r'D:\chromedriver.exe', options = options)

    driver.get('chrome://settings/content/siteDetails?site=https%3A%2F%2Fdrako.ru')
    logger.debug('Enabling FlashPlayer')
    time.sleep(1)
    actions = ActionChains(driver) 
    actions.send_keys(Keys.TAB * 11)
    actions.send_keys(Keys.DOWN)
    actions.send_keys(Keys.ENTER * 2)
    actions.perform()
    time.sleep(2)
    logger.debug('Enabled')


    driver.get("https://drako.ru/game/main.php")

    logger.debug('Opening main page')
    logger.debug('Wait until loaded')
    
    for i in tqdm(range(15 * 10)):
        time.sleep(0.1)


    logger.debug('Login inserting')
    inputElement = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div/div[2]/div[3]/form/div/fieldset[2]/div/input')
    inputElement.send_keys(login)
    logger.debug('Login inserted')

    logger.debug('Password inserting')
    inputElement = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div/div[2]/div[3]/form/div/fieldset[3]/input')
    inputElement.send_keys(password)
    logger.debug('Password inserted')

    logger.debug('login button searching')
    loginButton = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div/div[2]/div[3]/form/div/fieldset[4]/span/span/span')
    loginButton.click()
    logger.debug('login button clicked')

    time.sleep(2)

    logger.debug('enter game button searching')
    enterGameButton = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div/div[2]/div[3]/form/div/div/div/div/fieldset[1]/div[2]/div/div[2]/div/div')
    enterGameButton.click()
    logger.debug('enter game button clicked')

    logger.debug('wait until main game page loaded')

    for i in tqdm(range(10 * 10)):
        time.sleep(0.1)

    return parse_game_config(driver.page_source)
