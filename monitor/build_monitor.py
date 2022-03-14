#!/usr/bin/env python3

import logging

from monitor.gpio.board import Board
from monitor.gpio.constants import Lights
from monitor.service.aggregator_service import AggregatorService, Result


class BuildMonitor(object):
    def __init__(self,
                 board: Board,
                 aggregator: AggregatorService):
        self.board = board
        self.aggregator = aggregator

    async def run(self) -> None:
        self.board.on(Lights.BLUE)
        logging.info("Getting build results")
        result = await self.aggregator.run()
        status = result['status']
        is_running = result['is_running']
        self.board.off(Lights.BLUE)

        logging.info(f'Setting output {result}')

        match status:
            case Result.PASS:
                self.board.on(Lights.GREEN)
                self.board.off(Lights.RED)
            case Result.FAIL:
                self.board.off(Lights.GREEN)
                self.board.on(Lights.RED)
            case Result.UNKNOWN:
                self.board.on(Lights.GREEN)
                self.board.on(Lights.RED)
            case _:
                self.board.off(Lights.GREEN)
                self.board.off(Lights.RED)

        if is_running:
            await self.board.pulse(Lights.YELLOW)
        else:
            self.board.off(Lights.YELLOW)

        logging.info("Finished build run")
