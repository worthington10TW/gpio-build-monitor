#!/usr/bin/env python3
from unittest import mock
from unittest.mock import MagicMock, call
import aiounittest
from aioresponses import aioresponses
from monitor.build_monitor import BuildMonitor
from monitor.gpio.board import Board
from monitor.gpio.constants import Lights
from monitor.service.aggregator_service import AggregatorService
from monitor.service.integration_mapper import IntegrationMapper
import monitor.ci_gateway.integration_actions as available_integrations


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


async def run(mocked_pwm):
    mocked_pwm.return_value.ChangeDutyCycle = mock.MagicMock()
    mocked_pwm.return_value.stop = mock.MagicMock()
    data = {
        "workflow_runs": [
            dict(id=448533827,
                 name="CI",
                 created_at="2020-12-28T09:23:57Z",
                 html_url="http://cheese.com",
                 status="in_progress",
                 conclusion=None),
            dict(id=448533828,
                 name="Another",
                 created_at="2020-12-28T09:23:57Z",
                 html_url="http://cheese.com",
                 status="completed",
                 conclusion="success")
        ]
    }

    integrations = [dict(
        type='GITHUB',
        username='super-man',
        repo='awesome')]

    with aioresponses() as m:
        m.get('https://api.github.com/repos/super-man/awesome/actions/runs',  # noqa: E501
              payload=data, status=200)
        aggregator = AggregatorService(
            IntegrationMapper(
                available_integrations.get_all()).get(
                integrations))

        with Board() as board:
            monitor = BuildMonitor(board, aggregator)
            await monitor.run()


class AppTests(aiounittest.AsyncTestCase):

    @mock.patch('monitor.gpio.Mock.GPIO.PWM')
    @mock.patch('monitor.gpio.Mock.GPIO.output')
    async def test_blue_light(self, mocked_output, mocked_pwm):
        await run(mocked_pwm)
        self.assertTrue(call(Lights.BLUE.value, 1) in
                        mocked_output.call_args_list)
        self.assertTrue(call(Lights.BLUE.value, 0) in
                        mocked_output.call_args_list)

    @mock.patch('monitor.gpio.Mock.GPIO.PWM')
    @mock.patch('monitor.gpio.Mock.GPIO.output')
    async def test_pulse(self, mocked_output, mocked_pwm):
        await run(mocked_pwm)
        self.assertEqual(1, mocked_pwm.return_value.start.call_count)
        assert mocked_pwm.return_value.ChangeDutyCycle.called

    @mock.patch('monitor.gpio.Mock.GPIO.PWM')
    @mock.patch('monitor.gpio.Mock.GPIO.output')
    async def test_result(self, mocked_output, mocked_pwm):
        await run(mocked_pwm)
        self.assertTrue(call(Lights.GREEN.value, 1) in
                        mocked_output.call_args_list)
        self.assertTrue(call(Lights.RED.value, 0) in
                        mocked_output.call_args_list)


if __name__ == '__main__':
    aiounittest.main()
