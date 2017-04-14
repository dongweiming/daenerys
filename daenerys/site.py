class Site(object):
    def __init__(self, name):
        self.name = name
        self.actions = []

    def record_action(self, method_name, *args, **kwargs):
        self.actions.append((method_name, args, kwargs))

    def play_actions(self, target):
        for method_name, args, kwargs in self.actions:
            method = getattr(target, method_name)
            method(*args, **kwargs)

    def route(self, host, rule, **options):
        def decorator(func):
            endpoint = "{func.__module__}:{func.__name__}".format(func=func)
            self.record_action("add_url_rule", host, rule, endpoint, **options)
            return func
        return decorator
