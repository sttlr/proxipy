#!/usr/bin/env python

import proxipy
import pytest


def test_get_proxy_without_args(get_proxy, regex_proxy):
    prox_dict = get_proxy()
    assert 'http', 'https' in prox_dict.keys()

    assert regex_proxy(prox_dict)


@pytest.mark.parametrize('port,wrong_param', [(80, False), (8080, True)])
def test_get_proxy_with_args(get_proxy, regex_proxy, port, wrong_param):
    prox_dict = get_proxy(country='US', port=port, wrong_param=wrong_param)
    assert 'http', 'https' in prox_dict.keys()

    assert regex_proxy(prox_dict, port)


@pytest.mark.parametrize('limit', [2, 20])
def test_get_proxy_with_limit(get_proxy, regex_proxy, limit):
    prox_list = get_proxy(limit=limit)
    assert len(prox_list) == limit

    for prox_dict in prox_list:
        assert 'http', 'https' in prox_dict.keys()

        assert regex_proxy(prox_dict)


@pytest.mark.parametrize('type_', ['https', 'socks0'])
def test_error_wrong_conn_name(get_proxy, type_):
    with pytest.raises(proxipy.WrongConnType):
        get_proxy(type_=type_)


@pytest.mark.parametrize('limit', [-1, 0, 21])
def test_error_reached_limit(get_proxy, limit):
    with pytest.raises(proxipy.ReachedLimit):
        get_proxy(limit=limit)


@pytest.mark.parametrize('country', ['42', 'Oops', 'M7'])
def test_error_wrong_country_code(get_proxy, country):
    with pytest.raises(proxipy.WrongCountryCode):
        get_proxy(country=country)


@pytest.mark.parametrize('port', [-1, 0, 65536])
def test_error_wrong_port(get_proxy, port):
    with pytest.raises(proxipy.WrongPort):
        get_proxy(port=port)


@pytest.mark.parametrize('kwargs', [dict(country='UK'),
                                    dict(referrer=False, cookies=True,
                                         user_agent=False)])
def test_error_no_proxy_found(get_proxy, kwargs):
    with pytest.raises(proxipy.NoProxyFound):
        get_proxy(**kwargs)
