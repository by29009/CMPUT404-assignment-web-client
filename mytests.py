from __future__ import print_function

from httpclient import HTTPClient, HTTPResponse

from clientfuncs import *

def a():
    client = HTTPClient()
    response = client.command('127.0.0.1:8080/', command='GET')
    print('Code: {0}'.format(response.code))
    print('Body: {0}'.format(response.body))

def test1():
    argstring = argstring_from_args({'a': 'asd', 's': 'a a'})
    assert argstring == 'a=asd&s=a+a'

if __name__ == '__main__':
    test1()