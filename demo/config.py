BROKER_URI = 'redis://localhost:6379'
BACKEND_URI = 'mongodb://localhost:27017'

PENDING = 0
SUCCESS = 1
FAILURE = 2
REVOKED = 3

READY_STATES = frozenset({SUCCESS, FAILURE, REVOKED})
