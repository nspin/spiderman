from spiderman import Crawl, cc, normalize_url

def pred(flow):
    return normalize_url(flow.request.url).startswith('https://moodle.carleton.edu')

def driver_script(flow):
    with open('driver.js', 'r') as f:
        return f.read()

addons = [
    Crawl('db.sqlite', 'blobs', pred, driver_script),
    cc(),
]
