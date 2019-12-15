import time
import requests
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

from website_testing.config import config


class MockHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        r = requests.get(config['general']['host'] + ':8080' + self.path)

        self.send_response(r.status_code)
        self.end_headers()

        if 'app.js' in self.path:
            js_str: str = r.content.decode('utf-8')
            # Overwrite the backend port with the mocked one
            js_str: str = js_str.replace('const BACKEND_PORT = \':5000\'', 'const BACKEND_PORT = \':5555\'')
            content: bytes = bytes(js_str, encoding='utf-8')
        else:
            content: bytes = r.content

        self.wfile.write(content)

        return

    def do_POST(self):
        # Another way to mock a timeout would be to invoke time.sleep(420).
        # Since there is no point in waiting for 7+ minutes for a single
        # test on each tests run, the faster route was chosen.
        time.sleep(5)
        self.send_error(408, 'Request Timeout')
        return


class MockServer(object):
    def __init__(self):
        self.port = 5555
        self.server = HTTPServer((config['general']['host'].replace('http://', ''), self.port), MockHandler)

        # Start running mock server in a separate thread.
        # Daemon threads automatically shut down when the main process exits.
        self.thread = Thread(target=self.server.serve_forever)
        self.thread.setDaemon(True)
        self.thread.start()
