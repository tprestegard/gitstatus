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


def _parse_param(s, loc, toks):
    return toks.asDict()


def _parse_params(s, loc, toks):
    return {tok["key"]: tok["value"] for tok in toks}


def _parse_header(s, loc, toks):
    return toks.asDict()["header"][0][0]


def _parse_full(s, loc, toks):
    headers = toks.asDict()["header"]
    params = toks.asDict()["params"]
    result = {}
    for i in range(len(headers)):
        h_m = headers[i].get("mainheader")
        h_s = headers[i].get("subheader", None)

        if h_s is None:
            result.update({h_m: params[i]})
        else:
            if h_m in result:
                result[h_m].update({h_s: params[i]})
            else:
                result.update({h_m: {h_s: params[i]}})
    return result


def _parse_gitconfig(config: str) -> Dict[str, Any]:
    # Header
    header = Word(alphas).setResultsName("mainheader") + \
        Optional(QuotedString('"')).setResultsName("subheader")
    full_header = Suppress(LineStart()) + \
        nestedExpr(opener="[", closer="]", content=header) + \
        Suppress(LineEnd())
    full_header.setParseAction(_parse_header)

    # Keys
    key = Word(alphas).setResultsName("key") + Suppress(Literal("=")) + \
        Suppress(Optional(" ")) + restOfLine().setResultsName("value")
    key.setParseAction(_parse_param)
    params = ZeroOrMore(key).setParseAction(_parse_params)

    ## Full pattern
    full_pattern = ZeroOrMore(
        full_header.setResultsName("header", listAllMatches=True) +
        params.setResultsName("params", listAllMatches=True)
    )
    full_pattern.setParseAction(_parse_full)

    return full_pattern.parseString(config)[0]


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
