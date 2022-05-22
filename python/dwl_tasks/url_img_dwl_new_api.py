# -*- coding: utf-8 -*-

# !/usr/bin/python

# From the article: How to make Python code concurrent with 3 lines
# The entire code runs on Python 3.2+ without external packages.
# https://dev.to/rhymes/how-to-make-python-code-concurrent-with-3-lines-of-code-2fpe
# ...

# import a new API to create a thread pool
from concurrent.futures import ThreadPoolExecutor as ThPoolExecutor
# import a new API to create a process pool
from concurrent.futures import ProcessPoolExecutor as PrPoolExecutor

import http.client
import socket
import time
import sys

urls = [
    "www.google.com",
    "www.youtube.com",
    "www.wikipedia.org",
    "www.reddit.com",
    "www.httpbin.org"
] * 4 # * 200

# single/multi thread/process code to get an url
def get_it(url):
    try:
        # always set a timeout when you connect to an external server
        connection = http.client.HTTPSConnection(url, timeout=2)
        connection.request("GET", "/")
        response = connection.getresponse()
        return response.read()
    except socket.timeout:
        # in a real world scenario you would probably do stuff if the socket goes into timeout
        pass

# http loader
def loader():
    if len(sys.argv) < 1:
        print('Syntax: {} <method> (sp, th or pr) <num_workers> (threads or processes, def. 4)'.format(sys.argv[0]))
        sys.exit(0)
    
    if len(sys.argv) > 2:
        workers = sys.argv[2]
    else:
        workers = 4

    start_time = time.time()

    if sys.argv[1] == 'sp':
        for url in urls:
            get_it(url)

    elif sys.argv[1] == 'th':
        # create a thread pool of workers threads
        with ThPoolExecutor(max_workers=workers) as executor:
            # distribute the xxx URLs among x threads in the pool
            for _ in executor.map(get_it, urls):
                pass

    elif sys.argv[1] == 'pr':
        # create a thread pool of workers threads
        with PrPoolExecutor(max_workers=workers) as executor:
            # distribute the xxx URLs among x processes in the pool
            for _ in executor.map(get_it, urls):
                pass
    else:
        print('Unsupported method! Syntax: {} <method> (sp, th or pr) <num_workers> (threads or processes, def. 4)'.format(sys.argv[0]))

    print('Entire job took: {:6.2} seconds'.format(time.time() - start_time))

# arg1 : execution method
# arg2 : num_workers  (threads or processes)
if __name__ == '__main__':
    loader()