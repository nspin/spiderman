# Browser-Assisted Crawling

Consider the case of archiving a website.
Writing code ot figure out what ancillary resources must be fetched is a pain.
Browsers already use various execution engines to do that.
The idea here is to use [mitmproxy](https://mitmproxy.org/) between the browser and the internet to capture traffic, and then to serve what it captured.
Experience shows that surprisingly faithful archives can be collected and viewed with this simple approach.

A headless browser can be used to automate parts of the archiving process.
Alternatively, this project contains an addon for injecting JavaScript into passing HTML pages, along with a small command-and-control server, to drive the browser.
This also works surprisingly well.

### Usage

This package exports two [mitmproxy](https://mitmproxy.org/) addons:
```
from spiderman import Crawl, Serve
```
They both take a path for a sqlite database and a path for a directory for response bodies.
They also each take a predicate on `mitmproxy.flow.Flow`.
For `Crawl`, this predicate determines whether a given flow should be recorded.
For `Serve`, this predicate determines whether a given flow should only be served from the local store (and not pass the proxy).

This example 
```
$ cat crawl.py
from spiderman import Crawl

def pred(flow):
    return flow.request.url.startswith('https://foo.bar')

addons = [
    Crawl('db.sqlite', 'blobs', pred)
    ]

$ cat serve.py
from spiderman import Serve

def pred(flow):
    return flow.request.url.startswith('https://foo.bar')

addons = [
    Serve('db.sqlite', 'blobs', pred)
    ]

$ mitmproxy -s crawl.py

# navigate through foo.bar in a (possibly headless) browser

$ mitmproxy -s serve.py

# explore the local copy of foo.bar intercepted by the proxy in the previous run
```
