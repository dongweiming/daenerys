from werkzeug.utils import cached_property

from daenerys.site import Site
from daenerys.dinergate import Dinergate
from daenerys.pipeline.html import XPathTextProperty


site = Site(name="pypi")


@site.route("pypi.python.org", "/pypi/<name>", defaults={"version": ""})
@site.route("pypi.python.org", "/pypi/<name>/<version>")
class PythonPackageInfo(Dinergate):

    URL_TEMPLATE = "http://pypi.python.org/pypi/{self.name}/{self.version}"

    author = XPathTextProperty(
        xpath="//ul[@class='nodot']/li[1]/span/text()",
        pick_mode="first")
    _url_from_bt = XPathTextProperty(
        xpath=".//div[@id='download-button']/a/@href",
        strip_spaces=True, pick_mode="first")
    _url_from_table = XPathTextProperty(
        xpath="//table[@class='list']//a[re:match(@href, 'tar.gz#')]/@href",
        namespaces={'re': "http://exslt.org/regular-expressions"})

    @cached_property
    def download_url(self):
        return (self._url_from_table or self._url_from_bt).split('#')[0]

    @property
    def info(self):
        version = self.version or self.download_url.rpartition(
            '/')[-1].rsplit('-')[-1].replace('.tar.gz', '')
        return {"name": self.name, "version": version, "author": self.author,
                "download_url": self.download_url}
