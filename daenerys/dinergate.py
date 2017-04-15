from daenerys.pipeline.html import ElementTreeProperty
from daenerys.pipeline.network import HTTPClientProperty, TextResponseProperty


class Dinergate(object):
    URL_TEMPLATE = None

    http_client = HTTPClientProperty()
    text_response = TextResponseProperty()
    etree = ElementTreeProperty()

    def __init__(self, request, http_client=None, **kwargs):
        self.request = request
        if http_client:
            self.http_client = http_client
        # assign arguments from URL pattern
        vars(self).update(kwargs)

    @property
    def url(self):
        if not self.URL_TEMPLATE:
            raise NotImplementedError
        return self.URL_TEMPLATE.format(self=self)

    def to_dict(self):
        return {k: getattr(self, k) for k in dir(self)
                if not k.startswith('_') and k not in ('text_response',)}
