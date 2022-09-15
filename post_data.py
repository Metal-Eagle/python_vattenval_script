import requests
import logging
import argparse
import json
import os
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

base_url = os.getenv('API_URL')
api_user = os.getenv('API_USERNAME')
api_password = os.getenv('API_PASSWORD')




def post_hours():
    f = open('./exports/consumption_hours.json')
    jsonFile = json.load(f)
    url = base_url + "/hours"

    x = requests.post(url, json=jsonFile, auth=(api_user, api_password))
    logger.info(x.text)


def post_months():
    f = open('./exports/consumption_months.json')
    jsonFile = json.load(f)
    url = base_url + "/months"

    x = requests.post(url, json=jsonFile, auth=(api_user, api_password))
    logger.info(x.text)


def post_days():
    f = open('./exports/consumption_days.json')
    jsonFile = json.load(f)
    url = base_url + "/days"

    x = requests.post(url, json=jsonFile, auth=(api_user, api_password))
    logger.info(x.text)


if args.verbose:
    post_hours()
    post_months()
    post_days()
