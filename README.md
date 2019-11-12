
### Flask如何做routing的


## WSGI
> WSGI is not a server, a python module, a framework, an API or any kind of software. It is just an interface specification by which server and application communicate. [link](http://wsgi.tutorial.codepoint.net/)

WSGI应用可以嵌套，嵌套起来以后，中间的WSGI应用就称为中间件。WSGI服务器（容器）的工作是从客户端或者web服务器端获取request，然后将之传递给WSGI应用，最后将应用返回的response返回给客户端。

### WSGI应用interface
WSGI应用是一个可执行的对象，可以是类（实现了`__call__`的类)、函数等。
```python
def application(environ, start_response):
    response_body = 'Request method: {}'.format(environ['REQUEST_METHOD'])
    # 写入response的时候需要先转换成bytes类型
    response_body = response_body.encode()
    status = "200 OK"
    response_header = [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(response_body)))
    ]
    # 调回调函数，返回状态码和HTTP头文件
    start_response(status, response_header)
    # 返回response主体，以iterable的形式
    return [response_body]


# MAKE A SERVER
from wsgiref.simple_server import make_server
server = make_server('localhost', 5000, application)
server.handle_request()
```
该可执行对象接受两个positional参数

* environ：字典类型，定义了各种变量的值。WSGI服务器在收到请求之后，由它来填充该dictionary的各个变量。
* start_response：回调函数，应用用来发送HTTP status code和HTTP header给客户端。这表明该回调函数接受两个参数，第一个是HTTP状态码，第二个是HTTP header。由WSGI服务器提供。

### WSGI服务器端（server/gateway)

上面我们看了wsgi应用的接口，那么wsgi服务器端是怎么处理的呢？



WSGI container, web server, web framework, WSGI server,