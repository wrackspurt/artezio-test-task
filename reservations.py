"""Flight Selection"""
import requests
from lxml import html
from user import user
from search import get_flight_info, print_flight_info

IATA_FROM, IATA_TO, DEPARTURE_DATE, RETURN_DATE = user()
DDATE = f'{DEPARTURE_DATE[0:4]}_{DEPARTURE_DATE[5:7]}_{DEPARTURE_DATE[8:]}'
RDATE = f'{RETURN_DATE[0:4]}_{RETURN_DATE[5:7]}_{RETURN_DATE[8:]}'
ROUND_TRIP_URL = 'https://www.airblue.com/bookings/flight_selection.aspx?TT=RT&SS=&RT=&FL=on&DC=' +\
                 IATA_FROM + '&AC=' + IATA_TO + '&AM=' + DEPARTURE_DATE[0:7] + '&AD=' +\
                 DEPARTURE_DATE[8:] + '&DC=&AC=&AM=&AD=&DC=&AC=&AM=&AD=&DC=&AC=&AM=&AD=&RM=' +\
                 RETURN_DATE[0:7] + '&RD=' + RETURN_DATE[8:] + '&PA=1&PC=&PI=&CC=&NS=&CD='
ONE_WAY_URL = 'https://www.airblue.com/bookings/flight_selection.aspx?TT=OW&SS=&RT=&FL=on&DC=' +\
              IATA_FROM + '&AC=' + IATA_TO + '&AM=' + DEPARTURE_DATE[0:7] + '&AD=' +\
              DEPARTURE_DATE[8:] + '&DC=&AC=&AM=&AD=&DC=&AC=&AM=&AD=&DC=&AC=&AM=&AD=&RM=' +\
              RETURN_DATE[0:7] + '&RD=' + RETURN_DATE[8:] + '&PA=1&PC=&PI=&CC=&NS=&CD='


def find_flights():
    """a method that is providing information about flights"""
    try:
        print('\nsearch results: ')
        if RETURN_DATE == '':
            request = requests.get(ONE_WAY_URL)
            body = html.fromstring(request.text)
            print_flight_info(get_flight_info(body.xpath(f'//table[@id="trip_1_date_{DDATE}"]' +
                                                         '/tbody/tr')))
        else:
            request = requests.get(ROUND_TRIP_URL)
            body = html.fromstring(request.text)
            print('\nthere: ')
            print_flight_info(get_flight_info(body.xpath(f'//table[@id="trip_1_date_{DDATE}"]' +
                                                         '/tbody/tr')))
            print('\nback: ')
            print_flight_info(get_flight_info(body.xpath(f'//table[@id="trip_2_date_{RDATE}"]/' +
                                                         'tbody/tr')))
    except ConnectionError:
        print('something wrong with your connection')
