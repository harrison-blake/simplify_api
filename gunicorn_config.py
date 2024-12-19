import os

bind = "0.0.0.0:8000"  
workers = 2

if os.getenv('ENV') == 'production':
    debug = False
    loglevel = 'info'
else:
    debug = True
    loglevel = 'debug'
    