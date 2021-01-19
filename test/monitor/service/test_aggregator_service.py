#!/usr/bin/env python3

import aiounittest

from monitor.service.aggregator_service import Result, AggregatorService
import monitor.ci_gateway.constants as github_constants


async def return_pass():
    return dict(status=github_constants.CiResult.PASS),\
           dict(status=github_constants.CiResult.PASS)


async def return_fail():
    return dict(status=github_constants.CiResult.FAIL),


async def return_running():
    return dict(status=github_constants.CiResult.RUNNING),


class AggregatorServiceTests(aiounittest.AsyncTestCase):

    async def test_is_running(self):
        actions = [return_pass,
                   return_fail,
                   return_running]
        result = await AggregatorService(actions).run()
        self.assertEqual(True, result["is_running"])

    async def test_is_not_running(self):
        actions = [return_pass,
                   return_fail]
        result = await AggregatorService(actions).run()
        self.assertEqual(False, result["is_running"])

    async def test_contains_failed(self):
        actions = [return_pass,
                   return_fail]
        result = await AggregatorService(actions).run()
        self.assertEqual(Result.FAIL, result["status"])

    async def test_all_pass(self):
        actions = [return_pass,
                   return_pass,
                   return_running]
        result = await AggregatorService(actions).run()
        self.assertEqual(Result.PASS, result["status"])

    async def test_no_results(self):
        actions = [return_running]
        result = await AggregatorService(actions).run()
        self.assertEqual(Result.NONE, result["status"])


if __name__ == '__main__':
    aiounittest.main()
