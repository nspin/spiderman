from spiderman.normalize import normalize_url
from spiderman.addons import Intercept, Inject, cc

def pred(flow):
    return normalize_url(flow.request.url).startswith('https://moodle.carleton.edu')

def script(flow):
    with open('driver.js', 'r') as f:
        return f.read()

# Order matters. We don't want to save injected pages, or inject into CC
# communication.
addons = [
    cc('cia.gov', 443), # fbi.gov accepts h2 during ALPN, whereas cia.gov accepts http/1.1
    Intercept('db.sqlite', 'blobs', pred),
    Inject(script),
    ]
