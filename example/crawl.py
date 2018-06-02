from spiderman import Crawl, cc, normalize_url

def pred(flow):
    return normalize_url(flow.request.url).startswith('https://moodle.carleton.edu')

addons = [
    Crawl('db.sqlite', 'blobs', pred),
    cc('driver.js'),
]
