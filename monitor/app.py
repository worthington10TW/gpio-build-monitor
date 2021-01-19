#!/usr/bin/env python3

import logging
import asyncio
import json
import os
import pprint
from gpio.board import Board
from .service.aggregator_service import AggregatorService
from .service.integration_mapper import IntegrationMapper
from .ci_gateway import integration_actions as available_integrations
from .log_handler import setup_logger
from .build_monitor import BuildMonitor


async def main(conf_file, level):
    config = get_config(conf_file)
    setup_logger(level)
    logging.info('Hello build monitor!')

    with Board() as board:
        logging.info('Board initialised')
        poll_in_seconds = config.get('poll_in_seconds') or 30
        integrations = config['integrations']
        logging.info(f'Polling increment (in seconds): {poll_in_seconds}')
        logging.info(f'Integrations: {pprint.pformat(integrations)}')

        aggregator = AggregatorService(
            IntegrationMapper(
                available_integrations.get_all()).get(
                integrations))
        monitor = BuildMonitor(board, aggregator)
        while True:
            await monitor.run()
            await asyncio.sleep(poll_in_seconds)


def get_config(conf_file):
    path = os.path.join(
        os.getcwd(), conf_file)
    response_json = path
    with open(response_json) as integrations:
        return json.load(integrations)
