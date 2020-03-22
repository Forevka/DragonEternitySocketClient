import requests
import time

cookies = {
    'account': 'T23f4CeWc7pmTeVm3-fW38y7JBREFp14V0sze9xJ8ac.eyJpZCI6MjY5Njg4ODcsImVtYWlsIjoiemViZXN0Zm9yZXZrYUBnbWFpbC5jb20iLCJzaGFyZHMiOiJydTEiLCJjdGltZSI6MTU4NDczNjk3MSwibG9uZyI6MX0',
    'cid': '5D4BCF747B3C',
    'fbm_101651603250615': 'base_domain=.drako.ru',
    'user': 'rcKhe1w5OvU9w5V-agIUikHjkoIxiRrGFgJHczUJUOM.eyJ1aWQiOjIxMTI4MTAxLCJndWVzdERhdGEiOiIiLCJjdGltZSI6MTU4NDkwMDY2MCwibG9uZyI6MX0',
    'fbsr_101651603250615': 'mJVlZHy3hdwBxO3KcSEsG7gWF8nXwIzx0vM9s99d6KQ.eyJ1c2VyX2lkIjoiMTAwMDA3OTM0NzQ0OTg1IiwiY29kZSI6IkFRQjRUM3MzRGdYUUg0X21xUkU4MjQ4cWpSU3FtQ0JKdDNyRF9kR0tVRXdibVJFXzdrb1hnLWhsb1pBc0FodVlweXlzXzdrd0tobm44NFdzZmlKckxhM1B1QXdRRHktNDNDVXhiNUZQSU00RG1PNkZPenQ4ODd0S19iVmZMTFZIWGdmNl9NUXNGeG95TzdOSjF2azk0aEtodDhOdWZBVDltRUcyOGVqbG9BZlg5ZDBxNVlrYWxfTHlnRURUUmpWblBEQ0hpQnpJZDBYRFcwTVhNNldlQlVoNXRJTGFJaUtQWGg0bjhVdllfRV9NU3NmZ1BwSVhoMXZ2c3U0ZGI4MUNHRFFiTzdtZXRlMXpjd1RCSHMtNDR3OVh0cUVVMmh3cVVFNnZOeXFDZnltX0pFeTQ2MUZMWXVmaWxPdFNBTm1aVy0tRUlVZlZ4cFM5WlpQSm4yalVqbHl2Iiwib2F1dGhfdG9rZW4iOiJFQUFCY2M1dXozYmNCQU5VaVN3T3JNSjRjV2RDZzVHTmFwSTlvSDBkczlKY1ZJS0pSVHRSMkV4Y3ZRZFNodFRZTjFuOWZrME5lOXFPY2RvWU1jcVJuaTFkSW5NQlQzdFdUSmtwanV1TjVzSXhkbVpCNWpURGtpT0FaQnNWNG1tS1U5SEQ1MFdKWTVSNVNhOXNzN3JzekppOVZIamkyNHpmRHhnSEFXMnF6eDhFRlhXWkFzYnZBUGpta3h6T003WkJQWkM2NlZ4dlRJOEFaRFpEIiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE1ODQ5MDM5NDd9',
    'sess': 'mal5rohktm5b0heo71migihih6',
    'domain': 'drako.ru',
}

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Sec-Fetch-Dest': 'document',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Referer': 'https://drako.ru/game/main.php',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6,pl;q=0.5,fr;q=0.4,es;q=0.3',
}

#response = requests.get('https://drako.ru/game/main.php', headers=headers, cookies=cookies)
#print(response.text)
#print(response.text)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

LOGIN = "zebestforevka@gmail.com"
PASSWORD = "werdwerd"


options = webdriver.ChromeOptions()
options.add_argument("--host-resolver-rules=MAP vk.com 127.0.0.1")
options.add_argument("--disable-features=EnableEphemeralFlashPermission")

driver = webdriver.Chrome(r'D:\chromedriver.exe', options = options)
driver.get("https://drako.ru/game/main.php")
time.sleep(30)
inputElement = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div/div[2]/div[3]/form/div/fieldset[2]/div/input')
inputElement.send_keys(LOGIN)

inputElement = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div/div[2]/div[3]/form/div/fieldset[3]/input')
inputElement.send_keys(PASSWORD)

loginButton = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div/div[2]/div[3]/form/div/fieldset[4]/span/span/span')
loginButton.click()

time.sleep(5)

enterGameButton = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div/div[2]/div[3]/form/div/div/div/div/fieldset[1]/div[2]/div/div[2]/div/div')
enterGameButton.click()
#driver.add_cookie({})
while True:
    time.sleep(100)