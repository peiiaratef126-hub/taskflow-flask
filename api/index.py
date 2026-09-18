import os
import sys
from urllib.parse import parse_qs, urlencode

# Add project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app import create_app

flask_app = create_app(os.environ.get("FLASK_ENV", "production"))


def app(environ, start_response):
    """
    Vercel WSGI entrypoint wrapper.
    Restores the exact original PATH_INFO passed from Vercel rewrite parameter __vercel_route.
    """
    query_string = environ.get("QUERY_STRING", "")
    if "__vercel_route" in query_string:
        params = parse_qs(query_string, keep_blank_values=True)
        route_list = params.pop("__vercel_route", None)
        if route_list and route_list[0]:
            route = route_list[0]
            environ["PATH_INFO"] = route if route.startswith("/") else ("/" + route)
        else:
            environ["PATH_INFO"] = "/"
        environ["QUERY_STRING"] = urlencode(params, doseq=True)

    return flask_app(environ, start_response)
