"""Functions for searching"""
from datetime import datetime, timedelta


def get_depart(path):
    """a method that is finding the departure time"""
    depart = path.xpath('.//td[@class="time leaving"]/text()')
    return depart


def get_arrive(path):
    """a method that is finding the arrive time"""
    arrive = path.xpath('.//td[@class="time landing"]/text()')
    return arrive


def get_duration(start, end):
    """a method that is calculating the duration"""
    start_time = datetime.strptime(start[:-3], '%H:%M').time()
    end_time = datetime.strptime(end[:-3], '%H:%M').time()
    duration = timedelta(hours=end_time.hour, minutes=end_time.minute) -\
               timedelta(hours=start_time.hour, minutes=start_time.minute)
    return duration


def travel_deal(price, category):
    """a method that is checking the availability of travel deal"""
    result = ''
    if price == ' ':
        result += f'{category} travel deal is not available for the given flight.'
    else:
        result += price
    return result


def get_price(path, letter, category):
    """a method that is finding the price"""
    price = path.xpath('.//td[@class="family family-E' + letter.upper() +
                       ' family-group-Y "]/label/span/text()')
    currency = path.xpath('.//td[@class="family family-E' + letter.upper() +
                          ' family-group-Y "]/label/span' + '/b/text()')
    result = travel_deal(''.join(price) + ' ' + ''.join(currency), category)
    return result


def get_flight_info(path):
    """a method that is combining the flight information"""
    flight_info = []
    for p in path:
        depart = p.xpath('.//td[@class="time leaving"]/text()')
        if depart:
            arrive = get_arrive(p)[0]
            info = {'depart': depart[0], 'arrive': arrive,
                    'duration': get_duration(depart[0], arrive),
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
