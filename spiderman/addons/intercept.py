from mitmproxy import ctx

from spiderman.storage import Storage, Row

class Intercept(object):

    def __init__(self, db, blob_dir, pred):
        self.st = Storage(db, blob_dir)
        self.pred = pred

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
