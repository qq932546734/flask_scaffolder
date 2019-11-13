
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
* start_response：回调函数，应用用来发送HTTP status code和HTTP header给客户端。这表明该回调函数接受两个参数，第一个是HTTP状态码和状态信息拼成的string（格式是固定的：`200 Success`），第二个是HTTP header（格式是list of tuple，`[(header_name, header_value)]`）。由WSGI服务器提供。该函数必须返回一个callable，用于将bytestring写入response body中的。

### WSGI服务器端（server/gateway)

上面我们看了wsgi应用的接口，那么wsgi服务器端是怎么处理的呢？

#### WSGI中间件

中间件的设计，保证了应用可以嵌套。所以，中间件既要能起到WSGI server的作用，能调用上一层的application；中间件也需要有application的功能，被WSGI server调用。中间件的接驳，就像是“》》》》》》》”一样，任意个组合在一起，等同于一个application，能当成一个application被使用。

中间件的作用

1. 修改environ参数，然后将请求重定向到目标URL；
2. 在同一个进程中跑某个application的多个实例；
3. 将一个application进行拆分，load balancing；
4. 对content做一些后处理

### 设计原理

1. 为何application接受一个start_response的函数，而不是直接将HTTP headers & HTTP status作为返回值？

WSGI container, web server, web framework, WSGI server,