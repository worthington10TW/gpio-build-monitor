#!/usr/bin/env python3

import logging
from monitor.gpio.constants import Lights
from monitor.service.aggregator_service import AggregatorService, Result


class BuildMonitor(object):
    def __init__(self,
                 board,
                 aggregator: AggregatorService):
        self.board = board
        self.aggregator = aggregator

    async def run(self):
        self.board.on(Lights.BLUE)
        logging.info("Getting build results")
        result = await self.aggregator.run()
        status = result['status']
        is_running = result['is_running']
        self.board.off(Lights.BLUE)

        logging.info(f'Setting output {result}')
        if Result.PASS == status:
            self.board.on(Lights.GREEN)
            self.board.off(Lights.RED)
        elif Result.FAIL == status:
            self.board.off(Lights.GREEN)
            self.board.on(Lights.RED)
        elif Result.UNKNOWN == status:
            self.board.on(Lights.GREEN)
            self.board.on(Lights.RED)
        else:
            self.board.off(Lights.GREEN)
            self.board.off(Lights.RED)

        if is_running:
            await self.board.pulse(Lights.YELLOW)
        else:
            self.board.off(Lights.YELLOW)

        logging.info("Finished build run")
