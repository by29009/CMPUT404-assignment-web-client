import socket
import re
import urllib

def received_complete_response(buffer):
    """
    Fixes issue with sites returning 302 and keeping the conn open
    (recvall given to us will wait forever for conn close?)
    """
    headers = buffer.split('\r\n')
    content_length = [h for h in headers if h[:15] == 'Content-Length:']
    if content_length == []:
        return False
    content_length = int(content_length[0][15:])

    if buffer.find('\r\n\r\n') == -1:
        return False

    split_buffer = buffer.split('\r\n\r\n')
    if (len(split_buffer) == 1 or split_buffer[1] == '') and content_length == 0:
        return True
    if len(split_buffer[1]) >= content_length:
        return True

    return False

def recvall(sock):
    buffer = bytearray()
    done = False
    while not done:
        part = sock.recv(1024)
        if (part):
            buffer.extend(part)
            if received_complete_response(buffer):
                break
        else:
            done = not part

    return str(buffer)

def do_request(url, request):
    """
    sends the request as-is to the url
    returns the response
    """

    url = url.replace('http://', '')
    if url.find('/') != -1:
        url = url[:url.find('/')]

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if url.find(':') == -1:
        clientSocket.connect((url, 80))
    else:
        splitUrl = url.split(':')
        host, port = splitUrl[0], splitUrl[1]
        clientSocket.connect((host, int(port)))

    # print(request + '\n')
    clientSocket.sendall(request)

    return recvall(clientSocket)

def geturl_from_url(url):
    """
    Return the /url for the request
    Example: 'localhost/hi/ha.html' -> '/hi/ha.html'
    """
    url = url.replace('http://', '')
    if url.find('/') == -1:
        return '/'
    return url[url.find('/'):]

def host_from_url(url):
    """
    Returns host for Host header
    """
    url = url.replace('http://', '')
    if url.find('/') != -1:
        url = url[:url.find('/')]
    return url

def parse_response(response):
    """
    Extract the needed info from response
    Return (code, body)
    """
    headers = (response.split('\r\n\r\n')[0]).strip().split('\r\n')
    body = response.split('\r\n\r\n')[1]

    code_header = [header for header in headers if header[:8] == 'HTTP/1.1' or header[:8] == 'HTTP/1.0'][0]
    code = int(code_header.split(' ')[1])

    return code, body

def argstring_from_args(args):
    """
    args is a dict
    """
    if args is None:
        return ''
    else:
        return urllib.urlencode(args)
        # arg_string = '?'
        # for key in args:
        #     arg = '{0}={1}'.format(key, urllib.urlencode(args[key]))
        #     arg_string += arg
        #     arg_string += '&'
        # arg_string = arg_string[:-1]