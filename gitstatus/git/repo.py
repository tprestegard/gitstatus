import configparser
import json
import os
import re
import typing

from .utils import run_command


if typing.TYPE_CHECKING:
    from ..printer import Printer


class GitRepo:
    SECTION_REGEX = re.compile(r'^([a-zA-Z0-9]+) ?(?:"(.+)")?$')

    def __init__(self, path: str, printer: 'Printer'):
        # Assign attributes
        self.path = os.path.expanduser(path)
        self._git_path = os.path.join(self.path, ".git")
        self._git_config_path = os.path.join(self._git_path, "config")

        # Do some checks
        self._check_path_exists()
        self._check_is_git_repo()

        # Load config
        self.config = self._load_config()

    def _check_path_exists(self):
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"{self.path} does not exist")
        elif not os.path.isdir(self.path):
            raise TypeError(f"{self.path} is not a directory")

    def _check_is_git_repo(self):
        err_msg = None
        if not os.path.exists(self._git_path):
            err_msg = (f"Directory at {self.path} is not a git repo - "
                       "no .git directory")
        elif not os.path.exists(self._git_config_path):
            err_msg = (f"Git config (expected at {self._git_config_path}) "
                       "does not exist")
        if err_msg:
            raise FileNotFoundError(err_msg)

        if not os.path.isdir(self._git_path):
            err_msg = (f"Expected .git directory {self._git_path} is not a "
                       "directory")
        elif not os.path.isfile(self._git_config_path):
            err_msg = f"Git config ({self._git_config_path}) is not a file"

        if err_msg:
            raise TypeError(err_msg)

    def _load_config(self):
        cp = configparser.ConfigParser()
        cp.read(self._git_config_path)
        config = {}
        for section_name in cp.sections():
            match = self.SECTION_REGEX.search(section_name)
            if not match:
                # TODO
                raise Exception(section_name)
            header, subheader = match.groups()
            params = dict(cp.items(section_name))
            if subheader is None:
                config.update({header: params})
            else:
                if header in config:
                    config[header].update({subheader: params})
                else:
                    config.update({header: {subheader: params}})
        return config

    @property
    def branches(self):
        return list(self.config.get("branch"))

    def fetch(self):
        run_command(f"git --git-dir={self._git_path} fetch")

    def get_status(self):
        return run_command(f"git --git-dir={self._git_path} status")

    def get_refs(self) -> str:
        cmd = (f'git --git-dir={self._git_path} for-each-ref refs/heads '
               '--format="{\\"name\\": \\"%(refname:short)\\", '
               '\\"remote\\": \\"%(upstream:remotename)\\", '
               '\\"status\\": \\"%(upstream:track)\\"}"')
        output = run_command(cmd)
        return [json.loads(entry) for entry in output.split("\n") if entry]

    def __repr__(self):
        return f"<GitRepo: {self.path}>"
