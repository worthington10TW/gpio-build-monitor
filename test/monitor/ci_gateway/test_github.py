#!/usr/bin/env python3

import pytest
import json
import os
import aiounittest

from aioresponses import aioresponses

from monitor.ci_gateway.github import GitHubAction, APIError
from monitor.ci_gateway.constants import CiResult as Result, IntegrationType

os.environ['GITHUB_TOKEN'] = 'secret'


class GithubTests(aiounittest.AsyncTestCase):
    def test_type(self):
        self.assertEqual(IntegrationType.GITHUB,
                         GitHubAction(**{
                             'username': 'super-man',
                             'repo': 'awesome'}).get_type())

    def test_map_result(self):
        latest = """{
            "id": 448533827,
            "status": "completed",
            "conclusion": "success",
            "created_at": "2020-12-28T09:23:57Z",
            "html_url": "http://super-thing.com",
            "name": "amazing-workflow"
        }"""
        result = GitHubAction.map_result(json.loads(latest))
        self.assertEqual(IntegrationType.GITHUB, result["type"])
        self.assertEqual(Result.PASS, result["status"])
        self.assertEqual("2020-12-28T09:23:57Z", result["start"])
        self.assertEqual(448533827, result["id"])
        self.assertEqual("amazing-workflow", result["name"])
        self.assertEqual("http://super-thing.com", result["vcs"])

    def test_running(self):
        latest = """{
            "id": 448533827,
            "status": "in_progress",
            "conclusion": null,
            "created_at": "2020-12-28T09:23:57Z",
            "html_url": "http://super-thing.com",
            "name": "amazing-workflow"
        }"""
        result = GitHubAction.map_result(json.loads(latest))
        self.assertEqual(Result.RUNNING, result["status"])

    def test_queued(self):
        latest = """{
            "id": 448533827,
            "status": "queued",
            "conclusion": null,
            "created_at": "2020-12-28T09:23:57Z",
            "html_url": "http://super-thing.com",
            "name": "amazing-workflow"
        }"""
        result = GitHubAction.map_result(json.loads(latest))
        self.assertEqual(Result.RUNNING, result["status"])

    def test_pass(self):
        latest = """{
            "id": 448533827,
            "status": "completed",
            "conclusion": "success",
            "created_at": "2020-12-28T09:23:57Z",
            "html_url": "http://super-thing.com",
            "name": "amazing-workflow"
        }"""
        result = GitHubAction.map_result(json.loads(latest))
        self.assertEqual(Result.PASS, result["status"])

    def test_failed(self):
        latest = """{
            "id": 448533827,
            "status": "completed",
            "conclusion": "failure",
            "created_at": "2020-12-28T09:23:57Z",
            "html_url": "http://super-thing.com",
            "name": "amazing-workflow"
        }"""
        result = GitHubAction.map_result(json.loads(latest))
        self.assertEqual(Result.FAIL, result["status"])

    def test_unknown_not_completed(self):
        latest = """{
            "id": 448533827,
            "status": "something",
            "conclusion": null,
            "created_at": "2020-12-28T09:23:57Z",
            "html_url": "http://super-thing.com",
            "name": "amazing-workflow"
        }"""
        result = GitHubAction.map_result(json.loads(latest))
        self.assertEqual(Result.UNKNOWN, result["status"])

    def test_unknown_completed(self):
        latest = """{
            "id": 448533827,
            "status": "something",
            "conclusion": "completed",
            "created_at": "2020-12-28T09:23:57Z",
            "html_url": "http://super-thing.com",
            "name": "amazing-workflow"
        }"""
        result = GitHubAction.map_result(json.loads(latest))
        self.assertEqual(Result.UNKNOWN, result["status"])

    @aioresponses()
    async def test_gets_latest_from_git(self, m):
        response_json = os.path.join(
            os.path.dirname(__file__),
            'github_response.json')
        with open(response_json) as json_file:
            data = json.load(json_file)

        m.get('https://api.github.com/repos/super-man/awesome/actions/runs',  # noqa: E501
              payload=data, status=200)

        action = GitHubAction(**{'username': 'super-man',
                                 'repo': 'awesome'})
        result = await action.get_latest()

        self.assertEqual(IntegrationType.GITHUB, result[0]["type"])
        self.assertEqual("CI", result[0]["name"])
        self.assertEqual(
            "https://github.com/worthington10TW/gpio-build-monitor/actions/runs/448533827",  # noqa: E501
            result[0]["vcs"])
        self.assertEqual(Result.FAIL, result[0]["status"])

    @aioresponses()
    async def test_fails_when_not_200(self, m):
        with pytest.raises(APIError) as excinfo:
            m.get('https://api.github.com/repos/super-man/awesome/actions/runs',  # noqa: E501
                  body='',
                  status=400)
            action = GitHubAction(**{'username': 'super-man',
                                     'repo': 'awesome'})
            await action.get_latest()

        msg = "APIError: GET https://api.github.com/repos/super-man/awesome/actions/runs 400"  # noqa: E501
        self.assertEqual(msg, str(excinfo.value))


if __name__ == '__main__':
    aiounittest.main()
