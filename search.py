"""Functions for searching"""
import sys
from datetime import datetime, timedelta

import requests
from requests.exceptions import ConnectionError


def get_url(code_from, code_to, dep_date, ret_date, trip_type='TT'):
    """a method that calculates url"""
    payload = [(trip_type, 'RT'), ('SS', ''), ('RT', ''), ('FL', 'on'), ('DC', code_from),
               ('AC', code_to), ('AM', dep_date[0:7]), ('AD', dep_date[8:]),
               ('DC', ''), ('AC', ''), ('AM', ''), ('AD', ''), ('DC', ''), ('AC', ''),
               ('AM', ''), ('AD', ''), ('DC', ''), ('AC', ''), ('AM', ''), ('AD', ''),
               ('RM', ret_date[0:7]), ('RD', ret_date[8:]), ('PA', '1'), ('PC', ''),
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


def get_time(path, date, kind='leaving'):
    """a method that is finding the departure/arrive time"""
    time_path = f'.//td[@class="time {kind}"]'
    hours = path.xpath(f'{time_path}/text()')[0]
    result = datetime.strptime(f'{date} {hours}', '%Y-%m-%d %I:%M %p')
    for p in path.xpath(time_path):
        plus_day = p.xpath('.//sup/text()')
        if plus_day:
            result = result + timedelta(days=1)
    return result


def get_duration(start, end):
    """a method that is calculating the duration"""
    duration = end - start
    return duration


def travel_deal(price, category):
    """a method that is checking the availability of travel deal"""
    if price == '':
        return f'{category} travel deal is not available for the given flight.'
    else:
        return price


def get_price(path, letter, category):
    """a method that is finding the price"""
    price = path.xpath('.//td[@class="family family-E' + letter.upper() +
                       ' family-group-Y "]/label/span/text()')
    currency = path.xpath('.//td[@class="family family-E' + letter.upper() +
                          ' family-group-Y "]/label/span' + '/b/text()')
    if len(price) == 0:
        return travel_deal('', category)
    else:
        return travel_deal(f'{price[0]} {currency[0]}', category)


def get_flight_info(path, dt):
    """a method that is combining the flight information"""
    flight_info = []
    for p in path:
        if p.xpath('.//td[@class="time leaving"]/text()'):
            depart = get_time(p, dt)
            arrive = get_time(p, dt, 'landing')
            info = {'depart': depart, 'arrive': arrive,
                    'duration': get_duration(depart, arrive),
                    'discount': get_price(p, 'd', 'discount'),
                    'standard': get_price(p, 's', 'standard'),
                    'premium': get_price(p, 'p', 'premium')}
            flight_info.append(info)
        else:
            no_flights = str(p.xpath('.//td/text()')[0]).strip()
            flight_info.append(no_flights)
    return flight_info


def print_flight_info(info):
    """a method that is presenting the flight information"""
    for i, item in enumerate(info):
        if isinstance(item, dict):
            print('var', i + 1)
            for k in item:
                print(k + ':', item[k])
        else:
            print(info[i])
