from mitmproxy.addons import wsgiapp

from spiderman.cc_application import create_application

# Problems arise when the real server at host:port serves over TLS and accepts
# h2 during ALPN. mitmproxy's wsgi addon adapter doesn't support HTTP/2, but it
# doesn't stop the client from suggesting it during ALPN. To avoid issues with
# mixed content, most applications of this addon will need to run over TLS. So,
# Solutions are to run mitmproxy with --no-http2 or to ensure that host:port
# doesn't support HTTP/2. I don't feel like scanning the internet for
# candidates, but cia.gov does work. Also, you could run a dummy server
# somwhere.
def cc(host, port):
    return wsgiapp.WSGIApp(create_application(), host, port)
