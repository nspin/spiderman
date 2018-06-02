from collections import deque
from threading import Lock
import os.path

from mitmproxy.addons import wsgiapp
import tornado.web
import tornado.wsgi
import tornado.escape

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 13337
DEFAULT_NETLOC = '{}:{}'.format(DEFAULT_HOST, DEFAULT_PORT)

def cc(host=DEFAULT_HOST, port=DEFAULT_PORT):
    return wsgiapp.WSGIApp(tornado.wsgi.WSGIAdapter(mk_app()), host, port)

def mk_app():
    queue = Queue()
    handlers = [
        ('/next', NextHandler, {'queue': queue}),
        ('/enqueue', EnqueueHandler, {'queue': queue}),
        ]
    return tornado.web.Application(handlers, debug=True)

class Queue(object):

    def __init__(self):
        self.lock = Lock()
        self.q = deque()
        self.seen = set()

    def enqueue(self, x):
        with self.lock:
            if x not in self.seen:
                self.q.append(x)
                self.seen.add(x)

    def dequeue(self):
        with self.lock:
            return self.q.popleft()

    def is_empty(self):
        with self.lock:
            return len(self.q) == 0

class NextHandler(tornado.web.RequestHandler):

    def initialize(self, queue):
        self.queue = queue

    def get(self):
        if self.queue.is_empty():
            self.send_error(404)
        else:
            self.redirect(self.queue.deque(), permanent=False)

class EnqueueHandler(tornado.web.RequestHandler):

    def initialize(self, queue):
        self.queue = queue

    def post(self):
        urls = tornado.escape.json_decode(self.request.body)
        for url in urls:
            self.queue.enqueue(url)

if __name__ == '__main__':
    import tornado.ioloop
    app = mk_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
