proxipy
=======

Need proxy? You`re welcome.
---------------------------

To parse really big site in a small amount of time you need to make hundreds of requests concurrently and not being banned *(that's mainly impossible to do from one IP)*.

So, **proxipy** could help you with this.

It returns a random proxy *(or list of proxies)* to use it directly in requests module.

Installation
------------

.. code-block:: bash

    $ pip install proxipy

Usage
-----

First, we need to import our module (and/or **requests**):

.. code-block:: python

    >>> from proxipy import proxipy
    >>> import requests

And use it **with/out filters**:

.. code-block:: python

    >>> prox = proxipy()
    >>> prox
    {'http': ..., 'https': ...}
    >>> req = requests.get('http://httpbin.org/get',
    ...                    proxies=proxipy(country='US', port=8080))
    >>> req
    <Response [...]>
