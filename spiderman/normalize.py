import unicodedata
from urllib.parse import quote, unquote, urlsplit, urlunsplit, urljoin

DEFAULT_PORT = {
    'http': 80,
    'https': 443,
    }

# Should work alright most of the time.
def normalize_url(url, default_scheme='http', encoding='utf-8'):

    split = urlsplit(url.strip(), scheme=default_scheme)

    scheme = split.scheme.lower()

    netloc = split.hostname.lower().encode('idna').decode(encoding).rstrip('.')
    if split.username:
        netloc += split.username
        if split.password:
            netloc += ':' + split.password
        netloc += '@'
    if split.port:
        if not split.port.isdigit() or int(port) != DEFAULT_PORT[scheme]:
            netloc += ':' + split.port

    path_segments = []
    for raw_seg in split.path.split('/'):
        seg = normalize_path_segment(raw_seg)
        if seg == '' or seg == '.':
            pass
        elif seg == '..':
            if len(path_segments) > 1:
                path_segments.pop()
        else:
            path_segments.append(seg)
    if seg in ('', '.', '..'):
        path_segments.append('')
    path = ''.join(('/' + seg for seg in path_segments))

    query = '&'.join(
        sorted(
            filter(None,
                map(normalize_query_segment,
                    split.query.split('&')))))

    return urlunsplit((scheme, netloc, path, query, ''))


# TODO: minimize quoted characters
# TODO: path parameters
def normalize_path_segment(seg):
    return quote(_clean(seg), safe='')

# TODO: minimize quoted characters
def normalize_query_segment(seg):
    def f(subseg):
        return quote(_clean(subseg), safe='')
    return '='.join(map(f, seg.split('=', 1)))

def _clean(string, encoding='utf-8'):
    string = unquote(string)
    return unicodedata.normalize('NFC', string).encode(encoding)
