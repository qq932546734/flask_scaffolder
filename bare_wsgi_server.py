import os, sys

# 获取系统编码格式
enc, esc = sys.getfilesystemencoding(), 'surrogateescape'

def unicode2wsgi(u):
    # 将环境变量转换成“byte-as-unicode"string
    return u.encode(enc, esc).decode('iso-8859-1')

def wsgi2bytes(s):
    return s.encode("iso-8859-1")

# WSGI服务器/网关端调用wsgi应用
def run_with_cgi(application):
    # 填充environ环境变量字典
    environ = {k: unicode2wsgi(v) for k, v in os.environ.items()}
    environ['wsgi.input']        = sys.stdin.buffer
    environ['wsgi.errors']       = sys.stderr
    environ['wsgi.version']      = (1, 0)
    environ['wsgi.multithread']  = False
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once']     = True
    environ['wsgi.url_scheme'] = 'http'
    if environ.get('HTTPS', 'off') in ('on', '1'):
        environ['wsgi.url_scheme'] = 'https'

    # 回调函数start_response会设置该值
    headers_set = []
    headers_sent = []

    def start_response(status, response_headers, exc_info=None):
        # exc_info的格式为sys.exc_info()返回的格式: (type, value, traceback)
        # type是BaseException的子类；value是type的instance；traceback是traceback对象
        if exc_info:
            try:
                if headers_sent:
                    raise exc_info[1].with_traceback(exc_info[2])
            finally:
                exc_info = None
        elif headers_set:
            raise AssertionError("headers already set!")
        
        headers_set[:] = [status, response_headers]
        
        # TODO：不明白为啥此处要返回write
        return write

    def write(data):
        out = sys.stdout.buffer
        # 先处理header，即先调用start_response
        if not headers_set:
            raise AssertionError("write() before start_response()")
        elif not headers_sent:
            status, response_headers = headers_sent[:] = headers_set
            out.write(wsgi2bytes("Status: {}\r\n".format(status)))
            for header in response_headers:
                out.write(wsgi2bytes("{}: {}\r\n".fomrat(header[0], headers[1])))
            out.write(wsgi2bytes('\r\n'))
        
        out.write(data)
        out.flush()

    result = application(environ, start_response)
    try:
        for data in result:
            if data:
                write(data)
        if not headers_sent:
            # 如果是response body是空的，
            write("")
    finally:
        if hasattr(result, 'close'):
            result.close()
        

