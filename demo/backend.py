import ast
import cPickle
from datetime import datetime

import redis
from mongoengine import *

from config import READY_STATES, PENDING, SUCCESS, FAILURE

connect('zhihulive')
r = redis.StrictRedis(host='localhost', port=6379, db=0)


class Backend(Document):
    name = StringField(max_length=20)
    result = DictField(default={})
    status = IntField(default=PENDING)
    traceback = StringField(default='')
    create_at = DateTimeField(default=datetime.now)
    worker_id = StringField(default='')

    meta = {
        'indexes': ['name']
    }

    @classmethod
    def add(cls, name):
        item = cls.get(name)
        if not item:
            item = cls(name=name)
            item.save()
        return item

    @classmethod
    def get(cls, name):
        rs = r.get(name)
        if rs:
            return cls.from_json(cPickle.loads(rs))
        try:
            item = cls.objects.get(name=name)
        except DoesNotExist:
            pass
        else:
            if item:
                r.set(name, cPickle.dumps(item.to_json()))
                return item

    @classmethod
    def mark_as_done(cls, name, result, worker_id, state=SUCCESS):
        item = cls.objects.get(name=name)
        if item:
            item.update(result=result, status=state, worker_id=worker_id)
            item = cls.objects.get(name=name)
            r.set(name, cPickle.dumps(item.to_json()))
            return True
        return False

    @classmethod
    def mark_as_failure(self, name, traceback, worker_id, state=FAILURE):
        item = cls.objects.get(name=name)
        if item:
            item.update(traceback=traceback, status=state, worker_id=worker_id)
            item = cls.objects.get(name=name)
            r.set(name, cPickle.dumps(item.to_json()))
            return True
        return False
