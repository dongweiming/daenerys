from requests import Session

from daenerys.pipeline.base import PipelineProperty
from daenerys.exceptions import NotSupported


class HTTPClientProperty(PipelineProperty):
    def prepare(self):
        self.options.setdefault("session_class", Session)

    def provide_value(self, obj):
        session_class = self.options["session_class"]
        session = session_class()
        return session


class ResponseProperty(PipelineProperty):
    def prepare(self):
        self.options.setdefault("method", "GET")
        self.options.setdefault("data", {})

    def provide_value(self, obj):
        if "content_method" not in self.options:
            raise KeyError("You need create a subclass which inheritance "
                           "ResponseProperty, and assign `content_method` "
                           "into self.attr_names")
        response = obj.http_client.request(
            url=obj.url, method=self.options.get('method'),
            **self.options['data'])
        response.raise_for_status()
        content = getattr(response, self.options.get('content_method'))
        if callable(content):
            content = content()
        return content


class TextResponseProperty(ResponseProperty):
    def prepare(self):
        super(TextResponseProperty, self).prepare()
        self.options.setdefault("content_method", "content")


class JSONResponseProperty(ResponseProperty):
    def prepare(self):
        super(JSONResponseProperty, self).prepare()
        self.options.setdefault("content_method", "json")
