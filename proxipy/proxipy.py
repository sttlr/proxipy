#!/usr/bin/env python

import requests
import logging
import re

from functools import wraps
from typing import Callable, Union


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s:'
                                  '%(funcName)s > %(message)s',
                              datefmt='%d/%m %I:%M:%S')

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger.addHandler(handler)


def return_dict(func: Callable) -> Callable:

    @wraps(func)
    def wrapper(*args, **kwargs) -> Union[dict, tuple]:
        proxies = func(*args, **kwargs).get_proxies()

        if kwargs.get('limit', 1) > 1:
            proxies_tuple = ()
            for prox in proxies:
                proxies_tuple += (dict(http=prox, https=prox),)
            return proxies_tuple
        else:
            return dict(http=proxies[0], https=proxies[0])

    return wrapper


@return_dict
class proxipy:
    '''Need proxy? Catch it.

       :param type_: Can be ``http``, ``socks4`` or ``socks5``.
       :param https: Apply HTTPS.
       :param last_check: (in minutes) Display proxies that are verified no later than given amount of time.
       :param limit: Amount of proxies to return (no more than 20 proxies per request).
       :param country: String of countries *(2 char code - like 'US')* separated by commas.
       :param port: Apply given port.
       :param \*\*kwargs: Optional arguments that you don't really need.
       :returns: ``dict`` if 1 proxy, ``tuple`` of proxies if more.

       :raises: :class:`WrongConnType`, if ``type_`` param is not "http" or "socks4" or "socks5".
       :raises: :class:`ReachedLimit`, if ``limit`` param less than 1 or more than 20.
       :raises: :class:`WrongCountryCode`, if ``country`` param is not 2 symbol code.
       :raises: :class:`WrongPort`, if ``port`` param < 1 or > 65535.

       Usage:

       .. doctest::

            >>> from proxipy import proxipy
            >>> import requests
            >>> prox = proxipy()
            >>> prox  # doctest: +ELLIPSIS
            {'http': ..., 'https': ...}
            >>> req = requests.get('http://httpbin.org/get',
            ...                    proxies=proxipy(country='US', port=8080))
            >>> req  # doctest: +ELLIPSIS
            <Response [...]>

    '''

    def __init__(self, type_: str='http', https: bool=True, last_check: int=60,
                 limit: int=1, country: str=None, port: int=None, **kwargs):
        self._logger = logging.getLogger(__name__)

        if type_ in ['http', 'socks4', 'socks5']:
            self.type_ = type_
        else:
            raise WrongConnType('Type should be "http" or "socks4" or'
                                '"socks5".')

        self.https = bool(https) if https else True
        self.last_check = int(last_check) if last_check else 60

        if 1 <= int(limit) <= 20:
            self.limit = int(limit)
        else:
            raise ReachedLimit('Cannot be less than 1 and more than 20.')

        if country:
            self.country_regex = re.compile(r'^([a-z]){2}$', re.I)

            if bool(self.country_regex.search(country)):
                self.country = country
            else:
                raise WrongCountryCode('You have to use appropriate 2 symbol '
                                       'country code.')
        else:
            self.country = None

        if port and 1 <= int(port) <= 65535:
            self.port = int(port)
        else:
            if port is None:
                self.port = None
            else:
                raise WrongPort('Port need to be >= 1 and <= 65535.')

        # Additional arguments: you don't need it, actually
        self.post = kwargs.get('post', True)
        self.user_agent = kwargs.get('user_agent', True)
        self.cookies = kwargs.get('cookies', None)
        self.referrer = kwargs.get('referrer', None)
        self.format = 'txt'

    def get_proxies(self) -> Union[dict, tuple]:
        '''Actually making request to proxy service. **NOT** an interface, use just :class:`proxipy.proxipy`.

           :raises: :class:`ServiceUnavailable`, if can't connect to proxy service.
           :raises: :class:`TemporaryBlocked`, if making more than 1 request per second.
           :raises: :class:`NoProxyFound`, if there is no proxy to your filters.
        '''

        self._params = dict(type=self.type_, https=self.https,
                            last_check=self.last_check, limit=self.limit,
                            country=self.country, port=self.port,
                            post=self.post, user_agent=self.user_agent,
                            cookies=self.cookies, referrer=self.referrer,
                            format=self.format)

        self._logger.debug('Making request to proxy service with params %s',
                           self._params)

        try:
            self._source = requests.get('http://pubproxy.com/api/proxy',
                                        timeout=(5, 6),
                                        params=self._params).text

        except Exception as e:
            raise ServiceUnavailable('Cannot connect to service.')

        if '#premium' in self._source:
            raise TemporaryBlocked('Too many requests per second.')

        if self._source == 'No proxy':
            raise NoProxyFound('There is no proxy to your filters. '
                               'Please, try to change it.')

        self._to_proxies = self._source.split()
        self.proxies = ()

        for proxy in self._to_proxies[::-1]:
            self.proxies += ('http://{}'.format(self._to_proxies.pop()),)

        if self.limit > 1:
            self._logger.info('Got proxy %s', self.proxies)
        else:
            self._logger.info('Got proxy %s', self.proxies[0])

        return self.proxies

'''
class aioproxipy:

    def __init__()
'''

class WrongConnType(Exception):
    '''Raised when ``type_`` param is not "http" or "socks4" or "socks5".'''


class ReachedLimit(Exception):
    '''Raised when trying to set ``limit`` param that less than 1 and more than 20.'''


class WrongCountryCode(Exception):
    '''Raised when ``country`` name param is not 2 symbol code.'''


class WrongPort(Exception):
    '''Raised when ``port`` param need to be >= 1 and <= 65535.'''


class ServiceUnavailable(Exception):
    '''Raised when cannot connect to proxy service.'''


class TemporaryBlocked(Exception):
    '''Raised when making more than 2 request per second.'''


class NoProxyFound(Exception):
    '''Raised when there is no proxy found to your filters.'''
