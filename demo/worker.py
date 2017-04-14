import multiprocessing

from kombu import Connection
from mongoengine.connection import connect, disconnect

from app import app
from config import BROKER_URI, SUCCESS
from backend import Backend
from messaging import consumer

URL_TEMPLATE = 'https://pypi.python.org/pypi/{name}'


def process_task(body, message):
    worker_id = multiprocessing.current_process().name
    name = body['name']
    url = URL_TEMPLATE.format(name=name)
    pkg = app.dispatch_url(url)
    Backend.mark_as_done(name, pkg.info, worker_id=worker_id, state=SUCCESS)
    message.ack()
    print 'FINISHED: {}'.format(name)


def main():
    disconnect()
    connect('zhihulive')
    with Connection(BROKER_URI) as conn:
        consumer(conn, [process_task])


if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=main)
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()
