#!/usr/bin/env python3
from typing import List

from monitor.ci_gateway.constants import IntegrationType
from monitor.config import IntegrationConfig


class IntegrationMapper(object):
    def __init__(self, available_integrations: List[IntegrationConfig]):
        self.available_integrations = available_integrations

    def get(self, integrations):
        for i in integrations:
            if i['type'] not in IntegrationType.__members__:
                raise MismatchError(i['type'])

        return list(map(self._map, integrations))

    def _map(self, integration: IntegrationConfig):
        integration_type = IntegrationType[integration['type']]
        return self.available_integrations[integration_type](
            **integration).get_latest


class MismatchError(Exception):
    """An Integration Error Exception"""

    def __init__(self, integration):
        self.integration = integration

    def __str__(self):
        return f'Integration error: we currently do not integrate with {self.integration}.'  # noqa: E501
