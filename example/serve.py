from spiderman.normalize import normalize_url
from spiderman.addons import Serve

from mitmproxy import ctx

def pred(flow):
    ctx.log(normalize_url(flow.request.url))
    return normalize_url(flow.request.url).startswith('https://moodle.carleton.edu')

addons = [
    Serve('db.sqlite', 'blobs', pred)
]
