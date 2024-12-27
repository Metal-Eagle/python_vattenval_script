import logging
import argparse
import time
import sys
import os
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs

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
login2_xpath = "//iam-login-main-form/div[1]/form/div/button"


#//*[@id="loginForm"]/div/button

cookie_id = "acceptBtn"
username_field_id = "email-input"
password_field_id = "login_password"

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
    if '/api/v1/yearlybills' in request.url:
        logger.info("url is found", request.url)
        authorization = request.headers["authorization"]
        key = request.headers["ocp-apim-subscription-key"]
        parsed_url = urlparse(request.url)

        # Get you contractAccountId and businessPartnerId form url
        businessPartnerId = parse_qs(parsed_url.query)['businessPartnerId'][0]
        contractAccountId = parse_qs(parsed_url.query)['contractAccountId'][0]
        with open(f'{json_save_location}tokens.json', 'w', encoding='utf-8') as outfile:
            oneHourInMS = 3600000  # Adjust when necessary
            expiresOn = int(time.time()) + oneHourInMS
            json_output = {
                'authorization': authorization,
                'key': key,
                'businessPartnerId': businessPartnerId,
                'contractAccountId': contractAccountId,
                'expiresOn': expiresOn,
            }
            logger.info(json_output)
            json.dump(json_output, outfile, ensure_ascii=False, indent=4)


def get_token():
    # {json_save_location}tokens.json

    try:
        with open('./exports/tokens.json') as f:
            tokens = json.load(f)
            expiresOn = tokens["expiresOn"]
            dateNow = int(time.time())

            logger.info(f'expiresOn: {expiresOn} dateNow: {dateNow} total: {expiresOn - dateNow < 0}')

            if expiresOn - dateNow > 0:
                logger.info("Token is still valid")
                return
    except (KeyError, FileNotFoundError):
        logger.info("No valid token file found, proceeding with login")

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
        # The rest is handled by interceptors, give them some time to complete
        # TODO: wait in a better way
        logger.info('Giving time for the right api call to finish')
        time.sleep(60)
    finally:
        pass
        driver.close()


# Run in debug mode
if args.verbose:
    get_token()
