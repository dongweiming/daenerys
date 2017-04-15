import time
import cPickle

from kombu import Connection, Exchange, Queue

from config import BROKER_URI, BACKEND_URI, SUCCESS, PENDING
from backend import Backend, r

exchange = Exchange('web', 'direct', durable=True)
queue = Queue('web_queue', exchange=exchange, routing_key='pypi')


def publish(conn, name):
    print 'PUT {}'.format(name)
    producer = conn.Producer(serializer='json')
    payload = {'name': name}
    producer.publish(payload, exchange=exchange, routing_key='pypi',
                     declare=[queue])
    return Backend.add(name)


def consumer(conn, callbacks):
    with conn.Consumer(queue, callbacks=callbacks) as consumer:
        while 1:
            conn.drain_events()


def sync_get(name, interval=0.5):
    with Connection(BROKER_URI) as conn:
        publish(conn, name)
        while 1:
            rs = r.get(name)
            if rs and Backend.from_json(cPickle.loads(rs)).status == SUCCESS:
                break
            time.sleep(interval)
        item = Backend.get(name)
        return item.result
