#!/usr/bin/env python3
from typing import TypedDict
from enum import Enum
from abc import abstractmethod, ABC
import logging

from build.lib.monitor.ci_gateway.constants import CiResult


class IntegrationType(Enum):
    GITHUB = "GITHUB"
    CIRCLECI = "CIRCLE_CI"


class BuildStatus(TypedDict):
    type: IntegrationType
    vcs: str
    id: str
    name: str
    start: str
    status: CiResult


class IntegrationAdapter(ABC):
    @property
    @abstractmethod
    def get_type(self) -> IntegrationType:
        pass

    @abstractmethod
    def get_latest(self) -> BuildStatus:
        logging.info(f'Initiating integration {self.get_type()}')
        pass


class CiResult(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    RUNNING = "RUNNING"
    UNKNOWN = "UNKNOWN"
    CONNECTION_ERROR = "CONNECTION_ERROR"
    NONE = "NONE"

    def __eq__(self, other):
        return self.value == other.value


class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, verb, url, status, **kwargs):
        self.verb = verb
        self.url = url
        self.status = status
        self.text = kwargs.get("text") or ""

    def __str__(self):
        return f'APIError: {self.verb} {self.url} {self.status}{self.text}'
