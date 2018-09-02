#!/usr/bin/env python

'''
proxipy is the package that could help you get proxy in the easiest way:

    >>> from proxipy import proxipy
    >>> import requests
    >>> prox = proxipy()
    >>> prox
    {'http': ..., 'https': ...}
    >>> req = requests.get('http://httpbin.org/get',
    ...                    proxies=proxipy(country='US', port=8080))
    >>> req
    <Response [...]>

'''

from .proxipy import proxipy, aioproxipy, WrongConnType, ReachedLimit
from .proxipy import WrongCountryCode, WrongPort, ServiceUnavailable
from .proxipy import TemporaryBlocked, NoProxyFound

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __license__, __copyright__
