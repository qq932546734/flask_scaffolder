from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

@Request.application
def application(request):
    return Response("<h1>Hello, world</h1>")

if __name__ == "__main__":
    run_simple("localhost", 5000, application)