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


def _parse_gitconfig(config: str) -> Dict[str, Any]:
    # Header
    header = Word(alphas) + Optional(QuotedString('"'))
    full_header = Suppress(LineStart()) + \
        nestedExpr(opener="[", closer="]", content=header) + \
        Suppress(LineEnd())
    #full_header = Suppress(LineStart()) + Suppress(Literal("[")) + \
    #    header + Suppress(Literal("]")) + Suppress(LineEnd())

    # Keys
    key = Word(alphas) + Suppress(Literal("=")) + Suppress(Optional(" ")) + \
        restOfLine()

    # Full pattern
    full_pattern = full_header + ZeroOrMore(key)

    #return full_header
    return [match for match in full_pattern.scanString(config)]

class GitRepo:

    def __init__(self, path: str, printer: 'Printer'):
        # Assign attribute
        self.path = path
        self._printer = printer

        # Do some checks
        self._check_path_exists()
        self._check_is_git_repo()

        # Load config

    def _run_command(self, cmd: str):
        p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        try:
            stdout, stderr = p.communicate()
        except Exception as ex:
        
            pass

        

    def _check_path_exists(self):
        if not os.path.exists(self.path):
            self._printer.error(f"{self.path} does not exist", vlevel=0)
            raise SystemExit(1)
        elif not os.path.isdir(self.path):
            self._printer.error(f"{self.path} is not a directory", vlevel=0)
            raise SystemExit(1)

    def _check_is_git_repo(self):
        _git_path = os.path.join(self.path, ".git")
        _git_config_path = os.path.join(_git_path, "config")

        err_msg = None
        if not os.path.exists(_git_path):
            err_msg = (f"Directory at {self.path} is not a git repo - "
                       "no .git directory")
        elif not os.path.isdir(_git_path):
            err_msg = f"Expected .git directory {_git_path} is not a directory"
        elif not os.path.exists(_git_config_path):
            pass
        elif not os.path.isfile(_git_config_path):
            pass

        if err_msg:
            self._printer.error(err_msg)
            raise SystemExit(1)

    def _check_has_remote(self):
        pass

    def __repr__(self):
        return f"<GitRepo: {self.path}>"


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
        self._config = {}

    def _remove_comments(self):
        return self.comment_regex.sub("", self._str)

    def __repr__(self):
        return f"<GitConfig: {self.path}>"
