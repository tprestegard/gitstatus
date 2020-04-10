import os
from pyparsing import (
    oneOf, Optional, ZeroOrMore, StringEnd, Suppress, Literal, LineStart,
    LineEnd, Word, Or, alphas, alphanums, printables, restOfLine,
    QuotedString, nestedExpr
)
import re
import subprocess
from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .printer import Printer


def parse_keys(s, loc, toks):
    toks_dict = toks.asDict()
    return {toks_dict["key"][i]: toks_dict["value"][i] \
        for i in range(len(toks_dict["key"]))}


def parse_full(s, loc, toks):
    if len(toks[0]) == 2:
        test = {toks[0][1]: toks[1]}
    else:
        test = toks[1]
    return (toks[0][0], test)


def _parse_gitconfig(config: str) -> Dict[str, Any]:
    # Header
    header = Word(alphas) + Optional(QuotedString('"'))
    full_header = Suppress(LineStart()) + \
        nestedExpr(opener="[", closer="]", content=header) + \
        Suppress(LineEnd())

    # Keys
    key = Word(alphas).setResultsName("key", listAllMatches=True) + \
        Suppress(Literal("=")) + Suppress(Optional(" ")) + \
        restOfLine().setResultsName("value", listAllMatches=True)

    # Full pattern
    full_pattern = full_header + ZeroOrMore(key).setParseAction(parse_keys)
    full_pattern.setParseAction(parse_full)

    result = {}
    for match in full_pattern.scanString(config):
        key, value = match[0][0]
        if key in result:
            result[key].update(value)
        else:
            result.update({key: value})

    return result





class GitConfig:
    comment_regex = re.compile(r'(^\s*;.*\n|\s*;.*)', re.M)

    def __init__(self, path: str):
        # Assumes repo has already been verified and that config file exists
        # Assign attributes
        self.path = path
        self._str = None
        self._cleaned_str = None

    def _load(self) -> str:
        with open(self.path, "rb") as f:
            config = f.read()
        self._str = config.decode()

    def _parse(self):
        # Load full config as a string and store in self._str
        self._load()

        # Remove comments from string
        self._cleaned_str = self._remove_comments(self._str)

        # Parse cleaned config file string
        self._config = _parse_gitconfig(self._cleaned_str)

    def _remove_comments(self):
        return self.comment_regex.sub("", self._str)

    def __repr__(self):
        return f"<GitConfig: {self.path}>"
