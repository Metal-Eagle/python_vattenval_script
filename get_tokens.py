import logging
import argparse
import time
import sys
import os
import json

from seleniumwire import webdriver
from selenium.webdriver.common.by import By

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

parser = argparse.ArgumentParser(
    description="Get usage data from vattenfall.nl using selenium.")
parser.add_argument('-v', '--verbose', action='count')
args = parser.parse_args()

if not args.verbose:
    logger.setLevel(logging.WARNING)
elif args.verbose == 1:
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.DEBUG)

implicit_wait = 20
json_save_location = os.getenv('SAVE_LOCATION')
login2_xpath = "//iam-login-form/div[1]/form/div/button"
cookie_id = "acceptBtn"
username_field_id = "username"
password_field_id = "login_password"
verbruik_xpath = "//vfc-navigation-header/div/div[3]/div/div/div[2]/ul/li[3]/a"
kosten_xpath = "//vf-consumption-tabs-desktop/div/vfc-tab-group/div/div[3]/span[2]"


def api_url_cost_filter(
    x): return 'api.vattenfall' in x.url and '/1/?Interval' in x.url


datefrom_regex = r"(DateFrom=)(.*)(&)"

username = os.getenv('USERNAME_VATTENFALL')
password = os.getenv('PASSWORD_VATTENFALL')
startofsupply = os.getenv('START_OF_SUPPLY')

if username == 'your@ema.il':
    logger.error(f"'username:' not set")
    sys.exit(-1)
logger.info(f'username = {username}')


if password == 'hunter123':
    logger.error(f"'password:' not set")
    sys.exit(-1)


def datefrom_interceptor(request):
    if '/?Interval=' in request.url and 'GetAggregatedResults=false' in request.url:
        logger.info("url is found", request.url)
        authorization = request.headers["authorization"]
        key = request.headers["ocp-apim-subscription-key"]
        parsed_url = request.url.split("/")
        businessPartnerId = parsed_url[8]
        contractAccountId = parsed_url[9]
        with open(f'{json_save_location}tokens.json', 'w', encoding='utf-8') as outfile:
            oneDayInMs = 86400000
            expiresOn = int(time.time()) + oneDayInMs
            json_output = {
                'authorization': authorization,
                'key': key,
                'businessPartnerId': businessPartnerId,
                'contractAccountId': contractAccountId,
                'expiresOn': expiresOn,
            }
            json.dump(json_output, outfile, ensure_ascii=False, indent=4)

def get_token():
    # {json_save_location}tokens.json

    f = open('./exports/tokens.json')
    tokens = json.load(f)

    try:
        expiresOn = tokens["expiresOn"]
        dateNow = int(time.time())
        if expiresOn > dateNow:
            logger.info("Token is still valid")
            return
    except KeyError:
        logger.info("No token file")    
    
    logger.info("Opening webdriver")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    absolute_path = "./assets/chromedriver"
    driver = webdriver.Chrome(
        absolute_path,  options=chrome_options)
    logger.info("Opening setting interceptors")
    driver.request_interceptor = datefrom_interceptor
    try:
        driver.get("https://www.vattenfall.nl/service/mijn-vattenfall/")
        logger.info(f'implicit_wait = {implicit_wait}s')
        driver.implicitly_wait(implicit_wait)
        # TODO: check if exists
        # elem = driver.find_element(By.ID, cookie_id)
        # assert elem.text == 'Ja, ik accepteer cookies'
        # elem.click()
        elem = driver.find_element(By.ID, username_field_id)
        elem.clear()
        elem.send_keys(username)
        elem = driver.find_element(By.ID, password_field_id)
        elem.clear()
        elem.send_keys(password)
        elem = driver.find_element(By.XPATH, login2_xpath)
        assert elem.text == 'Inloggen'
        elem.click()
        logger.info('Successfully logged in')
        time.sleep(5)
        driver.maximize_window()
        elem = driver.find_element(By.XPATH, verbruik_xpath)
        assert elem.text == 'Verbruik'
        elem.click()
        elem = driver.find_element(By.XPATH, kosten_xpath)
        assert elem.text == 'Kosten'
        elem.click()
        # The rest is handled by interceptors, give them some time to complete
        # TODO: wait in a better way
        logger.info('Giving time for the right api call to finish')
        time.sleep(5)
    finally:
        pass
        driver.close()


# Run in debug mode
if args.verbose:
    get_token()