#!/usr/bin/env python3
from unittest.mock import MagicMock, call
import aiounittest

from monitor.build_monitor import BuildMonitor
from monitor.gpio.constants import Lights
from monitor.service.aggregator_service import Result


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


class BuildMonitorTests(aiounittest.AsyncTestCase):
    def setUp(self):
        self.board = MagicMock()
        self.board.on = MagicMock()
        self.board.pulse = AsyncMock()
        self.board.off = MagicMock()
        self.aggregator = AsyncMock()
        self.aggregator.run = AsyncMock()

    async def test_blue_light_when_getting_results(self):
        self.aggregator.run.return_value = dict(
            is_running=True,
            status=Result.PASS)
        monitor = BuildMonitor(self.board, self.aggregator)
        self.assertFalse(self.board.on.called)

        await monitor.run()

        self.assertEqual(call(Lights.BLUE), self.board.on.call_args_list[0])
        assert self.aggregator.run.called
        self.assertEqual(call(Lights.BLUE), self.board.off.call_args_list[0])

    async def test_on_pass_turn_on_green(self):
        self.aggregator.run.return_value = dict(
            is_running=False,
            status=Result.PASS)
        monitor = BuildMonitor(self.board, self.aggregator)
        self.assertFalse(self.board.on.called)

        await monitor.run()

        self.assertEqual(call(Lights.GREEN), self.board.on.call_args_list[1])
        self.assertEqual(call(Lights.RED), self.board.off.call_args_list[1])

    async def test_on_fail_turn_on_red(self):
        self.aggregator.run.return_value = dict(
            is_running=False,
            status=Result.FAIL)
        monitor = BuildMonitor(self.board, self.aggregator)
        self.assertFalse(self.board.on.called)

        await monitor.run()

        self.assertEqual(call(Lights.GREEN), self.board.off.call_args_list[1])
        self.assertEqual(call(Lights.RED), self.board.on.call_args_list[1])

    async def test_on_unknown_turn_on_green_and_red(self):
        self.aggregator.run.return_value = dict(
            is_running=False,
            status=Result.UNKNOWN)
        monitor = BuildMonitor(self.board, self.aggregator)
        self.assertFalse(self.board.on.called)

        await monitor.run()

        self.assertEqual(call(Lights.GREEN), self.board.on.call_args_list[1])
        self.assertEqual(call(Lights.RED), self.board.on.call_args_list[2])

    async def test_pulse_when_running(self):
        self.aggregator.run.return_value = dict(
            is_running=True,
            status=Result.PASS)
        monitor = BuildMonitor(self.board, self.aggregator)
        self.assertFalse(self.board.on.called)

        await monitor.run()

        self.assertEqual(call(Lights.GREEN),
                         self.board.on.call_args_list[1])
        self.assertEqual(call(Lights.YELLOW),
                         self.board.pulse.call_args_list[0])

    async def test_do_not_pulse_when_not_running(self):
        self.aggregator.run.return_value = dict(
            is_running=False,
            status=Result.PASS)
        monitor = BuildMonitor(self.board, self.aggregator)
        self.assertFalse(self.board.on.called)

        await monitor.run()

        self.assertEqual(call(Lights.GREEN), self.board.on.call_args_list[1])
        self.assertEqual(call(Lights.RED), self.board.off.call_args_list[1])
        self.assertFalse(self.board.pulse.called)


if __name__ == '__main__':
    aiounittest.main()
