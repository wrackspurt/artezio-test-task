"""User information"""
import sys
from datetime import datetime
import requests
from lxml import html

URL = 'https://www.airblue.com/'
PATH = '//*[@id="content"]/span[2]/select[1]/option'


def get_destinations(url, path, key='directions'):
    """a method that is finding available destinations"""
    try:
        request = requests.get(url)
    except ConnectionError as i:
        print(i)
        request = 'no response'
        sys.exit()
    body = html.fromstring(request.text)
    destinations = {'directions': [], 'iata': []}
    for i in range(2, 12):
        destinations['directions'].append(''.join(body.xpath(f'{path}[{i}]/text()')))
        destinations['iata'].append(''.join(body.xpath(f'{path}[{i}]/@value')))
    return destinations[key]


IATA_CODES = get_destinations(URL, PATH, 'iata')
DESTINATIONS = get_destinations(URL, PATH)


def user():
    """a method that is getting information from user"""
    print('hello! here are the destinations provided by', URL + ':')
    print(' - ' + '\n - '.join(DESTINATIONS))
    print('\nwhere would you like to go?')
    while True:
        iata_from = input('\nenter the IATA code of the initial airport: ').upper()
        iata_to = input('enter the IATA code of the ultimate airport: ').upper()
        try:
            if iata_from not in IATA_CODES or iata_to not in IATA_CODES:
                print('\nincorrect IATA! enter IATA codes again.')
                continue
            current_date = datetime.now().date()
            return_date = ''
            flight_type = int(input('do you plan a round trip (1) or a one way (2)? (1/2): '))
            if flight_type == 1:
                departure_date = datetime.strptime(input('enter the date of departure ' +
                                                         '(dd-mm-yyyy): '), '%d-%m-%Y').date()
                return_date = datetime.strptime(input('enter the date of return ' +
                                                      '(dd-mm-yyyy): '), '%d-%m-%Y').date()
                if departure_date < current_date or return_date < current_date or \
                        departure_date > return_date:
                    print('\nincorrect date! enter the flight information again.')
                    continue
            elif flight_type == 2:
                departure_date = datetime.strptime(input('enter the date of departure ' +
                                                         '(dd-mm-yyyy): '), '%d-%m-%Y').date()
                if departure_date < current_date:
                    print('\nincorrect date! enter the flight information again.')
                    continue
            else:
                raise UnboundLocalError
        except ValueError:
            print('incorrect type of flight and/or date! try again.')
            continue
        except UnboundLocalError:
            print('you must enter only 1 or 2! try again.')
            continue
        break
    return iata_from, iata_to, str(departure_date), str(return_date)
