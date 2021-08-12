import os
import logging
from abc import ABC
from itertools import groupby

from monitor.ci_gateway.constants import \
    IntegrationType, CiResult, APIError, IntegrationAdapter, BuildStatus
from aiohttp import ClientSession


class GitHubAction(IntegrationAdapter, ABC):
    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.repo = kwargs.get('repo')
        self.token = os.getenv('GITHUB_TOKEN')
        self.excluded_workflows = kwargs.get('excluded_workflows') or []

    def get_type(self) -> IntegrationType:
        return IntegrationType.GITHUB

    async def get_latest(self) -> BuildStatus:
        super().get_latest()
        base = 'https://api.github.com'
        url = f'{base}/repos/{self.username}/{self.repo}/actions/runs'

        logging.debug(f'Calling {url}')

        async with ClientSession() as session:
            resp = await session.get(
                url,
                headers={'Authorization': f'token {self.token}'})

            if resp.status != 200:
                raise APIError('GET', url, resp.status)

            json = await resp.json()

        response = list(
            map(
                GitHubAction.map_result,
                self.get_unique_latest_jobs(json['workflow_runs'])))
        logging.info(f'Called {url}')
        logging.info(f'Response {response}')
        return response

    @staticmethod
    def map_result(latest) -> BuildStatus:
        conclusion = latest["conclusion"]
        status = latest["status"]
        return BuildStatus(
            type=IntegrationType.GITHUB,
            vcs=latest["html_url"],
            id=latest["id"],
            name=latest["name"],
            start=latest["created_at"],
            status=CiResult.FAIL if status == "completed" and conclusion == "failure" else  # noqa: E501
            CiResult.PASS if status == "completed" and conclusion == "success" else  # noqa: E501
            CiResult.RUNNING if conclusion is None and (status == "queued" or status == "in_progress") else  # noqa: E501
            CiResult.UNKNOWN)

    def get_unique_latest_jobs(self, json):
        jobs = []
        for k, g in groupby(
                sorted(
                    filter(
                        lambda x: x['name']
                        not in self.excluded_workflows,
                        json), key=lambda x: x['name']),
                lambda x: x['name']):
            jobs.append(list(g)[0])

        return jobs


if __name__ == "__main__":
    import argparse
    import sys
    import asyncio

    parser = argparse.ArgumentParser()

    parser.add_argument('--username', help='repo username')
    parser.add_argument('--repo', help='repo to query')

    args = parser.parse_args()

    screen_handler = logging.StreamHandler(stream=sys.stdout)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(screen_handler)

    loop = asyncio.get_event_loop()
    args.excluded_workflows = args.excluded_workflows or []
    task = GitHubAction(
        **{
            'username': args.username,
            'repo': args.repo,
            'excluded_workflows': args.excluded_workflows
        }).get_latest()
    done, pending = loop.run_until_complete(asyncio.wait((task,)))
    for future in done:
        value = future.result()
        print(value)
