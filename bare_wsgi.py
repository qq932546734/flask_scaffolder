from wsgiref.simple_server import make_server

# 调用该函数时，必须采用positional的形式调用，不能用keywords，因为没有规定参数名
def application(environ, start_response):

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


# callable是class的时候
class AppClass:

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
    
    def __iter__(self):
        status = "200 OK"
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield HELLO_WORLD


# Instantiate the server
httpd = make_server ('localhost', 5000, application)

# Wait for a single request, serve it and quit
# httpd.handle_request()
httpd.serve_forever()