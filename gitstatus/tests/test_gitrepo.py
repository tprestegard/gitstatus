from unittest import mock

import pytest

from gitstatus.git.repo import GitRepo


###############################################################################
# FIXTURES ####################################################################
###############################################################################
@pytest.fixture
def gitrepo_instance():
    with mock.patch("gitstatus.git.os.path.exists"), mock.patch(
        "gitstatus.git.os.path.isdir"
    ), mock.patch("gitstatus.git.os.path.isfile"):
        g = GitRepo("fake_path", mock.Mock())
    return g
