import requests
import os
import json
import datetime
import calendar
import logging
import argparse
import os


from dotenv import load_dotenv

load_dotenv()
json_save_location = os.getenv('SAVE_LOCATION')

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


def hours_data():
    logger.info("Get hours data")
    f = open('./exports/tokens.json')
    tokens = json.load(f)

    currentDate = datetime.datetime.now()
    startDate = currentDate - datetime.timedelta(days=currentDate.weekday())
    endDate = startDate + datetime.timedelta(days=6)

    url = "https://api.vattenfall.nl/api/mijnnuonprd/v2/consumptions/consumptions/" + \
        tokens['businessPartnerId'] + "/" + tokens["contractAccountId"] + \
        "/5/?Interval=5&GetAggregatedResults=false&GetAmountDetails=false&GetAmounts=true&GetRoundedAmounts=false&GetComparedConsumption=false&DateFrom={}&DateTo={}".format(
            startDate.strftime('%Y-%m-%d'), endDate.strftime('%Y-%m-%d'))


    headers = {
        'ocp-apim-subscription-key': tokens['key'],
        'authorization': tokens['authorization'],
        'authority': 'api.vattenfall.nl',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'nl,en;q=0.9,nl-NL;q=0.8,en-US;q=0.7',
        'cache-control': 'no-cache',
        'origin': 'https://www.vattenfall.nl',
        'pragma': 'no-cache',
        'referer': 'https://www.vattenfall.nl/',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    resp = requests.get(url=url,  headers=headers)
    data = resp.json()
    # extracting data in json format
    with open(f'{json_save_location}consumption_hours.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)


def months_data():
    logger.info("Get months data")
    f = open('./exports/tokens.json')
    tokens = json.load(f)

    currentDate = datetime.datetime.now()
    startDate = currentDate.strftime('%Y-01-01')
    endDate = datetime.date(currentDate.year, 12, calendar.monthrange(
        currentDate.year, currentDate.month)[1])

    url = "https://api.vattenfall.nl/api/mijnnuonprd/v2/consumptions/consumptions/" + \
        tokens['businessPartnerId'] + "/" + tokens["contractAccountId"] + \
        "/1/?Interval=1&GetAggregatedResults=false&GetAmountDetails=false&GetAmounts=true&GetRoundedAmounts=false&GetComparedConsumption=false&DateFrom={}&DateTo={}".format(
            startDate, endDate)

    headers = {
        'ocp-apim-subscription-key': tokens['key'],
        'authorization': tokens['authorization'],
        'authority': 'api.vattenfall.nl',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'nl,en;q=0.9,nl-NL;q=0.8,en-US;q=0.7',
        'cache-control': 'no-cache',
        'origin': 'https://www.vattenfall.nl',
        'pragma': 'no-cache',
        'referer': 'https://www.vattenfall.nl/',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    resp = requests.get(url=url,  headers=headers)
    data = resp.json()
    # extracting data in json format
    with open(f'{json_save_location}consumption_months.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)


def days_data():
    logger.info("Get days data")
    f = open('./exports/tokens.json')
    tokens = json.load(f)

    currentDate = datetime.datetime.now()
    startDate = currentDate.strftime('%Y-%m-01')  # "2022-09-01"
    endDate = datetime.date(currentDate.year, currentDate.month, calendar.monthrange(
        currentDate.year, currentDate.month)[1])  # "2022-09-30"
    url = "https://api.vattenfall.nl/api/mijnnuonprd/v2/consumptions/consumptions/" + \
        tokens['businessPartnerId'] + "/" + tokens["contractAccountId"] + \
        "/3/?Interval=3&GetAggregatedResults=false&GetAmountDetails=false&GetAmounts=true&GetRoundedAmounts=false&GetComparedConsumption=false&DateFrom={}&DateTo={}".format(
            startDate, endDate)

    headers = {
        'ocp-apim-subscription-key': tokens['key'],
        'authorization': tokens['authorization'],
        'authority': 'api.vattenfall.nl',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'nl,en;q=0.9,nl-NL;q=0.8,en-US;q=0.7',
        'cache-control': 'no-cache',
        'origin': 'https://www.vattenfall.nl',
        'pragma': 'no-cache',
        'referer': 'https://www.vattenfall.nl/',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    resp = requests.get(url=url,  headers=headers)
    data = resp.json()
    # extracting data in json format
    with open(f'{json_save_location}consumption_days.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

# only on debug run
if args.verbose:
    days_data()
    hours_data()
    months_data()
