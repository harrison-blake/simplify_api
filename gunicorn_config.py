import os

workers = int(os.environ.get('WEB_CONCURRENCY', '1'))
threads = 4
timeout = 20
graceful_timeout = 20

bind = ["[::]:{}".format(os.environ.get("PORT", 8000))]

forwarded_allow_ips = '*'
