import os
import logging
from abc import ABC
from itertools import groupby

from monitor.ci_gateway.constants import Integration, \
    APIError, IntegrationAdapter, CiResult
from aiohttp import ClientSession, client_exceptions


class CircleCI(IntegrationAdapter, ABC):
    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.repo = kwargs.get('repo')
        self.token = os.getenv('CIRCLE_CI_TOKEN')
        self.excluded_workflows = kwargs.get('excluded_workflows') or []

    def get_type(self):
        return Integration.CIRCLECI

    async def get_latest(self):
        super().get_latest()
        base = 'https://circleci.com/api/v1.1'
        url = f'{base}/project/github/{self.username}/{self.repo}?shallow=true'  # noqa: E501
        logging.debug(f'Calling {url}')

        async with ClientSession() as session:
            resp = await session.get(
                url,
                headers={'Circle-Token': f'{self.token}',
                         'Accept': 'application/json',
                         'Content-Type': 'application/json'})

            if resp.status != 200:
                raise APIError('GET', url, resp.status)

            try:
                json = await resp.json(content_type=None)
            except client_exceptions.ContentTypeError:
                raise APIError('GET',
                               url,
                               resp.status,
                               text=await resp.text())

        response = list(
            map(
                CircleCI.map_result,
                self.get_unique_latest_jobs(json)))
        logging.info(f'Called {url}')
        logging.info(f'Response {response}')
        return response

    @staticmethod
    def map_result(latest):
        outcome = latest["outcome"]
        lifecycle = latest["lifecycle"]
        return dict(
            type=Integration.CIRCLECI,
            vcs=latest["vcs_url"],
            id=latest["build_num"],
            name=latest['workflows']['workflow_name'],
            start=latest["start_time"],
            status=CiResult.RUNNING if lifecycle != "finished" else
            CiResult.FAIL if outcome != "success" else  # noqa: E501
            CiResult.PASS)

    def get_unique_latest_jobs(self, json):
        jobs = []
        for k, g in groupby(
                sorted(
                    filter(
                        lambda x:
                        x['workflows']['workflow_name']not in
                        self.excluded_workflows,
                        json), key=lambda x: x['workflows']['workflow_name']),
                lambda x: x['workflows']['workflow_name']):
            jobs.append(list(g)[0])

        return jobs


if __name__ == "__main__":
    import argparse
    import sys
    import asyncio

    parser = argparse.ArgumentParser()

    parser.add_argument('--username', help='repo username')
    parser.add_argument('--repo', help='repo to query')
    parser.add_argument('--excluded_workflows', help='excluded workflows')

    args = parser.parse_args()

    screen_handler = logging.StreamHandler(stream=sys.stdout)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(screen_handler)

    loop = asyncio.get_event_loop()

    args.excluded_workflows = args.excluded_workflows or []
    task = CircleCI(
        **{
            'username': args.username,
            'repo': args.repo,
            'excluded_workflows': args.excluded_workflows
        }).get_latest()
    done, pending = loop.run_until_complete(asyncio.wait((task,)))
    for future in done:
        value = future.result()
        print(value)
