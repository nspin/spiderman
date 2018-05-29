# Browser-Assisted Crawling

Consider the case of archiving a website.
Writing code ot figure out what ancillary resources must be fetched is a pain.
Browsers already use various execution engines to do that.
The idea here is to use [mitmproxy](https://mitmproxy.org/) between the browser and the internet to capture traffic, and then to serve what it captured.
Experience shows that surprisingly faithful archives can be collected and viewed with this simple approach.

A headless browser can be used to automate parts of the archiving process.
