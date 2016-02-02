import socket
import re
import urllib

def recvall(sock):
    buffer = bytearray()
    done = False
    while not done:
        part = sock.recv(1024)
        if (part):
            buffer.extend(part)
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

    clientSocket.sendall(request)

    return recvall(clientSocket)

def geturl_from_url(url):
    """
    Return the /url for the request
    Example: 'localhost/hi/ha.html' -> '/hi/ha.html'
    """
    if url.find('/') == -1:
        return '/'
    return url[url.find('/'):]

def parse_response(response):
    """
    Extract the needed info from response
    Return (code, body)
    """
    headers = (response.split('\r\n\r\n')[0]).strip().split('\r\n')
    body = response.split('\r\n\r\n')[1]

    code_header = [header for header in headers if header[:8] == 'HTTP/1.1'][0]
    code = int(code_header.split(' ')[1])

    return code, body