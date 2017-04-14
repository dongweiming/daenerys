import random

from kombu import Connection

from messaging import publish
from config import BROKER_URI


PACKAGES = ['httpie', 'django', 'requests', 'keras',
            'tornado', 'sentry', 'ipython', 'werkzeug']


if __name__ == '__main__':
    with Connection(BROKER_URI) as conn:
        random.shuffle(PACKAGES)
        for p in PACKAGES:
            publish(conn, p)



