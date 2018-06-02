from mitmproxy import ctx
from spiderman import Serve, normalize_url

def pred(flow):
    ctx.log(normalize_url(flow.request.url))
    return normalize_url(flow.request.url).startswith('https://moodle.carleton.edu')

addons = [
    Serve('db.sqlite', 'blobs', pred)
]
