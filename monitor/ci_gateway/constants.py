#!/usr/bin/env python3

import enum
from abc import abstractmethod, ABC
import logging


class Integration(enum.Enum):
    GITHUB = "GITHUB"
    CIRCLECI = "CIRCLE_CI"


class IntegrationAdapter(ABC):
    @property
    @abstractmethod
    def get_type(self) -> Integration:
        pass

    @abstractmethod
    def get_latest(self):
        logging.info(f'Initiating integration {self.get_type()}')
        pass


class CiResult(enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    RUNNING = "RUNNING"
    UNKNOWN = "UNKNOWN"
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
