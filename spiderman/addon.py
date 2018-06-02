import re

from mitmproxy import ctx
from mitmproxy.http import HTTPResponse
from mitmproxy.net.http import Headers

from spiderman.storage import Storage, Row

body_re = re.compile(br'<\s*/\s*body\s*>')

class Crawl(object):

    def __init__(self, db, blob_dir, pred, driver_script):
        self.st = Storage(db, blob_dir)
        self.pred = pred
        self.driver_script = driver_script

    def response(self, flow):
        if self.pred(flow):
            if flow.request.method == 'GET':
                row = self.st.get_row_by_url(flow.request.url)
                if row is None:
                    row = Row(flow.request.url,
                        content_type=flow.response.headers['content-type'],
                        hash=self.st.put_blob(flow.response.get_content()),
                        )
                    ctx.log.info('@ putting row: {}'.format(row))
                    self.st.put_row(row)
        if 'content-type' in flow.response.headers and flow.response.headers['content-type'].startswith('text/html'):
            sub = r'<script>{}</script>\0'.format(self.driver_script(flow)).encode('ascii')
            flow.response.content = body_re.sub(sub, flow.response.content)

class Serve(object):

    def __init__(self, db, blob_dir, pred):
        self.st = Storage(db, blob_dir)
        self.pred = pred

    def request(self, flow):
        if self.pred(flow):
            try:
                if flow.request.method == 'GET':
                    row = self.st.get_row_by_url(flow.request.url)
                    if row is None:
                        ctx.log.info('@ not found: {}'.format(flow.request.url))
                        flow.response = HTTPResponse.make(404, content=flow.request.url)
                    else:
                        ctx.log.info('@ using row: {}'.format(row))
                        flow.response = HTTPResponse.make(
                            content=self.st.get_blob(row.hash),
                            headers={
                                'content-type': row.content_type
                                },
                            )
            except Exception as e:
                flow.response = HTTPResponse.make(500, content=str(e))
