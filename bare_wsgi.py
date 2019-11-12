from wsgiref.simple_server import make_server

def application (environ, start_response):

    # Sorting and stringifying the environment key, value pairs
    items = ["{}:{}".format(k, v) for k, v in environ.items()]
    # Response body应该是bytes类型，所以需要encode一下
    response_body = "\n".join(items).encode()
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)

    return [response_body]

# Instantiate the server
httpd = make_server ('localhost', 5000, application)

# Wait for a single request, serve it and quit
httpd.handle_request()