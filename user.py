"""User information"""
import sys
from datetime import datetime, timedelta

import requests
from lxml import html
from requests.exceptions import ConnectionError

URL = 'https://www.airblue.com/'
DESTINATIONS_PATH = '//*[@id="content"]/span[2]/select[1]/option'


def get_destinations(url, path, key='directions'):
    """a method that is finding available destinations"""
    try:
        request = requests.get(url)
    except ConnectionError:
        print('something wrong with your connection')
        sys.exit()
    body = html.fromstring(request.text)
    destinations = {'directions': [], 'iata': []}
    for i in range(2, 12):
        destinations['directions'].append(''.join(body.xpath(f'{path}[{i}]/text()')))
        destinations['iata'].append(''.join(body.xpath(f'{path}[{i}]/@value')))
    return destinations[key]


def check_date(cdate, ddate, ldate, rdate):
    """a method that is checking the date"""
    result = ''
    if ddate < cdate:
        result += 'incorrect date! the departure date cannot be earlier than the current date.'
    elif ddate >= ldate:
        result += 'incorrect date! the departure date cannot be later than the last available date.'
    elif rdate < cdate:
        result += 'incorrect date! the return date cannot be earlier than the current date.'
    elif rdate >= ldate:
        result += 'incorrect date! the return date cannot be later than the last available date.'
    elif ddate > rdate:
        result += 'incorrect date! the return date cannot be earlier than the departure date.'
    return result


def get_user_options():
    """a method that is getting information from user"""

    iata_codes = get_destinations(URL, DESTINATIONS_PATH, 'iata')
    destinations = get_destinations(URL, DESTINATIONS_PATH)

    print('hello! here are the destinations provided by', URL + ':')
    print(' - ' + '\n - '.join(destinations))
    print('\nwhere would you like to go?')
    while True:
        iata_from = input('\nenter the IATA code of the initial airport: ').upper()
        iata_to = input('enter the IATA code of the ultimate airport: ').upper()
        try:
            if iata_from not in iata_codes or iata_to not in iata_codes:
                print('\nincorrect IATA! enter IATA codes again.')
                continue
            current_date = datetime.now().date()
            latest_date = current_date + timedelta(days=183)  # the limitation of website response is a half year
            flight_type = int(input('do you plan a round trip (1) or a one way (2)? (1/2): '))
            if flight_type == 1:
                departure_date = datetime.strptime(input('enter the date of departure ' +
                                                         '(dd-mm-yyyy): '), '%d-%m-%Y').date()
                return_date = datetime.strptime(input('enter the date of return ' +
                                                      '(dd-mm-yyyy): '), '%d-%m-%Y').date()
                check = check_date(current_date, departure_date, latest_date, return_date)
                if check != '':
                    print(check)
                    continue
            elif flight_type == 2:
                departure_date = datetime.strptime(input('enter the date of departure ' +
                                                         '(dd-mm-yyyy): '), '%d-%m-%Y').date()
                return_date = departure_date + timedelta(days=2)
                check = check_date(current_date, departure_date, latest_date, return_date)
                if check != '':
                    print(check)
                    continue
            else:
                print('incorrect value! you must enter 1 or 2.')
                continue
        except ValueError:
            print('incorrect type of flight and/or date! try again.')
            continue
        break
    return iata_from, iata_to, flight_type, departure_date, return_date
