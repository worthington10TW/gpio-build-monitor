#!/usr/bin/env python3

import aiounittest

from monitor.ci_gateway import integration_actions
from monitor.ci_gateway.constants import Integration
from monitor.ci_gateway.github import GitHubAction
from monitor.ci_gateway.circleci import CircleCI


class IntegrationsTests(aiounittest.AsyncTestCase):
    def test_get_all(self):
        result = integration_actions.get_all()

        assert GitHubAction is result[Integration.GITHUB]
        assert CircleCI is result[Integration.CIRCLECI]

        self.assertEqual(2, len(result))


if __name__ == '__main__':
    aiounittest.main()
