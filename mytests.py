from __future__ import print_function

from httpclient import HTTPClient, HTTPResponse

if __name__ == '__main__':
    client = HTTPClient()
    response = client.command('127.0.0.1:8080/', command='GET')
    print('Code: {0}'.format(response.code))
    print('Body: {0}'.format(response.body))