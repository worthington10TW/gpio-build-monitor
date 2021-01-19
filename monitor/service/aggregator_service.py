#!/usr/bin/env python3

import asyncio
import enum
import monitor.ci_gateway.constants as ci_constants


class Result(enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"
    NONE = "NONE"

    def __eq__(self, other):
        return self.value == other.value


def get_status(result: dict) -> Result:
    if len(result) == 0:
        return Result.NONE
    elif any(r['status'] == ci_constants.CiResult.FAIL for r in result):
        return Result.FAIL

    elif all(r['status'] == ci_constants.CiResult.PASS for r in result):
        return Result.PASS
    else:
        return Result.UNKNOWN


class AggregatorService(object):
    def __init__(self, integrations: dict):
        self.integrations = integrations

    async def run(self):
        tasks = [integration() for integration in self.integrations]
        done, pending = await asyncio.wait(tasks)

        result = []
        [result.extend(future.result()) for future in done]

        return dict(
            type="AGGREGATED",
            is_running=True
            if any(
                r['status'] == ci_constants.CiResult.RUNNING for r in result)
            else False,
            status=get_status(
                list(
                    filter(
                        lambda x:
                        x['status'] != ci_constants.CiResult.RUNNING,
                        result))))
