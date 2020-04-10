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
