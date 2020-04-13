import typing

if typing.TYPE_CHECKING:
    from .repo import GitRepo


class GitChecker:
    def __init__(self, repo: 'GitRepo'):
        self.repo = repo

    def run_checks(self):
        # Check if repo has a remote
        has_remote = self._has_remote()

        # Git fetch
        # Get current branch and store it - if not on a branch, fail
        # Check for uncommitted changes on current branch; if any, make a note
        #     and stash them
        # Check if branch has a remote; if not then raise warning
        # If has remote, then check if we are in sync with it
        # Move to next branch and repeat the last two steps
        # When done with all branches, return to initial branch and unstash
        # any stashed changes

    def _has_remote(self):
        return "remote" in self.repo.config
