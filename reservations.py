"""Flight Selection"""
from datetime import datetime
import sys
import requests
from lxml import html
from requests.exceptions import ConnectionError
from user import get_user_options
from search import get_flight_info, print_flight_info

iata_from, iata_to, flights_type, departure_date, return_date = get_user_options()
ddate = str(datetime.strptime(departure_date, "%Y-%m-%d").date().strftime("%Y_%m_%d"))
rdate = str(datetime.strptime(return_date, "%Y-%m-%d").date().strftime("%Y_%m_%d"))


def get_url(trip_type='TT'):
    """a method that calculates url"""
    payload = [(trip_type, 'RT'), ('SS', ''), ('RT', ''), ('FL', 'on'), ('DC', iata_from),
               ('AC', iata_to), ('AM', departure_date[0:7]), ('AD', departure_date[8:]),
               ('DC', ''), ('AC', ''), ('AM', ''), ('AD', ''), ('DC', ''), ('AC', ''),
               ('AM', ''), ('AD', ''), ('DC', ''), ('AC', ''), ('AM', ''), ('AD', ''),
               ('RM', return_date[0:7]), ('RD', return_date[8:]), ('PA', '1'), ('PC', ''),
               ('PI', ''), ('CC', ''), ('NS', ''), ('CD', '')]
    if trip_type == 'OW':
        payload.insert(0, ('TT', trip_type))
    try:
        response = requests.get('https://www.airblue.com/bookings/flight_selection.aspx',
                                params=payload)
        return response
    except ConnectionError:
        print('something wrong with your connection')
        sys.exit()


def find_flights():
    """a method that is providing information about flights"""
    print('\nsearch results: ')
    if flights_type == 1:
        body = html.fromstring(get_url().text)
        print('\nthere: ')
        print_flight_info(get_flight_info(body.xpath(f'//table[@id="trip_1_date_{ddate}"]' +
                                                     '/tbody/tr')))
        print('\nback: ')
        print_flight_info(get_flight_info(body.xpath(f'//table[@id="trip_2_date_{rdate}"]/' +
                                                     'tbody/tr')))
    elif flights_type == 2:
        body = html.fromstring(get_url('OW').text)
        print_flight_info(get_flight_info(body.xpath(f'//table[@id="trip_1_date_{ddate}"]' +
                                                     '/tbody/tr')))
