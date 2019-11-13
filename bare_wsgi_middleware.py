from piglatin import piglatin

class LatinIter:
    
    def __init__(self, result, transform_ok):
        if hasattr(result, 'close'):
            result.close()
        self._next = iter(result).__next__
        self.transform_ok = transform_ok

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.transform_ok:
            return piglatin(self._next())
        else:
            return self._next()


class Latinator:

    transform = False

    def __init__(self, application):
        self.application = application

    def __call__(self, environment, start_response):
        transform_ok = []

        def start_latin(status, respones_headers, exc_info=None):
            del transform_ok[:]

            for name, value in respones_headers:
                if name.lower() == "content-type" and value == "text/plain":
                    transform_ok.append(True)

                    respones_headers = []
                    for name, value in respones_headers:
                        if name.lower() != 'content-length':
                            respones_headers.append((name, value))
                    break
            
            write = start_response(status, respones_headers, exc_info)

            if transform_ok:
                def write_latin(data):
                    write(piglatin(data))
                return write_latin
            else:
                return write
        
        return LatinIter(self.application(environ, start_latin), transform_ok)
                

from foo_app import foo_app
run_with_cgi(Latinator(foo_app))