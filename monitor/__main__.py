#!/usr/bin/env python3

import asyncio
import logging
import monitor.app as app

import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-log',
    default='info',
    help=(
        'Provide logging level. '
        'Example --log debug\', default=\'warning\''),
)
parser.add_argument(
    '-conf',
    default='integration.json',
    help='Integration configuration file',
)

options = parser.parse_args()
levels = dict(critical=logging.CRITICAL,
              error=logging.ERROR,
              warn=logging.WARNING,
              warning=logging.WARNING,
              info=logging.INFO,
              debug=logging.DEBUG)
level = levels.get(options.log.lower())
conf_file = options.conf
if level is None:
    raise ValueError(
        f'log level given: {options.log}'
        f' -- must be one of: {" | ".join(levels.keys())}')

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(app.main(conf_file, level))
except KeyboardInterrupt:
    pass
