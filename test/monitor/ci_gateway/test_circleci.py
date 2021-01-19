#!/usr/bin/env python3

import pytest
import json
import os
import aiounittest
from aioresponses import aioresponses
from monitor.ci_gateway.circleci import CircleCI, APIError
from monitor.ci_gateway.constants import CiResult as Result, Integration

os.environ['CIRCLECI_TOKEN'] = 'secret'


class CircleCiTests(aiounittest.AsyncTestCase):
    def test_type(self):
        self.assertEqual(Integration.CIRCLECI,
                         CircleCI(**{
                             'username': 'super-man',
                             'repo': 'awesome'}).get_type())

    def test_map_result(self):
        latest = """{
            "build_num": 1234,
            "outcome": "success",
            "lifecycle": "finished",
            "start_time": "2020-12-28T09:23:57Z",
            "workflows": {
                "workflow_name": "blah"
            },
            "vcs_url": "http://superurl.com"
        }"""
        result = CircleCI.map_result(json.loads(latest))
        self.assertEqual(Integration.CIRCLECI, result["type"])
        self.assertEqual(Result.PASS, result["status"])
        self.assertEqual("2020-12-28T09:23:57Z", result["start"])
        self.assertEqual("2020-12-28T09:23:57Z", result["start"])
        self.assertEqual("blah", result["name"])
        self.assertEqual("http://superurl.com", result["vcs"])
        self.assertEqual(1234, result["id"])

    def test_running(self):
        latest = """{
                    "build_num": 1234,
                    "outcome": "failed",
                    "lifecycle": "not_finished",
                    "start_time": "2020-12-28T09:23:57Z",
                    "workflows": {
                        "workflow_name": "blah"
                    },
                    "vcs_url": "http://superurl.com"
                }"""
        result = CircleCI.map_result(json.loads(latest))
        self.assertEqual(Result.RUNNING, result["status"])

    def test_pass(self):
        latest = """{
                    "build_num": 1234,
                    "outcome": "success",
                    "lifecycle": "finished",
                    "start_time": "2020-12-28T09:23:57Z",
                    "workflows": {
                        "workflow_name": "blah"
                    },
                    "vcs_url": "http://superurl.com"
                }"""
        result = CircleCI.map_result(json.loads(latest))
        self.assertEqual(Result.PASS, result["status"])

    def test_failed(self):
        latest = """{
                    "build_num": 1234,
                    "outcome": "failed",
                    "lifecycle": "finished",
                    "start_time": "2020-12-28T09:23:57Z",
                    "workflows": {
                        "workflow_name": "blah"
                    },
                    "vcs_url": "http://superurl.com"
                }"""
        result = CircleCI.map_result(json.loads(latest))
        self.assertEqual(Result.FAIL, result["status"])

    @aioresponses()
    async def test_gets_latest_from_circle(self, m):
        response_json = os.path.join(
            os.path.dirname(__file__),
            'circleci_response.json')
        with open(response_json) as json_file:
            data = json.load(json_file)

        m.get('https://circleci.com/api/v1.1/project/github/super-man/awesome?shallow=true',  # noqa: E501
              payload=data, status=200)

        action = CircleCI(**{'username': 'super-man',
                             'repo': 'awesome'})
        result = await action.get_latest()
        self.assertEqual(Integration.CIRCLECI, result[0]["type"])
        self.assertEqual(Result.PASS, result[0]["status"])
        self.assertEqual("build_and_test", result[0]["name"])

        self.assertEqual(Integration.CIRCLECI, result[1]["type"])
        self.assertEqual(Result.FAIL, result[1]["status"])
        self.assertEqual("check_vulnerabilities", result[1]["name"])

        self.assertEqual(Integration.CIRCLECI, result[2]["type"])
        self.assertEqual(Result.PASS, result[2]["status"])
        self.assertEqual("scan_for_vulnerabilities", result[2]["name"])

    @aioresponses()
    async def test_ignores_excluded_repo(self, m):
        response_json = os.path.join(
            os.path.dirname(__file__),
            'circleci_response.json')
        with open(response_json) as json_file:
            data = json.load(json_file)

        m.get('https://circleci.com/api/v1.1/project/github/super-man/awesome?shallow=true',  # noqa: E501
              payload=data, status=200)

        action = CircleCI(**{'username': 'super-man',
                             'repo': 'awesome',
                             'excluded_workflows': 'scan_for_vulnerabilities'})
        result = await action.get_latest()
        self.assertEqual("build_and_test", result[0]["name"])
        self.assertEqual("check_vulnerabilities", result[1]["name"])
        self.assertEqual(2, len(result))

    @aioresponses()
    async def test_fails_when_not_200(self, m):
        with pytest.raises(APIError) as excinfo:
            m.get(
                'https://circleci.com/api/v1.1/project/github/super-man/awesome?shallow=true',  # noqa: E501
                status=400)
            action = CircleCI(**{'username': 'super-man',
                                 'repo': 'awesome'})
            await action.get_latest()

        msg = "APIError: GET https://circleci.com/api/v1.1/project/github/super-man/awesome?shallow=true 400"  # noqa: E501
        self.assertEqual(msg, str(excinfo.value))


if __name__ == '__main__':
    aiounittest.main()
