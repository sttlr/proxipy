#!/usr/bin/env python

import pytest
import proxipy
import time
import re

from typing import Callable, Union


@pytest.fixture(scope='function')
def get_proxy() -> Callable:

    def wrapper(*args, **kwargs) -> Union[dict, tuple]:
        prox = proxipy.proxipy(*args, **kwargs)
        time.sleep(1)

        return prox

    return wrapper


@pytest.fixture(scope='function')
def regex_proxy() -> Callable:

    def wrapper(prox, port=r'(\d){1,5}') -> bool:
        prox_http = prox['http']
        prox_https = prox['https']

        regex = re.compile(r'^http://((\d){1,3}\.?){4}:' + str(port) + r'$')

        result_http = bool(regex.search(prox_http))
        result_https = bool(regex.search(prox_https))

        if result_http == result_https:
            return True

        return False

    return wrapper
