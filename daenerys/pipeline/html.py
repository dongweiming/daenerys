import lxml.html

from daenerys.pipeline.base import PipelineProperty


class ElementTreeProperty(PipelineProperty):
    def prepare(self):
        self.options.setdefault("encoding", None)

    def provide_value(self, obj):
        text_response = obj.text_response
        if self.options["encoding"]:
            text_response = text_response.encode(self.options["encoding"])
        return lxml.html.fromstring(text_response)


class XPathTextProperty(PipelineProperty):
    required_attrs = {"xpath"}
    def prepare(self):
        self.options.setdefault("strip_spaces", False)
        self.options.setdefault("pick_mode", "join")
        self.options.setdefault("joiner", " ")
        self.options.setdefault("namespaces", None)

    def choice_pick_impl(self):
        pick_mode = self.options["pick_mode"]
        impl = {
            "join": self.pick_joining,
            "first": self.pick_first,
            "keep": self.keep_value,
        }.get(pick_mode)

        if not impl:
            raise ValueError("%r is not valid pick mode" % pick_mode)
        return impl

    def pick_joining(self, value):
        joiner = self.options["joiner"]
        return joiner.join(value)

    def pick_first(self, value):
        return value[0] if value else ""

    def keep_value(self, value):
        return value

    def provide_value(self, obj):
        value = obj.etree.xpath(
            self.xpath, namespaces=self.options.get("namespaces"))
        pick_value = self.choice_pick_impl()

        if self.options["strip_spaces"]:
            value = [v.strip() for v in value if v.strip()]

        return pick_value(value)
