#!/usr/bin/env python3
from typing import Mapping

from monitor.ci_gateway.circleci import CircleCI
from monitor.ci_gateway.github import GitHubAction
from monitor.ci_gateway.constants import IntegrationType, IntegrationAdapter


def get_all() -> Mapping[IntegrationType, IntegrationAdapter]:
    action = {
        IntegrationType.GITHUB: GitHubAction,
        IntegrationType.CIRCLECI: CircleCI
    }

    return dict(map((lambda x: (x, action.get(x))), IntegrationType))
