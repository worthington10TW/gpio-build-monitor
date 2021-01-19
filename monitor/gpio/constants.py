#!/usr/bin/env python3

import enum


class Lights(enum.Enum):
    GREEN = 17
    YELLOW = 22
    RED = 27
    BLUE = 18

    def __str__(self):
        return f"{{ Colour: {self.name}, Pin: {self.value} }}"
