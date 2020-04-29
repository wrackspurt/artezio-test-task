"""Flight Selection"""
from datetime import datetime

from lxml import html

from user import get_user_options
from search import get_url, get_flight_info, print_flight_info


def find_flights():
    """a method that is providing information about flights"""
    iata_from, iata_to, flights_type, departure_date, return_date = get_user_options()
    ddate = str(datetime.strptime(departure_date, "%Y-%m-%d").date().strftime("%Y_%m_%d"))
    rdate = str(datetime.strptime(return_date, "%Y-%m-%d").date().strftime("%Y_%m_%d"))
    print('\nsearch results: ')
    if flights_type == 1:
        body = html.fromstring(get_url(iata_from, iata_to, departure_date, return_date).text)
        print('\nthere: ')
        print_flight_info(get_flight_info(body.xpath(f'//table[@id="trip_1_date_{ddate}"]' +
                                                     '/tbody/tr'), departure_date))
        print('\nback: ')
        print_flight_info(get_flight_info(body.xpath(f'//table[@id="trip_2_date_{rdate}"]/' +
                                                     'tbody/tr'), return_date))
    elif flights_type == 2:
        body = html.fromstring(get_url(iata_from, iata_to, departure_date, return_date,
                                       trip_type='OW').text)
        print_flight_info(get_flight_info(body.xpath(f'//table[@id="trip_1_date_{ddate}"]' +
                                                     '/tbody/tr'), departure_date))
