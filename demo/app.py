import sys
sys.path.insert(0, '..')

from daenerys import Daenerys

app = Daenerys()
# app.ignore_sites = {'pypi'}
app.mount_sites('sites')


if __name__ == "__main__":
    from pprint import pprint
    for url in ('https://pypi.python.org/pypi/Werkzeug/0.9.4',
                'https://pypi.python.org/pypi/Werkzeug',
                'https://mydomain.org/pypi/NotExistsPkg'):
        pkg = app.dispatch_url(url)
        pprint(pkg.info)
