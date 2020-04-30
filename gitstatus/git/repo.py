import configparser
import json
import os
import re
from typing import Dict, List

from .exceptions import NoRemoteError
from .utils import run_command


class GitRepo:
    SECTION_REGEX = re.compile(r'^([a-zA-Z0-9]+) ?(?:"(.+)")?$')

    def __init__(self, path: str):
        # Assign attributes
        self.path = os.path.expanduser(path)
        self._git_path = os.path.join(self.path, ".git")
        self._git_config_path = os.path.join(self._git_path, "config")
        self._current_branch = None
        self._status = None

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
                raise ValueError("Error parsing git config section "
                                 f"{section_name}")
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

    @property
    def current_branch(self, force: bool = False):
        if self._current_branch is None or force:
            result = self._run_command("branch --show-current")
            self._current_branch = result.strip()
        return self._current_branch

    def fetch(self):
        self._run_command("fetch")

    def get_refs(self) -> List[Dict[str, str]]:
        cmd = (f'for-each-ref refs/heads '
               '--format="{\\"name\\": \\"%(refname:short)\\", '
               '\\"remote\\": \\"%(upstream:remotename)\\", '
               '\\"status\\": \\"%(upstream:track)\\"}"')
        output = self._run_command(cmd)
        return [json.loads(entry) for entry in output.split("\n") if entry]

    def get_status(self):
        output = self._run_command("status --porcelain")
        if not output:
            self._status = {}
        else:
            self._status = dict(e.strip().split(' ', 1)[::-1] for e in
                                output.strip().split('\n'))

    @property
    def has_uncommitted_changes(self):
        if not self._status:
            self.get_status()
        if "M" in list(self._status.values()):
            return True
        return False

    @property
    def has_untracked_files(self):
        if not self._status:
            self.get_status()
        if "??" in list(self._status.values()):
            return True
        return False

    def pull_branch(self, branch_name: str):
        # Try to get the branch from the config. If branch is None, it doesn't
        # have a remote
        branch = self.config.get("branch", {}).get(branch_name, None)
        if branch is None:
            raise NoRemoteError(f"Branch {branch_name} has no remote")

        # Otherwise, get the command to run
        if branch_name == self.current_branch:
            # Have to use 'git pull' if we are trying to update the
            # current branch
            cmd = "pull"
        else:
            # Use this 'git fetch' variation to pull into another branch; for
            # some reason it doesn't work on the current branch
            cmd = f'fetch {branch["remote"]} {branch_name}:{branch_name}'

        # Run command
        self._run_command(cmd)

    def _run_command(self, cmd: str):
        return run_command(
            f"git -C {self.path} --git-dir={self._git_path} {cmd}"
        )

    def __repr__(self):
        return f"<GitRepo: {self.path}>"
