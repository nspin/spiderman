import re

from mitmproxy import ctx

body_re = re.compile(br'<\s*/\s*body\s*>')

class Inject(object):

    def __init__(self, script):
        self.script = script

    def response(self, flow):
        if 'content-type' in flow.response.headers and flow.response.headers['content-type'].startswith('text/html'):
            script = self.script(flow)
            if script:
                sub = ('<script>' + script + '</script></body>').encode('ascii')
                flow.response.content = body_re.sub(sub, flow.response.content)
                # TODO: more granular header modification, and deal with
                # relevant <meta> tags.
                flow.response.headers.pop('Content-Security-Policy', None)
