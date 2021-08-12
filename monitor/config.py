#!/usr/bin/env python3

from typing import TypedDict


class IntegrationConfig(TypedDict):
    type: str
    username: str
    repo: str


class Config(TypedDict):
    poll_in_seconds: int
    integrations: IntegrationConfig
