import re
import unicodedata
from urllib.parse import quote, quote_plus, unquote, urlsplit, urlunsplit


# from https://github.com/niksite/url-normalize/blob/master/url_normalize/url_normalize.py
# TODO adapt to our needs
def normalize_url(url, charset='utf-8'):
    """URI normalization routine.
    Sometimes you get an URL by a user that just isn't a real
    URL because it contains unsafe characters like ' ' and so on.  This
    function can fix some of the problems in a similar way browsers
    handle data entered by the user:
    >>> normalize_url(u'http://de.wikipedia.org/wiki/Elf (Begriffsklärung)')
    'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'
    Params:
        charset : string : The target charset for the URL if the url was
                           given as unicode string.
    """
    # if there is no scheme use http as default scheme
    if url[0] not in ['/', '-'] and ':' not in url[:7]:
        url = 'http://' + url

    # shebang urls support
    url = url.replace('#!', '?_escaped_fragment_=')

    # remove feedburner's crap
    url = re.sub(r'\?utm_source=feedburner.+$', '', url)

    # splitting url to useful parts
    scheme, auth, path, query, fragment = urlsplit(url.strip())
    (userinfo, host, port) = re.search('([^@]*@)?([^:]*):?(.*)', auth).groups()

    # Always provide the URI scheme in lowercase characters.
    scheme = scheme.lower()

    # Always provide the host, if any, in lowercase characters.
    host = host.lower()
    if host and host[-1] == '.':
        host = host[:-1]

    # take care about IDN domains
    host = host.encode("idna").decode(charset)

    # Only perform percent-encoding where it is essential.
    # Always use uppercase A-through-F characters when percent-encoding.
    # All portions of the URI must be utf-8 encoded NFC from Unicode strings
    path = quote(_clean(path), "~:/?#[]@!$&'()*+,;=")
    fragment = quote(_clean(fragment), "~")

    # note care must be taken to only encode & and = characters as values
    query = "&".join(
        sorted(["=".join(
            [quote(_clean(t), "~:/?#[]@!$'()*+,;=")
             for t in q.split("=", 1)]) for q in query.split("&")]))

    # Prevent dot-segments appearing in non-relative URI paths.
    if scheme in ["", "http", "https", "ftp", "file"]:
        output, part = [], None
        for part in path.split('/'):
            if part == "":
                if not output:
                    output.append(part)
            elif part == ".":
                pass
            elif part == "..":
                if len(output) > 1:
                    output.pop()
            else:
                output.append(part)
        if part in ["", ".", ".."]:
            output.append("")
        path = '/'.join(output)

    # For schemes that define a default authority, use an empty authority if
    # the default is desired.
    if userinfo in ["@", ":@"]:
        userinfo = ""

    # For schemes that define an empty path to be equivalent to a path of "/",
    # use "/".
    if path == "" and scheme in ["http", "https", "ftp", "file"]:
        path = "/"

    # For schemes that define a port, use an empty port if the default is
    # desired
    if port and scheme in DEFAULT_PORT.keys():
        if port.isdigit():
            port = str(int(port))
            if int(port) == DEFAULT_PORT[scheme]:
                port = ''

    # Put it all back together again
    auth = (userinfo or "") + host
    if port:
        auth += ":" + port
    if url.endswith("#") and query == "" and fragment == "":
        path += "#"

    return urlunsplit((scheme, auth, path, query, fragment))


def _clean(string, charset='utf-8'):
    """Unquote and normalize unicode string.
    Params:
        charset : string : optional : output encoding
    Returns:
        string : an unquoted and normalized string
    """
    string = unquote(string)
    return unicodedata.normalize('NFC', string).encode(charset)


DEFAULT_PORT = {
    'ftp': 21,
    'telnet': 23,
    'http': 80,
    'ws': 80,
    'gopher': 70,
    'news': 119,
    'nntp': 119,
    'prospero': 191,
    'https': 443,
    'wss': 443,
    'snews': 563,
    'snntp': 563,
}
