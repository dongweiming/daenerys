import urllib
from urlparse import urlparse, ParseResult

from werkzeug.utils import find_modules, import_string
from werkzeug.urls import url_decode, url_encode
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect

from .request import Request
from .exceptions import NotSupported


class Daenerys(object):
    def __init__(self, ignore_sites=set()):
        self.url_map = Map(strict_slashes=False, host_matching=True,
                           redirect_defaults=False)
        self.ignore_sites = ignore_sites

    def add_url_rule(self, host, rule_string, endpoint, **options):
        rule = Rule(rule_string, host=host, endpoint=endpoint, **options)
        self.url_map.add(rule)

    def parse_url(self, url_string):
        url = urlparse(url_string)
        url = self.validate_url(url)
        url_adapter = self.url_map.bind(server_name=url.hostname,
                                        url_scheme=url.scheme,
                                        path_info=url.path)
        query_args = url_decode(url.query)
        return url, url_adapter, query_args

    def validate_url(self, url):
        url_path = urllib.quote(url.path, safe=b"/%")
        url_query = urllib.quote(url.query, safe=b"?=&")

        url = ParseResult(url.scheme, url.netloc, url_path,
                          url.params, url_query, url.fragment)

        has_hostname = url.hostname is not None and len(url.hostname) > 0
        has_http_scheme = url.scheme in ("http", "https")
        has_path = not len(url.path) or url.path.startswith("/")

        if not (has_hostname and has_http_scheme and has_path):
            raise NotSupported("invalid url: %s" % repr(url))

        return url

    def dispatch_url(self, url_string):
        url, url_adapter, query_args = self.parse_url(url_string)

        try:
            endpoint, kwargs = url_adapter.match()
        except NotFound:
            raise NotSupported(url_string)
        except RequestRedirect as e:
            new_url = "{0.new_url}?{1}".format(e, url_encode(query_args))
            return self.dispatch_url(new_url)

        try:
            handler = import_string(endpoint)
            request = Request(url=url, args=query_args)
            return handler(request, **kwargs)
        except RequestRedirect as e:
            return self.dispatch_url(e.new_url)

    def mount_site(self, site):
        if isinstance(site, basestring):
            site = import_string(site)
        site.play_actions(target=self)

    def mount_sites(self, root):
        for name in find_modules(root, recursive=True):
            mod = import_string(name)
            site = name.split('.')[-1]
            if hasattr(mod, 'site') and site not in self.ignore_sites:
                mod.site.play_actions(target=self)

