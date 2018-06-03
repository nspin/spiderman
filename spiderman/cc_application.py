import json
from threading import Lock
from collections import deque

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.utils import redirect
from werkzeug.exceptions import HTTPException, NotFound

class UniQ(object):

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

class Application(object):

    def __init__(self, uniq):
        self.uniq = uniq
        self.url_map = Map([
            Rule('/', methods=['GET'], endpoint=self.on_root),
            Rule('/next', methods=['GET'], endpoint=self.on_next),
            Rule('/enqueue', methods=['POST'], endpoint=self.on_enqueue),
            ])

    def __call__(self, environ, start_response):
        request = Request(environ)
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, _ = adapter.match()
        except HTTPException as e:
            response = e
        else:
            response = endpoint(request)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response(environ, start_response)

    def on_root(self, request):
        return Response('idle')

    def on_next(self, request):
        url = '/' if self.uniq.is_empty() else self.uniq.dequeue()
        return redirect(url, code=302)

    def on_enqueue(self, request):
        urls = json.loads(request.get_data())
        for url in urls:
            self.uniq.enqueue(url)
        return Response('thanks')

def create_application():
    uniq = UniQ()
    return Application(uniq)

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    application = create_application()
    run_simple('localhost', 13337, application,
            # ssl_context='adhoc',
            use_debugger=True,
            use_reloader=True,
            )
